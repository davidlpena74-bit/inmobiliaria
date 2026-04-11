import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.getcwd())

import config
from supabase_utils import SupabaseClient

def audit_missing_fields():
    client = SupabaseClient()
    try:
        # Obtener todas las propiedades para filtrar localmente (evitar problemas de sintaxis de filtros complejos en una sola query)
        # O intentar una query filtrada más robusta
        res = client.client.table("inm_propiedades").select("id, referencia, titulo, descripcion, tipo").execute()
        properties = res.data
        
        missing_both = []
        missing_desc = []
        missing_tipo = []
        
        for p in properties:
            has_desc = bool(p.get('descripcion') and p.get('descripcion').strip())
            has_tipo = bool(p.get('tipo') and p.get('tipo').strip())
            
            if not has_desc and not has_tipo:
                missing_both.append(p)
            elif not has_desc:
                missing_desc.append(p)
            elif not has_tipo:
                missing_tipo.append(p)

        print(f"Total de propiedades analizadas: {len(properties)}")
        print(f"Propiedades sin descripción Y sin tipo: {len(missing_both)}")
        print(f"Propiedades solo sin descripción: {len(missing_desc)}")
        print(f"Propiedades solo sin tipo: {len(missing_tipo)}")
        print("-" * 50)
        
        if missing_both:
            print("EJEMPLOS SIN AMBOS CAMPOS:")
            for p in missing_both[:10]:
                print(f"- Ref: {p.get('referencia')} | Título: {p.get('titulo')}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_missing_fields()
