import supabase_utils
import config

# Datos de Madrid Capital (Extraídos de la lógica del dashboard)
distritos_capital = [
    {"nombre": "Salamanca", "precio_venta": 9968, "precio_alquiler": 28.5, "rentabilidad": 3.43, "ratio_recuperacion": 29.1, "variacion_1y": 14.8, "variacion_5y": 42.1, "variacion_10y": 85.4, "categoria": "Premium", "latitud": 40.4297, "longitud": -3.6797},
    {"nombre": "Chamberí", "precio_venta": 8873, "precio_alquiler": 24.2, "rentabilidad": 3.27, "ratio_recuperacion": 30.5, "variacion_1y": 12.5, "variacion_5y": 38.4, "variacion_10y": 78.2, "categoria": "Premium", "latitud": 40.4344, "longitud": -3.7038},
    {"nombre": "Chamartín", "precio_venta": 7971, "precio_alquiler": 22.8, "rentabilidad": 3.43, "ratio_recuperacion": 29.1, "variacion_1y": 15.2, "variacion_5y": 40.1, "variacion_10y": 80.5, "categoria": "Premium", "latitud": 40.462, "longitud": -3.676},
    {"nombre": "Retiro", "precio_venta": 7691, "precio_alquiler": 21.5, "rentabilidad": 3.35, "ratio_recuperacion": 29.8, "variacion_1y": 13.4, "variacion_5y": 35.2, "variacion_10y": 72.4, "categoria": "Premium", "latitud": 40.413, "longitud": -3.682},
    {"nombre": "Centro", "precio_venta": 7322, "precio_alquiler": 25.4, "rentabilidad": 4.16, "ratio_recuperacion": 24.0, "variacion_1y": 16.2, "variacion_5y": 45.8, "variacion_10y": 92.1, "categoria": "Premium", "latitud": 40.417, "longitud": -3.703},
    {"nombre": "Arganzuela", "precio_venta": 6203, "precio_alquiler": 19.5, "rentabilidad": 3.77, "ratio_recuperacion": 26.5, "variacion_1y": 11.2, "variacion_5y": 32.4, "variacion_10y": 65.4, "categoria": "Alto", "latitud": 40.401, "longitud": -3.696},
    {"nombre": "Ciudad Lineal", "precio_venta": 5010, "precio_alquiler": 16.8, "rentabilidad": 4.02, "ratio_recuperacion": 24.8, "variacion_1y": 10.5, "variacion_5y": 30.1, "variacion_10y": 60.2, "categoria": "Alto", "latitud": 40.448, "longitud": -3.650},
    {"nombre": "Vicálvaro", "precio_venta": 3965, "precio_alquiler": 18.5, "rentabilidad": 5.60, "ratio_recuperacion": 17.9, "variacion_1y": 25.4, "variacion_5y": 68.2, "variacion_10y": 124.5, "categoria": "Oportunidad", "latitud": 40.404, "longitud": -3.606},
    {"nombre": "Villa de Vallecas", "precio_venta": 3560, "precio_alquiler": 15.2, "rentabilidad": 5.12, "ratio_recuperacion": 19.5, "variacion_1y": 18.2, "variacion_5y": 52.4, "variacion_10y": 98.4, "categoria": "Asequible", "latitud": 40.375, "longitud": -3.626},
    {"nombre": "Puente de Vallecas", "precio_venta": 3287, "precio_alquiler": 16.4, "rentabilidad": 5.99, "ratio_recuperacion": 16.7, "variacion_1y": 21.5, "variacion_5y": 58.2, "variacion_10y": 110.1, "categoria": "Asequible", "latitud": 40.392, "longitud": -3.658},
    {"nombre": "Usera", "precio_venta": 3348, "precio_alquiler": 15.8, "rentabilidad": 5.66, "ratio_recuperacion": 17.7, "variacion_1y": 19.4, "variacion_5y": 54.1, "variacion_10y": 102.4, "categoria": "Asequible", "latitud": 40.383, "longitud": -3.706},
    {"nombre": "Villaverde", "precio_venta": 2823, "precio_alquiler": 14.5, "rentabilidad": 6.16, "ratio_recuperacion": 16.2, "variacion_1y": 22.7, "variacion_5y": 62.4, "variacion_10y": 115.2, "categoria": "Económico", "latitud": 40.350, "longitud": -3.712}
]

# Puedes añadir más municipios de la Comunidad aquí

def migrar():
    if not config.USAR_SUPABASE or config.SUPABASE_URL == "https://tu-proyecto.supabase.co":
        print("❌ Configura primero tus credenciales de Supabase en config.py")
        return

    print("🚀 Iniciando migración de datos a Supabase...")
    
    # Migrar distritos de la capital
    for d in distritos_capital:
        res = supabase_utils.upsert_municipio(d)
        if res:
            print(f"✅ Migrado: {d['nombre']}")
        else:
            print(f"❌ Error migrando: {d['nombre']}")

    print("\n✨ Migración completada.")

if __name__ == "__main__":
    migrar()
