import pandas as pd
from supabase_utils import SupabaseClient
import time
from datetime import datetime

import sys
import io

# Configurar salida UTF-8 para consola Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def calcular_y_actualizar_estadisticas():
    print("🔄 Iniciando cálculo de estadísticas agregadas...")
    client = SupabaseClient()
    
    # 1. Obtener todas las propiedades
    # Nota: Si son muchas, habría que paginar. Supabase limita a 1000 por defecto.
    # Aquí asumimos que por ahora caben o usamos rango amplio
    try:
        response = client.client.table("inm_propiedades").select("*").execute()
        props = response.data
        if not props:
            print("⚠️ No hay propiedades en la base de datos.")
            return

        df = pd.DataFrame(props)
        print(f"📊 Procesando {len(df)} propiedades...")
        
        # Limpieza básica
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
        df['superficie'] = pd.to_numeric(df['superficie'], errors='coerce')
        
        # Filtrar datos válidos
        df = df[df['precio'] > 0]
        df = df[df['superficie'] > 10] # Mínimo 10m2
        
        # Calcular precio/m2 si no existe
        if 'caracteristicas' in df.columns:
             # Extraer precio_m2 de json si es necesario, pero mejor calcularlo fresco
             pass
        
        df['precio_m2_calc'] = df['precio'] / df['superficie']
        
        # 2. Agrupar por zona (municipio/distrito)
        # Normalizar nombres de zona
        df['zona_norm'] = df['zona'].str.strip().str.title()
        
        stats = df.groupby('zona_norm').agg({
            'precio': 'mean',
            'precio_m2_calc': 'mean',
            'titulo': 'count', # Conteo de propiedades
            'habitaciones': 'mean',
            'superficie': 'mean'
        }).reset_index()
        
        stats.columns = ['zona', 'precio_medio', 'precio_m2', 'count', 'hab_media', 'm2_medio']
        
        # 3. Actualizar tabla inm_municipios
        print("\n💾 Actualizando tabla de municipios...")
        
        for index, row in stats.iterrows():
            nombre_zona = row['zona']
            
            # Mapeo de campos a la tabla inm_municipios
            # Asegurarse de que coinciden con el esquema de supabase
            datos_municipio = {
                "nombre": nombre_zona,
                "precio_venta": round(row['precio_m2'], 2), # El dashboard usa precio_venta como precio/m2
                "precio_alquiler": 0, # Pendiente de calcular si hay datos de alquiler
                "variacion_1y": 0, # Pendiente histórico
                "rentabilidad": 0, # Pendiente
                "ultima_actualizacion": datetime.now().isoformat(),
                "num_propiedades": int(row['count'])
            }
            
            # Upsert
            try:
                client.upsert_municipio(datos_municipio)
                print(f"   ✅ {nombre_zona}: {round(row['precio_m2'], 0)} €/m2 ({int(row['count'])} props)")
            except Exception as e:
                print(f"   ❌ Error actualizando {nombre_zona}: {e}")
                
        print("\n✨ Proceso de agregación completado.")

    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    calcular_y_actualizar_estadisticas()
