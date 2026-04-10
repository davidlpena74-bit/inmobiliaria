import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from supabase_utils import supabase

def check():
    try:
        print("Intentando listar bucket 'propiedades'...")
        res = supabase.storage.from_('propiedades').list("", {"limit": 100})
        print(f"Éxito. Encontrados {len(res)} objetos en la raíz del bucket 'propiedades'.")
        
        if res:
            print("\nDetalle de los primeros 20 objetos:")
            for item in res[:20]:
                name = item.get('name', 'N/A')
                # Check if it looks like an image or a directory
                metadata = item.get('metadata')
                mimetype = metadata.get('mimetype', 'folder') if metadata else 'folder'
                size = metadata.get('size', 0) if metadata else 0
                print(f"  - [{mimetype}] {name} ({size} bytes)")
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error accediendo al bucket: {e}")

if __name__ == "__main__":
    check()
