"""
Generador de datos de ejemplo para demostración
Basado en precios reales del mercado de Vicálvaro, Madrid
"""

import pandas as pd
import random
from datetime import datetime

def generar_datos_vicalvaro():
    """
    Genera datos de ejemplo realistas para pisos en Vicálvaro
    Basado en rangos de precios reales del mercado (2026)
    """
    
    # Datos realistas de Vicálvaro
    calles = [
        "Calle de Villajoyosa",
        "Calle de San Cipriano",
        "Avenida de Daroca",
        "Calle de Valdebernardo",
        "Calle de Arcentales",
        "Calle de Pico de Artilleros",
        "Calle de Sierra Carbonera",
        "Avenida de la Institución Libre de Enseñanza",
        "Calle de Valdeolea",
        "Calle de Villablanca"
    ]
    
    propiedades = []
    
    # Generar 30 propiedades de ejemplo
    for i in range(30):
        # Características aleatorias pero realistas
        habitaciones = random.choice([1, 2, 2, 3, 3, 3, 4])
        banos = random.choice([1, 1, 2, 2, 3])
        superficie = random.randint(45, 120)
        
        # Precio base según m² (Vicálvaro: 2,500-3,500 €/m²)
        precio_m2_base = random.uniform(2500, 3500)
        precio = int(superficie * precio_m2_base)
        
        # Redondear precio a miles
        precio = round(precio / 1000) * 1000
        
        calle = random.choice(calles)
        numero = random.randint(1, 150)
        planta = random.choice(["Bajo", "1ª", "2ª", "3ª", "4ª", "5ª", "6ª"])
        
        descripciones = [
            "Piso en buen estado, exterior, muy luminoso",
            "Vivienda reformada, cocina equipada",
            "Piso para entrar a vivir, ascensor",
            "Vivienda amplia, plaza de garaje incluida",
            "Piso exterior, buenas vistas, ascensor",
            "Vivienda reformada, calefacción central",
            "Piso luminoso, terraza, trastero",
            "Vivienda en zona tranquila, bien comunicada"
        ]
        
        ref = f"WPT-{random.randint(10000, 99999)}"
        
        propiedad = {
            'referencia': ref,
            'titulo': f"Piso en {calle}, Vicálvaro",
            'tipo': 'Apartamento',
            'precio': precio,
            'superficie': superficie,
            'precio_m2': round(precio / superficie, 2),
            'habitaciones': habitaciones,
            'banos': banos,
            'detalles': f"{habitaciones} hab., {banos} baños, {superficie} m², Planta {planta}",
            'descripcion': random.choice(descripciones),
            'url': f"https://www.idealista.com/inmueble/{random.randint(10000000, 99999999)}/",
            'zona': 'Vicálvaro',
            'ciudad': 'Madrid',
            'fecha_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'publicar_web': True
        }
        
        propiedades.append(propiedad)
    
    # Crear DataFrame
    df = pd.DataFrame(propiedades)
    
    # Ordenar por precio
    df = df.sort_values('precio').reset_index(drop=True)
    
    return df


if __name__ == "__main__":
    # Generar datos
    df = generar_datos_vicalvaro()
    
    # Guardar en CSV
    df.to_csv('datos_vicalvaro_ejemplo.csv', index=False, encoding='utf-8-sig')
    
    # Mostrar estadísticas
    print(f"\n{'='*60}")
    print(f"📊 DATOS DE EJEMPLO GENERADOS - VICÁLVARO")
    print(f"{'='*60}")
    print(f"Total propiedades: {len(df)}")
    print(f"Precio medio: {df['precio'].mean():,.0f} €")
    print(f"Precio mínimo: {df['precio'].min():,.0f} €")
    print(f"Precio máximo: {df['precio'].max():,.0f} €")
    print(f"Precio/m² medio: {df['precio_m2'].mean():,.2f} €/m²")
    print(f"m² medio: {df['superficie'].mean():.0f} m²")
    print(f"\n💾 Archivo guardado: datos_vicalvaro_ejemplo.csv")
    print(f"{'='*60}\n")
    
    # Mostrar muestra
    print("📋 MUESTRA DE DATOS (primeras 5 propiedades):\n")
    print(df[['titulo', 'precio', 'superficie', 'precio_m2', 'habitaciones', 'banos']].head(5).to_string(index=False))
