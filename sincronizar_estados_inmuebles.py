"""
sincronizar_estados_inmoweb.py
==============================
Sincroniza el estado de publicación "Mi web" de Inmoweb con el campo 'publicar_web' de Supabase.
Si un inmueble no está marcado como publicado en Inmoweb, se desactivará en el CRM propio.
"""

import json
import os
import config
from supabase import create_client, Client

def sincronizar():
    path_sync = 'data/inmoweb_full_sync.json'

    if not os.path.exists(path_sync):
        print("Error: No se encontro " + path_sync + ". Ejecuta Scrapper_Inmoweb.py primero.")
        return

    # Iniciar cliente Supabase
    url: str = config.SUPABASE_URL
    key: str = config.SUPABASE_KEY
    supabase: Client = create_client(url, key)

    print("Conectando a Supabase para sincronizar estados...")

    # Cargar datos del scraper
    with open(path_sync, 'r', encoding='utf-8') as f:
        inmoweb_data = json.load(f)

    print("Procesando " + str(len(inmoweb_data)) + " inmuebles desde Inmoweb...")

    actualizados = 0
    desactivados = 0

    for item in inmoweb_data:
        ref = item.get('ref')
        esta_activo_inmoweb = item.get('publicado_web', False)

        if not ref:
            continue

        try:
            # Actualizar el campo 'publicar_web' en Supabase basado en el estado de Inmoweb
            res = supabase.table('inm_propiedades').update({
                "publicar_web": esta_activo_inmoweb
            }).eq('referencia', ref).execute()
            
            if len(res.data) > 0:
                actualizados += 1
                if not esta_activo_inmoweb:
                    desactivados += 1
                    print("Ref " + ref + ": Desactivado (no activo en Inmoweb)")
            
        except Exception as e:
            print("Error sincronizando Ref " + ref + ": " + str(e))

    print("\nSincronizacion completada.")
    print("Total procesados: " + str(len(inmoweb_data)))
    print("Supabase actualizados: " + str(actualizados))
    print("Inmuebles desactivados: " + str(desactivados))

if __name__ == "__main__":
    sincronizar()
