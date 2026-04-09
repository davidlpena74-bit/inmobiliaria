import sys
import os

# Añadir el directorio raíz al path para importar supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import supabase_utils
import config

def migrate():
    print("Iniciando migracion de 'tipo_operacion'...")
    
    # Obtener todas las propiedades
    try:
        response = supabase_utils.supabase.table(supabase_utils.TBL_PROPIEDADES).select("id, precio").execute()
        propiedades = response.data
        print(f"Encontradas {len(propiedades)} propiedades.")
    except Exception as e:
        print(f"Error al obtener propiedades: {e}")
        return

    # Actualizar cada propiedad
    count = 0
    for p in propiedades:
        tipo = 'Alquiler' if (p['precio'] or 0) < 10000 else 'Venta'
        try:
            supabase_utils.supabase.table(supabase_utils.TBL_PROPIEDADES).update({"tipo_operacion": tipo}).eq("id", p['id']).execute()
            count += 1
            if count % 50 == 0:
                print(f"Procesadas {count}/{len(propiedades)}...")
        except Exception as e:
            print(f"Error actualizando propiedad {p['id']}: {e}")

    print(f"Migracion finalizada. Se actualizaron {count} propiedades.")

if __name__ == "__main__":
    migrate()
