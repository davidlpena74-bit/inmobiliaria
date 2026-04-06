import json
import os
from datetime import datetime

def export_to_idealista(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    idealista_properties = []

    for item in data:
        # Basic mapping
        # Note: Idealista expects specific values for many fields. 
        # This is an approximation based on V6 Common Specs.
        
        # Determine operation
        # If title contains 'en alquiler' or price has '/mes', it's rent.
        # Otherwise, assume sale for high values.
        operation = 'sale'
        price = item.get('precio', 0)
        if isinstance(price, str):
            if '/mes' in price or '€' in price:
                price = float(price.replace('€', '').replace('/mes', '').replace('.', '').replace(',', '').strip())
                if '/mes' in item.get('precio', ''):
                    operation = 'rent'
        
        # Property type mapping
        prop_type = 'homes' # Default
        tipo = item.get('tipo', '').lower()
        if 'apartamento' in tipo or 'piso' in tipo:
            prop_type = 'homes'
        elif 'chalet' in tipo or 'villa' in tipo:
            prop_type = 'homes'
        elif 'oficina' in tipo:
            prop_type = 'offices'
        
        # Address extraction (simple heuristic)
        titulo = item.get('titulo', '')
        street = ""
        if " en " in titulo:
            parts = titulo.split(" en ")
            if len(parts) > 1:
                street_part = parts[1].split(",")[0]
                street = street_part.strip()

        property_data = {
            "property_reference": item.get('referencia', item.get('ref', '')),
            "operation": operation,
            "property_type": prop_type,
            "address": {
                "street_name": street,
                "city": item.get('ciudad', 'Madrid'),
                "province": "Madrid",
                "zip_code": "", # Should be added if available
                "visibility": "full" # or 'area'
            },
            "prices": [
                {
                    "operation": operation,
                    "price": price,
                    "currency": "EUR"
                }
            ],
            "descriptions": [
                {
                    "language": "es",
                    "description": item.get('descripcion', item.get('title', ''))
                }
            ],
            "features": {
                "area": item.get('superficie', item.get('surface', 0)),
                "bedrooms": item.get('habitaciones', item.get('rooms', 0)),
                "bathrooms": item.get('banos', item.get('baths', 0)),
                "condition": "good" # Placeholder
            },
            "images": []
        }

        # Add images if available
        img = item.get('image', [])
        if isinstance(img, str):
            property_data["images"].append({"url": img, "label": "Principal"})
        elif isinstance(img, list):
            for i, url in enumerate(img):
                property_data["images"].append({"url": url, "label": f"Imagen {i+1}"})

        idealista_properties.append(property_data)

    feed = {
        "customer_code": "ilc8b226",
        "feed_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "properties": idealista_properties
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully exported {len(idealista_properties)} properties to {output_file}")

if __name__ == "__main__":
    # Prioritize 'datos_345_propiedades.json' as it has more details
    input_path = 'datos_345_propiedades.json'
    if not os.path.exists(input_path):
        input_path = 'data/inmoweb_properties.json'
        
    output_path = 'data/idealista_feed.json'
    
    if not os.path.exists('data'):
        os.makedirs('data')
        
    export_to_idealista(input_path, output_path)
