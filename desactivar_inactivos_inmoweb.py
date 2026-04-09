"""
desactivar_inactivos_inmoweb.py
==============================
Ejecuta la desactivación selectiva en Supabase basada en el escaneo real realizado.
"""

import config
from supabase import create_client, Client

def ejecutar_desactivacion():
    # Lista de referencias detectadas como INACTIVAS en Inmoweb
    refs_inactivas = [
        "AJLJELNE",
        "ATTTRRR20",
        "ALQPNMYP",
        "ALQUEH2200",
        "AAUWH900A",
        "LUX0070"
    ]

    # Iniciar cliente Supabase
    url: str = config.SUPABASE_URL
    key: str = config.SUPABASE_KEY
    supabase: Client = create_client(url, key)

    print(f"Sincronizando desactivación de {len(refs_inactivas)} inmuebles...")

    # 1. Desactivar los detectados como inactivos
    for ref in refs_inactivas:
        try:
            res = supabase.table('inm_propiedades').update({
                "publicar_web": False
            }).eq('referencia', ref).execute()
            
            if len(res.data) > 0:
                print(f"OK: Ref {ref} desactivada correctamente.")
            else:
                print(f"Info: Ref {ref} no encontrada en Supabase (posiblemente borrada).")
        except Exception as e:
            print(f"Error con Ref {ref}: {e}")

    # 2. Opcional: Asegurar que el resto estén activos? 
    # Por ahora solo cumplimos la orden directa de desactivar los inactivos detectados.
    
    print("\nProceso finalizado.")

if __name__ == "__main__":
    ejecutar_desactivacion()
