import json
import os
import re
import sys

# Añadir el directorio raíz al path para importar supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import supabase_utils

def clean_numeric(value):
    """Limpia cadenas como '2.350€/mes' o '126.000€' y devuelve un número"""
    if not value or value == "-":
        return 0
    # Eliminar todo lo que no sea dígito
    clean_val = re.sub(r'[^\d]', '', str(value))
    return int(clean_val) if clean_val else 0

def extract_municipality(location):
    """Extrae el municipio de una cadena como 'Calle 123, Torrevieja'"""
    if not location:
        return "Alicante" # Default por si acaso
    parts = location.split(',')
    if len(parts) > 1:
        return parts[-1].strip()
    return location.strip()

def process_and_import(input_file='data/inmoweb_properties.json', use_supabase=True):
    if not os.path.exists(input_file):
        print(f"❌ Archivo no encontrado: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    print(f"INFO: Procesando {len(raw_data)} inmuebles...")
    
    count_success = 0
    count_error = 0
    
    for item in raw_data:
        # Extraer tipo de propiedad del título
        titulo = item.get('title', '')
        tipo = "Apartamento"
        if "Villa" in titulo or "Lujo" in titulo: tipo = "Villa"
        elif "Casa" in titulo: tipo = "Casa / Chalet"
        elif "Bungalow" in titulo: tipo = "Bungalow"
        elif "Dúplex" in titulo: tipo = "Dúplex"
        elif "Ático" in titulo: tipo = "Ático"
        
        municipio = extract_municipality(item.get('location'))
        
        # Mapeo de estado
        status_map = {
            "Activo": "Activo",
            "Reservado": "Pausado",
            "Vendido": "Vendido",
            "Alquilado": "Alquilado"
        }
        
        # Construir objeto para Weperty Supabase
        # 'url' es requerido según el schema para evitar duplicados en upsert
        target_item = {
            "referencia": item.get('ref'),
            "titulo": item.get('title'),
            "tipo": tipo,
            "precio": clean_numeric(item.get('price')),
            "habitaciones": int(item.get('rooms', 0)) if item.get('rooms') else 0,
            "banos": int(item.get('baths', 0)) if item.get('baths') else 0,
            "superficie": clean_numeric(item.get('surface')),
            "zona": municipio, # Aquí guardamos el municipio para que insert_propiedad lo use
            "url": f"https://weperty.com/inmueble/{item.get('ref', 'unknown')}", # Placeholder URL
            "imagenes_url": [item.get('image')],
            "estado_publicacion": status_map.get(item.get('status'), "Activo"),
            "origen_datos": "CRM_WEPERTY",
            "publicar_web": True,
            "agente": "Weperty Properties"
        }
        
        if use_supabase:
            res = supabase_utils.insert_propiedad(target_item)
            if res:
                count_success += 1
            else:
                count_error += 1
        else:
            count_success += 1
            
    print(f"OK: Finalizado.")
    print(f"RESUMEN: {count_success} subidos, {count_error} errores.")

if __name__ == "__main__":
    process_and_import()
