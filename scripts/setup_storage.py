import sys
import os

# Añadir el directorio raíz al path para importar supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import supabase_utils

def setup_storage():
    """Crea el bucket 'propiedades' en Supabase Storage si no existe"""
    try:
        # Intentar crear el bucket con acceso público
        supabase_utils.supabase.storage.create_bucket(
            'propiedades', 
            options={'public': True}
        )
        print("INFO: Bucket 'propiedades' creado exitosamente.")
    except Exception as e:
        # Si ya existe, nos dará un error que podemos ignorar
        error_str = str(e)
        if "already exists" in error_str.lower() or "Duplicate" in error_str:
            print("INFO: El bucket 'propiedades' ya existe.")
        else:
            print(f"ERROR: No se pudo crear el bucket: {e}")

if __name__ == "__main__":
    setup_storage()
