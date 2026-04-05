import json
import os
import re
import sys
import requests

# Añadir el directorio raíz al path para importar supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import supabase_utils

def download_image(url, folder, filename):
    """Descarga una imagen y la guarda localmente"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(os.path.join(folder, filename), "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"Error HTTP {response.status_code} al descargar {url}")
            return False
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return False

def upload_to_supabase_storage(local_path, bucket_name, remote_path):
    """Sube una imagen local al Bucket de Supabase Storage"""
    try:
        with open(local_path, 'rb') as f:
            res = supabase_utils.supabase.storage.from_(bucket_name).upload(
                path=remote_path,
                file=f,
                file_options={"content-type": "image/jpeg", "upsert": "true"}
            )
            if res:
                # Retornar la URL pública del archivo subido
                public_url = supabase_utils.supabase.storage.from_(bucket_name).get_public_url(remote_path)
                return public_url
            return None
    except Exception as e:
        print(f"Error al subir {local_path} a Storage: {e}")
        return None

def process_property_deep_data(property_data):
    """Procesa una propiedad: descarga fotos, sube a Supabase Storage y actualiza DB"""
    ref = property_data.get('referencia')
    if not ref:
        print("Error: Propiedad sin referencia.")
        return False
        
    print(f"\n--- PROCESANDO: {ref} ---")
    
    # Crear estructura de carpetas local
    prop_dir = os.path.join("data", "propiedades", ref)
    photos_dir = os.path.join(prop_dir, "fotos")
    os.makedirs(photos_dir, exist_ok=True)
    
    # 1. Descargar y Subir fotos
    supabase_urls = []
    print(f"INFO: Procesando {len(property_data.get('imagenes_url', []))} fotos...")
    
    for i, url in enumerate(property_data.get('imagenes_url', [])):
        # Descarga local
        ext = url.split('.')[-1].split('?')[0]
        if len(ext) > 4: ext = "jpg" # Fallback for messy URLs
        filename = f"foto_{i+1:02d}.{ext}"
        local_path = os.path.join(photos_dir, filename)
        
        if download_image(url, photos_dir, filename):
            # Subida a Supabase
            remote_path = f"{ref}/{filename}"
            s3_url = upload_to_supabase_storage(local_path, "propiedades", remote_path)
            if s3_url:
                supabase_urls.append(s3_url)
            else:
                # Si falla la subida, guardamos la URL original como fallback
                supabase_urls.append(url)
                
    # 2. Actualizar Supabase (Base de Datos)
    try:
        existing = supabase_utils.supabase.table("inm_propiedades").select("id").eq("referencia", ref).execute()
        if existing.data:
            record_id = existing.data[0]['id']
            
            update_fields = {
                "titulo": property_data.get('titulo'),
                "descripcion": property_data.get('descripcion'),
                "caracteristicas": property_data.get('caracteristicas'),
                "imagenes_url": supabase_urls, # Ahora apuntan a TU Supabase
                "latitud": property_data.get('latitud'),
                "longitud": property_data.get('longitud'),
                "estado_publicacion": "Activo"
            }
            
            supabase_utils.supabase.table("inm_propiedades").update(update_fields).eq("id", record_id).execute()
            print(f"ÉXITO: {ref} sincronizado (Local + Storage + DB).")
            return True
        else:
            print(f"ERROR: No se encontró la referencia {ref} en la base de datos.")
            return False
    except Exception as e:
        print(f"Error final en base de datos: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # El argumento debe ser la RUTA al archivo JSON
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: Archivo {file_path} no encontrado.")
            sys.exit(1)
            
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data_list = json.load(f)
                for prop in data_list:
                    process_property_deep_data(prop)
            except Exception as e:
                print(f"Error procesando archivo JSON: {e}")
    else:
        print("Uso: python scripts/deep_scraper_final.py [ruta_archivo_json]")
