import json
import os
import sys

# Añadir el directorio raíz al path para importar supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import supabase_utils

def update_properties_from_file(file_path):
    """Actualiza propiedades en Supabase buscando por referencia e inyectando datos profundos"""
    if not os.path.exists(file_path):
        print(f"Error: Archivo {file_path} no encontrado.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count_success = 0
    count_error = 0
    
    print(f"INFO: Actualizando {len(data)} registros en Supabase...")
    
    for item in data:
        ref = item.get('referencia')
        if not ref:
            continue
            
        try:
            # 1. Buscar el registro actual para obtener su ID
            existing = supabase_utils.supabase.table("inm_propiedades").select("id").eq("referencia", ref).execute()
            
            if existing.data:
                record_id = existing.data[0]['id']
                
                # 2. Actualizar por ID
                update_fields = {
                    "descripcion": item.get('descripcion'),
                    "imagenes_url": item.get('imagenes_url'),
                    "caracteristicas": item.get('caracteristicas')
                }
                
                res = supabase_utils.supabase.table("inm_propiedades").update(update_fields).eq("id", record_id).execute()
                if res.data:
                    count_success += 1
                else:
                    count_error += 1
            else:
                print(f"WARN: Referencia {ref} no encontrada en la base de datos.")
                count_error += 1
                
        except Exception as e:
            print(f"Error procesando {ref}: {e}")
            count_error += 1
            
    print(f"OK BATCH: {count_success} actualizados, {count_error} fallidos.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_properties_from_file(sys.argv[1])
    else:
        print("Uso: python scripts/update_batch_data.py [ruta_archivo_json]")
