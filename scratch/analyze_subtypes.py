import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.getcwd())

import config
from supabase_utils import SupabaseClient

def analyze_subtypes():
    client = SupabaseClient()
    try:
        res = client.client.table("inm_propiedades").select("id, referencia, titulo, descripcion, tipo, caracteristicas").execute()
        props = res.data
        
        counts = {
            "Pisos": 0,
            "Áticos": 0,
            "Dúplex": 0,
            "Independientes": 0,
            "Pareados": 0,
            "Adosados": 0,
            "Casas rústicas": 0
        }
        
        for p in props:
            text = f"{p.get('titulo', '')} {p.get('descripcion', '')} {p.get('tipo', '')}".lower()
            
            # Pisos
            if "piso" in text or "apartamento" in text:
                counts["Pisos"] += 1
            
            # Áticos
            if "ático" in text or "atico" in text or "penthouse" in text:
                counts["Áticos"] += 1
            
            # Dúplex
            if "dúplex" in text or "duplex" in text:
                counts["Dúplex"] += 1
            
            # Casas y chalets
            if "independiente" in text or "villa" in text:
                counts["Independientes"] += 1
            
            if "pareado" in text or "semi-detached" in text:
                counts["Pareados"] += 1
            
            if "adosado" in text or "townhouse" in text or "terraced" in text:
                counts["Adosados"] += 1
            
            if "rústica" in text or "rustica" in text or "finca" in text or "cortijo" in text:
                counts["Casas rústicas"] += 1

        print(f"Análisis de subtipos (basado en palabras clave):")
        for k, v in counts.items():
            print(f"- {k}: {v}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_subtypes()
