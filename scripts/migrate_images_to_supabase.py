import os
import requests
import sys
import mimetypes
from urllib.parse import urlparse

# Add current directory to path
sys.path.append(os.getcwd())

from supabase_utils import supabase

BUCKET_NAME = "propiedades_images"

def setup_storage():
    """Ensure the bucket exists and is public"""
    try:
        # Check if bucket exists
        buckets = supabase.storage.list_buckets()
        exists = any(b.name == BUCKET_NAME for b in buckets)
        
        if not exists:
            print(f"Creando bucket '{BUCKET_NAME}'...")
            supabase.storage.create_bucket(BUCKET_NAME, {"public": True})
            print("Bucket creado con éxito.")
        else:
            print(f"El bucket '{BUCKET_NAME}' ya existe.")
    except Exception as e:
        print(f"Error configurando storage: {e}")

def migrate():
    setup_storage()
    
    # 1. Obtener propiedades (excepto Coldwell Banker)
    print("Obteniendo propiedades de la base de datos...")
    try:
        query = supabase.table("inm_propiedades").select("*").neq("agente", "coldwellbanker")
        res = query.execute()
        properties = res.data
        print(f"Total propiedades a procesar: {len(properties)}")
    except Exception as e:
        print(f"Error obteniendo propiedades: {e}")
        return

    total_uploaded = 0
    total_size_bytes = 0

    for prop in properties:
        ref = prop.get("referencia")
        urls = prop.get("imagenes_url") or []
        
        if not urls:
            continue
            
        # Saltarse si ya son URLs de Supabase (heurística simple)
        if urls and "supabase.co/storage" in urls[0]:
            print(f"[{ref}] Ya migrado. Saltando.")
            continue

        print(f"[{ref}] Procesando {len(urls)} imágenes...")
        
        # Backup original URLs if not already backed up
        carac = prop.get("caracteristicas") or {}
        if "original_urls" not in carac:
            carac["original_urls"] = urls
            
        new_urls = []
        
        for i, url in enumerate(urls):
            try:
                # 2. Descargar imagen
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    print(f"  - Error descargando {url}: {response.status_code}")
                    new_urls.append(url) # Mantener original si falla
                    continue
                
                content = response.content
                file_size = len(content)
                total_size_bytes += file_size
                
                # Determinar extensión
                parsed_url = urlparse(url)
                ext = os.path.splitext(parsed_url.path)[1] or ".jpg"
                if "?" in ext: ext = ext.split("?")[0]
                
                filename = f"img_{i}{ext}"
                file_path = f"{ref}/{filename}"
                
                # Determinar content-type
                content_type = mimetypes.guess_type(filename)[0] or "image/jpeg"
                
                # 3. Subir a Supabase Storage
                # Usamos upsert=True para evitar errores si ya existe
                supabase.storage.from_(BUCKET_NAME).upload(
                    file_path, 
                    content, 
                    {"content-type": content_type, "upsert": "true"}
                )
                
                # 4. Obtener URL pública
                public_url_res = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
                new_urls.append(public_url_res)
                total_uploaded += 1
                
            except Exception as e:
                print(f"  - Error en imagen {i}: {e}")
                new_urls.append(url)

        # 5. Actualizar propiedad en DB
        try:
            supabase.table("inm_propiedades").update({
                "imagenes_url": new_urls,
                "caracteristicas": carac
            }).eq("id", prop["id"]).execute()
            print(f"  - OK: {len(new_urls)} imágenes actualizadas.")
        except Exception as e:
            print(f"  - Error actualizando DB para {ref}: {e}")

    print("\n--- RESUMEN DE MIGRACIÓN ---")
    print(f"Total archivos subidos: {total_uploaded}")
    print(f"Espacio total ocupado: {total_size_bytes / (1024*1024):.2f} MB")
    print(f"Limite Supabase Free: 1024.00 MB")
    if total_size_bytes > 0:
        print(f"Porcentaje del límite: {(total_size_bytes / (1024*1024*1024)) * 100:.2f}%")

if __name__ == "__main__":
    migrate()
