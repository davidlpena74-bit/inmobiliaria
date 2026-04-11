import os
import json
from supabase import create_client, Client
import config

# Inicializar cliente de Supabase
supabase_url = config.SUPABASE_URL
supabase_key = config.SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

TBL_PROPIEDADES = "inm_propiedades"

def update_descriptions():
    descriptions = {}
    
    # Cargar todos los batches
    for i in range(1, 5):
        batch_file = f"scratch/descriptions_batch_{i}.json"
        if os.path.exists(batch_file):
            with open(batch_file, "r", encoding="utf-8") as f:
                batch_data = json.load(f)
                descriptions.update(batch_data)
    
    print(f"Total de descripciones cargadas: {len(descriptions)}")
    
    success_count = 0
    error_count = 0
    
    for prop_id, desc in descriptions.items():
        try:
            print(f"Actualizando propiedad {prop_id}...")
            response = supabase.table(TBL_PROPIEDADES).update({"descripcion": desc}).eq("id", prop_id).execute()
            if response.data:
                success_count += 1
            else:
                print(f"⚠️ No se encontró la propiedad {prop_id} o no hubo cambios.")
                error_count += 1
        except Exception as e:
            print(f"❌ Error actualizando propiedad {prop_id}: {e}")
            error_count += 1
            
    print(f"\nResumen de actualización:")
    print(f"Exitos: {success_count}")
    print(f"Errores: {error_count}")

if __name__ == "__main__":
    update_descriptions()
