import os
import mimetypes
from supabase import create_client, Client
import config
import supabase_utils

def subir_fotos():
    # Inicializar cliente
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    
    base_dir = os.path.join("data", "propiedades")
    if not os.path.exists(base_dir):
        print(f"Error: No se encontro el directorio {base_dir}")
        return

    bucket_name = "propiedades"
    print(f"--- Iniciando subida de fotos al bucket '{bucket_name}' ---")

    # Listar subdirectorios (cada uno es una referencia de propiedad)
    refs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for ref in refs:
        fotos_dir = os.path.join(base_dir, ref, "fotos")
        if not os.path.exists(fotos_dir):
            continue

        print(f"\n--- Procesando propiedad: {ref} ---")
        
        # Buscar archivos de imagen en la carpeta fotos
        carpetas_fotos = os.listdir(fotos_dir)
        extensiones_validas = ('.jpg', '.jpeg', '.png', '.webp')
        fotos_locales = [f for f in carpetas_fotos if f.lower().endswith(extensiones_validas)]
        
        if not fotos_locales:
            print(f"  Aviso: No hay fotos validas en {fotos_dir}")
            continue

        public_urls = []
        
        for foto_name in fotos_locales:
            local_path = os.path.join(fotos_dir, foto_name)
            remote_path = f"{ref}/{foto_name}"
            
            # Detectar content-type
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                content_type = "image/jpeg"

            try:
                print(f"  Subiendo {foto_name}...", end=" ", flush=True)
                with open(local_path, "rb") as f:
                    # Usar x-upsert para sobrescribir si ya existe
                    res = supabase.storage.from_(bucket_name).upload(
                        remote_path, 
                        f, 
                        {"content-type": content_type, "x-upsert": "true"}
                    )
                
                # Construir URL pública (formato estándar de Supabase)
                # https://dwbvegnxmyvpolvofkfn.supabase.co/storage/v1/object/public/propiedades/REF/FOTO.jpg
                public_url = f"{config.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{remote_path}"
                public_urls.append(public_url)
                print("OK")
                
            except Exception as e:
                # Si es un error de duplicado (ya existe y no se usó upsert o falló)
                if "already exists" in str(e).lower():
                    public_url = f"{config.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{remote_path}"
                    public_urls.append(public_url)
                    print("OK (ya existe)")
                else:
                    print(f"ERROR: {e}")

        # Actualizar base de datos con las nuevas URLs
        if public_urls:
            print(f"  Actualizando base de datos con {len(public_urls)} fotos...", end=" ", flush=True)
            res_db = supabase_utils.update_propiedad_fotos(ref, public_urls)
            if res_db:
                print("OK")
            else:
                print("FALLO")

    print("\n--- Proceso de subida finalizado. ---")

if __name__ == "__main__":
    subir_fotos()
