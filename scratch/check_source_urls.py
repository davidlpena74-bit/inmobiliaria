import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.getcwd())

import config
from supabase_utils import SupabaseClient

def check_source_urls():
    client = SupabaseClient()
    try:
        # Buscar propiedades sin descripción y ver sus URLs y características
        res = client.client.table("inm_propiedades").select("id, referencia, url, caracteristicas").or_("descripcion.is.null, descripcion.eq.").limit(10).execute()
        data = res.data
        
        for r in data:
            print(f"Ref: {r.get('referencia')}")
            print(f"  DB URL: {r.get('url')}")
            caract = r.get('caracteristicas', {})
            if isinstance(caract, dict):
                # Buscar posibles URLs originales
                orig_url = caract.get('original_url') or caract.get('source_url') or caract.get('url')
                print(f"  Caract URL: {orig_url}")
                # Si no hay, ver todas las llaves para pistas
                print(f"  Keys: {list(caract.keys())}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_source_urls()
