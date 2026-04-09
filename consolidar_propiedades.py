"""
consolidar_propiedades.py
========================
Combina los datos extraídos de Inmoweb (CRM) y Weperti (Web pública).
Marca los inmuebles que están efectivamente publicados en weperti.com.
"""

import json
import os

def consolidar():
    inmoweb_file = 'data/inmuebles_registrados.json' # He visto que el CRM usa este nombre a veces, pero mi script genera 'inmoweb_properties.json'
    # Ajustamos a los nombres de mis scripts
    path_inmoweb = 'data/inmoweb_properties.json'
    path_weperti = 'data/weperti_published.json'
    path_final = 'data/propiedades_final.json'

    if not os.path.exists(path_inmoweb):
        print(f"❌ No se encontró {path_inmoweb}. Ejecuta Scrapper_Inmoweb.py primero.")
        return

    # Cargar datos de Inmoweb (CRM - Fuente de verdad de todos los inmuebles)
    with open(path_inmoweb, 'r', encoding='utf-8') as f:
        inmoweb_data = json.load(f)

    # Cargar datos de Weperti (Web pública - Fuente de qué está publicado)
    weperti_refs = set()
    if os.path.exists(path_weperti):
        with open(path_weperti, 'r', encoding='utf-8') as f:
            weperti_data = json.load(f)
            weperti_refs = {item['ref'] for item in weperti_data}
        print(f"✅ Cargadas {len(weperti_refs)} referencias publicadas en Weperti.")
    else:
        print(f"⚠️ No se encontró {path_weperti}. Se asumirá que nada está publicado.")

    # Consolidar
    consolidado = []
    for prop in inmoweb_data:
        # Normalizar referencia para asegurar que el match funciona
        ref = prop.get('ref', '').strip()
        
        # El match principal: ¿Está la referencia de Inmoweb en la lista de Weperti?
        esta_publicado = ref in weperti_refs
        
        prop['esta_publicado'] = esta_publicado
        consolidado.append(prop)

    # Guardar resultado final
    os.makedirs('data', exist_ok=True)
    with open(path_final, 'w', encoding='utf-8') as f:
        json.dump(consolidado, f, indent=2, ensure_ascii=False)
    
    print(f"🏁 Consolidación completada. {len(consolidado)} inmuebles procesados.")
    print(f"📊 Publicados: {sum(1 for p in consolidado if p['esta_publicado'])}")
    print(f"💾 Resultado guardado en {path_final}")

if __name__ == "__main__":
    consolidar()
