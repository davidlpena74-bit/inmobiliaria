import pandas as pd
import os
import json
from supabase import create_client, Client

# Configuración
CSV_PATH = r"C:\Users\david\Desktop\backup_propiedad_1939_7737_6786606 (1).csv"
SB_URL = "https://dwbvegnxmyvpolvofkfn.supabase.co"
SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3YnZlZ254bXl2cG9sdm9ma2ZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc1Mzg1NTUsImV4cCI6MjA4MzExNDU1NX0.eT5ZSce8H8Yk8pWKyLUYChU0HtmZljywP4eEQd5FkOI"

supabase: Client = create_client(SB_URL, SB_KEY)
TBL_PROPIEDADES = "inm_propiedades"

def migrar_datos():
    print(f"Buscando archivo en: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        print("Error: No se encontro el archivo de backup.")
        return

    # Leer CSV
    try:
        df = pd.read_csv(CSV_PATH)
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding='latin-1')
        
    print(f"Leidos {len(df)} inmuebles del backup.")

    # 1. Limpiar datos antiguos (opcional pero recomendado)
    print("Limpiando base de datos de muestras...")
    try:
        # Intentamos borrar todo (ID > 0 borra todo en Supabase)
        supabase.table(TBL_PROPIEDADES).delete().neq("id", 0).execute()
        print("Base de datos limpia.")
    except Exception as e:
        print(f"Advertencia al limpiar: {e}")

    # 2. Procesar Columnas de Imagenes
    img_cols = [c for c in df.columns if 'multimedia-images-public-' in c and c.endswith('-url')]
    
    propiedades_batch = []
    
    for _, row in df.iterrows():
        # Recolectar imagenes
        imagenes = []
        for col in img_cols:
            if pd.notna(row[col]) and str(row[col]).startswith('http'):
                imagenes.append(str(row[col]))

        # Mapeo de datos
        prop = {
            "referencia": str(row.get('reference', '')),
            "titulo": str(row.get('description-0-es-short', 'Propiedad Weperty')),
            "tipo": str(row.get('type-name', 'Inmueble')),
            "precio": float(row.get('price', 0)) if pd.notna(row.get('price')) else 0,
            "habitaciones": int(row.get('bed', 0)) if pd.notna(row.get('bed')) else 0,
            "banos": int(row.get('bath', 0)) if pd.notna(row.get('bath')) else 0,
            "superficie": float(row.get('surface_area-built', 0)) if pd.notna(row.get('surface_area-built')) else 0,
            "zona": str(row.get('location-zone', '')),
            "descripcion": str(row.get('description-0-es-large', '')),
            "latitud": float(row.get('location-coordinate-latitude', 0)) if pd.notna(row.get('location-coordinate-latitude')) else 38.36,
            "longitud": float(row.get('location-coordinate-longitude', 0)) if pd.notna(row.get('location-coordinate-longitude')) else -0.45,
            "publicar_web": bool(row.get('publication-web', 0)),
            "imagenes_url": imagenes,
            "caracteristicas": {
                "ciudad": str(row.get('location-city-name', '')),
                "cod_postal": str(row.get('location-postal_code', '')),
                "pais": str(row.get('location-country-name', 'España'))
            },
            "origen_datos": "CRM_WEPERTY",
            "estado_publicacion": "Activo"
        }
        
        propiedades_batch.append(prop)

        # Insertar en bloques para evitar fallos de red
        if len(propiedades_batch) >= 20:
            try:
                supabase.table(TBL_PROPIEDADES).insert(propiedades_batch).execute()
                print(f"Insertadas {len(propiedades_batch)} propiedades...")
                propiedades_batch = []
            except Exception as e:
                print(f"Error al insertar bloque: {e}")
                propiedades_batch = []

    # Insertar resto
    if propiedades_batch:
        try:
            supabase.table(TBL_PROPIEDADES).insert(propiedades_batch).execute()
            print(f"Finalizado. Insertadas {len(propiedades_batch)} propiedades finales.")
        except Exception as e:
            print(f"Error al insertar bloque final: {e}")

if __name__ == "__main__":
    migrar_datos()
