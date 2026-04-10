import sys
import os

# Añadir el directorio raíz al path para poder importar config y supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from supabase_utils import SupabaseClient

# Configurar salida UTF-8 para consola Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def find_missing_descriptions():
    client = SupabaseClient()
    
    # Intentar obtener propiedades de alquiler (precio < 5000 es un buen proxy si no hay flag)
    # Y que no tengan descripción
    try:
        # Paginamos si es necesario, pero para este chequeo 1000 debería bastar
        res = client.client.table("inm_propiedades").select("referencia, titulo, precio, descripcion, agente").is_("descripcion", "null").execute()
        null_props = res.data
        
        res_empty = client.client.table("inm_propiedades").select("referencia, titulo, precio, descripcion, agente").eq("descripcion", "").execute()
        empty_props = res_empty.data
        
        all_missing = null_props + empty_props
        
        # Filtrar por alquiler (precio < 5000)
        rentals_missing = [p for p in all_missing if p.get('precio', 0) < 5000]
        
        print(f"Total de propiedades sin descripción: {len(all_missing)}")
        print(f"Propiedades de ALQUILER (precio < 5000) sin descripción: {len(rentals_missing)}")
        print("-" * 50)
        
        for p in rentals_missing:
            print(f"Ref: {p['referencia']} | Precio: {p['precio']}€ | Agente: {p['agente']} | Título: {p['titulo']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_missing_descriptions()
