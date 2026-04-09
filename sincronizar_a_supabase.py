"""
sincronizar_a_supabase.py
========================
Sube los datos consolidados del scrapping a la base de datos Supabase
para que se refresquen los estados en el CRM.
"""

import json
import os
import config
from supabase import create_client, Client

def sincronizar():
    path_final = 'data/propiedades_final.json'

    if not os.path.exists(path_final):
        print(f"❌ No se encontró {path_final}. Ejecuta consolidar_propiedades.py primero.")
        return

    # Iniciar cliente Supabase
    url: str = config.SUPABASE_URL
    key: str = config.SUPABASE_KEY
    supabase: Client = create_client(url, key)

    print("☁️ Conectando a Supabase...")

    # Cargar datos
    with open(path_final, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"🔄 Sincronizando {len(data)} inmuebles...")

    for prop in data:
        ref = prop.get('ref')
        if not ref:
            continue

        # Actualizar el campo 'publicado_weperti_com' en Supabase
        # Nota: Asegúrate de que la columna exista en la tabla 'inm_propiedades'
        try:
            # Primero intentamos actualizar si existe
            res = supabase.table('inm_propiedades').update({
                "publicado_weperti_com": prop.get('esta_publicado', False)
            }).eq('referencia', ref).execute()
            
            if len(res.data) == 0:
                print(f"⚠️ Referencia {ref} no encontrada en Supabase. Saltando...")
            else:
                print(f"✅ Ref {ref}: Publicado={prop.get('esta_publicado')}")
        
        except Exception as e:
            print(f"❌ Error sincronizando Ref {ref}: {e}")

    print("🏁 Sincronización completada.")

if __name__ == "__main__":
    sincronizar()
