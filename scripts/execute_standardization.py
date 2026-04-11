import os
import sys
import json

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
import config

def execute_update():
    # Supabase setup
    url = config.SUPABASE_URL
    key = config.SUPABASE_KEY
    supabase = create_client(url, key)

    # Load all batches
    batches = [
        'scratch/translations_batch_1.json',
        'scratch/translations_batch_2.json',
        'scratch/translations_batch_3.json',
        'scratch/translations_batch_4.json'
    ]

    all_updates = []
    for batch_path in batches:
        if os.path.exists(batch_path):
            with open(batch_path, 'r', encoding='utf-8') as f:
                all_updates.extend(json.load(f))
        else:
            print(f"Warning: Batch {batch_path} not found.")

    print(f"Total properties to update: {len(all_updates)}")

    success_count = 0
    error_count = 0

    for item in all_updates:
        prop_id = item['id']
        
        # Get current state to preserve other translation keys if they exist
        try:
            current_res = supabase.table('inm_propiedades').select('traducciones').eq('id', prop_id).execute()
            current_trads = {}
            if current_res.data:
                current_trads = current_res.data[0].get('traducciones') or {}
            
            # Update/Create entries for EN, DE, NL
            new_trads = current_trads.copy()
            
            new_trads['en'] = {
                "titulo": item['titulo_en'],
                "descripcion": item['descripcion_en']
            }
            new_trads['de'] = {
                "titulo": item.get('titulo_de', item['titulo_en']), # Fallback to EN title for DE/NL if not provided
                "descripcion": item['descripcion_de']
            }
            new_trads['nl'] = {
                "titulo": item.get('titulo_nl', item['titulo_en']),
                "descripcion": item['descripcion_nl']
            }

            # Prepare update data
            update_data = {
                "descripcion": item['descripcion_es'],
                "titulo": item['titulo_es'],
                "traducciones": new_trads
            }

            # Execute update
            res = supabase.table('inm_propiedades').update(update_data).eq('id', prop_id).execute()
            
            if res.data:
                success_count += 1
                print(f"Successfully updated ID {prop_id}")
            else:
                error_count += 1
                print(f"Failed to update ID {prop_id}")

        except Exception as e:
            error_count += 1
            print(f"Error updating ID {prop_id}: {str(e)}")

    print(f"\nStandardization complete.")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    execute_update()
