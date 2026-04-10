import os
import requests
import sys
import mimetypes
from urllib.parse import urlparse

# Add current directory to path
sys.path.append(os.getcwd())

from supabase_utils import supabase

BUCKET_NAME = "propiedades"

def get_public_storage_url(path):
    """Utility to get the full public URL for a storage path"""
    return f"https://dwbvegnxmyvpolvofkfn.supabase.co/storage/v1/object/public/{BUCKET_NAME}/{path}"

def sync():
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

    synced_count = 0
    migrated_count = 0
    failed_count = 0

    for prop in properties:
        ref = prop.get("referencia")
        if not ref:
            continue
            
        urls = prop.get("imagenes_url") or []
        carac = prop.get("caracteristicas") or {}
        
        # Backup original URLs if not already backed up
        if urls and urls[0].startswith("http") and "supabase" not in urls[0]:
            if "original_urls" not in carac:
                carac["original_urls"] = urls
        elif not urls and "original_urls" in carac:
            # Maybe they were already moved or cleared?
            urls = carac["original_urls"]

        print(f"[{ref}] Comprobando bucket...")
        
        try:
            # Check if folder exists in bucket
            # The list command lists files in a prefix.
            folder_content = supabase.storage.from_(BUCKET_NAME).list(ref)
            
            if folder_content:
                print(f"  - Carpeta encontrada con {len(folder_content)} archivos. Sincronizando...")
                new_urls = []
                for item in folder_content:
                    # Skip if it's a "folder" entry (size 0 and no metadata often used for folders in some APIs)
                    # For Supabase, list() returns objects.
                    file_path = f"{ref}/{item['name']}"
                    new_urls.append(get_public_storage_url(file_path))
                
                # Update DB
                supabase.table("inm_propiedades").update({
                    "imagenes_url": new_urls,
                    "caracteristicas": carac
                }).eq("id", prop["id"]).execute()
                synced_count += 1
                
            else:
                # Case B: Folder does NOT exist, download and upload
                if not urls or (urls and "supabase" in urls[0]):
                    print(f"  - Carpeta no encontrada y no hay URLs externas válidas para descargar. Saltando.")
                    continue
                    
                print(f"  - Carpeta no encontrada. Iniciando descarga/subida de {len(urls)} imágenes...")
                new_urls = []
                
                for i, url in enumerate(urls):
                    try:
                        response = requests.get(url, timeout=15)
                        if response.status_code != 200:
                            new_urls.append(url)
                            continue
                        
                        content = response.content
                        parsed_url = urlparse(url)
                        ext = os.path.splitext(parsed_url.path)[1] or ".jpg"
                        if "?" in ext: ext = ext.split("?")[0]
                        
                        filename = f"img_{i}{ext}"
                        storage_path = f"{ref}/{filename}"
                        content_type = mimetypes.guess_type(filename)[0] or "image/jpeg"
                        
                        supabase.storage.from_(BUCKET_NAME).upload(
                            storage_path, 
                            content, 
                            {"content-type": content_type, "upsert": "true"}
                        )
                        
                        new_urls.append(get_public_storage_url(storage_path))
                    except Exception as e:
                        print(f"    * Error en imagen {i}: {e}")
                        new_urls.append(url)
                
                # Update DB
                supabase.table("inm_propiedades").update({
                    "imagenes_url": new_urls,
                    "caracteristicas": carac
                }).eq("id", prop["id"]).execute()
                migrated_count += 1
                
        except Exception as e:
            print(f"  - Error procesando {ref}: {e}")
            failed_count += 1

    print("\n--- RESUMEN DE SINCRONIZACIÓN ---")
    print(f"Propiedades sincronizadas (ya estaban en bucket): {synced_count}")
    print(f"Propiedades migradas (descargadas y subidas): {migrated_count}")
    print(f"Propiedades fallidas: {failed_count}")

if __name__ == "__main__":
    sync()
