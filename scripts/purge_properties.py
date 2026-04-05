import os
import sys

# Añadir el directorio raíz al path para importar supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import supabase_utils
from supabase import create_client, Client
import config

def purge_all_properties():
    """Elimina todos los registros de la tabla inm_propiedades"""
    print("PURGA: Iniciando eliminacion de todas las propiedades...")
    
    # Usar el cliente directamente para un delete sin filtros
    supabase = supabase_utils.supabase
    try:
        response = supabase.table("inm_propiedades").delete().gt("id", 0).execute()
        count = len(response.data) if response.data else 0
        print(f"OK PURGA: Eliminados {count} registros de inm_propiedades.")
        return True
    except Exception as e:
        print(f"ERROR PURGA: {e}")
        return False

if __name__ == "__main__":
    confirm = input("¿Estás seguro de que deseas eliminar todas las propiedades? (s/n): ")
    if confirm.lower() == 's':
        purge_all_properties()
    else:
        print("Operación cancelada.")
