import json
import os
import re
from idealista_api_client import IdealistaAPIClient

def extract_street(titulo):
    """Simple heuristic to extract the street from the title."""
    # Example: "Piso en Calle de Villajoyosa, Valdebernardo" -> "Calle de Villajoyosa"
    match = re.search(r' en (.+?),', titulo)
    if match:
        return match.group(1).strip()
    return titulo # Fallback

def map_to_idealista_api(item, contact_id=12345):
    """Maps an internal property item to the Idealista API schema."""
    
    # Determine typology
    tipo_map = {
        "Apartamento": "flat",
        "Piso": "flat",
        "Chalet": "house",
        "Villa": "house",
        "Oficina": "office",
        "Local": "commercial"
    }
    typology = tipo_map.get(item.get('tipo', 'Apartamento'), "flat")

    # Construct the API payload
    property_data = {
        "operation": {
            "type": "sale", # Defaulting to sale based on current data
            "price": item.get('precio', 0)
        },
        "type": typology,
        "address": {
            "streetName": extract_street(item.get('titulo', '')),
            "streetNumber": "", # We don't have exact numbers in this JSON, will need them for 'Exact' visibility
            "postalCode": "28032", # Defaulting to Vicálvaro/Madrid if missing
            "city": item.get('ciudad', 'Madrid'),
            "province": "Madrid",
            "country": "es"
        },
        "features": {
            "areaConstructed": item.get('superficie', 0),
            "bedroomNumber": item.get('habitaciones', 0),
            "bathroomNumber": item.get('banos', 1)
        },
        "descriptions": [
            {
                "language": "es",
                "description": item.get('descripcion', item.get('titulo', ''))
            }
        ],
        "contactId": contact_id # Mandatory field in API
    }
    
    return property_data

def sync_batch(input_file, limit=5):
    """Reads internal data and syncs a batch to the API (Sandbox)."""
    if not os.path.exists(input_file):
        print(f"File {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        properties = json.load(f)

    # Note: Use real credentials when received
    CLIENT_ID = "testDocu"
    CLIENT_SECRET = "dc4haw4JmASg2CZG"
    FEED_KEY = "ilc8b226" # Placeholder
    
    client = IdealistaAPIClient(CLIENT_ID, CLIENT_SECRET, FEED_KEY, sandbox=True)
    
    # Only try to authenticate if we want to run the real sync
    # For now, we just prepare the mapping log
    print(f"--- Preparing to sync {min(len(properties), limit)} properties ---")
    
    for i, item in enumerate(properties[:limit]):
        api_payload = map_to_idealista_api(item)
        ref = item.get('referencia', f'PROP-{i}')
        
        print(f"Mapping [{ref}]: {item.get('titulo')}")
        # print(json.dumps(api_payload, indent=2, ensure_ascii=False))
        
        # client.publish_property(api_payload)
        # print(f"Successfully sent {ref}")

    print("\nMapping verification complete. Ready for real API SECRET.")

if __name__ == "__main__":
    sync_batch('datos_345_propiedades.json', limit=3)
