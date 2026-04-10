import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.getcwd())

import config
from supabase_utils import SupabaseClient

def get_urls_missing_desc():
    client = SupabaseClient()
    try:
        res = client.client.table("inm_propiedades").select("id, referencia, url, descripcion").or_("descripcion.is.null, descripcion.eq.").execute()
        data = res.data
        
        print(f"Propiedades sin descripción encontradas: {len(data)}")
        for i, r in enumerate(data):
            ref = r.get('referencia', 'N/A')
            url = r.get('url', 'N/A')
            print(f"{i+1}. Ref: {ref} | URL: {url}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_urls_missing_desc()
