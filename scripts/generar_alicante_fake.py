import json
import random
import os
from datetime import datetime

# CONFIGURACIÓN ALICANTE (Zonas de influencia Weperty)
ZONAS_ALICANTE = [
    {"barrio": "San Juan Playa", "rango_precio": (450000, 1200000), "m2_medio": 4500},
    {"barrio": "Alicante Centro", "rango_precio": (250000, 650000), "m2_medio": 3200},
    {"barrio": "Muchavista / Campello", "rango_precio": (350000, 950000), "m2_medio": 3800},
    {"barrio": "Cabo de las Huertas", "rango_precio": (600000, 2500000), "m2_medio": 5500},
    {"barrio": "Altea Hills", "rango_precio": (850000, 4500000), "m2_medio": 7000}
]

TITULOS = [
    "Villa de lujo con vistas panorámicas al mar",
    "Ático exclusivo en primera línea de playa",
    "Apartamento moderno recién reformado",
    "Chalet independiente con piscina privada",
    "Dúplex minimalista con gran terraza"
]

def generar_datos_fake(cantidad=100):
    propiedades = []
    
    for i in range(cantidad):
        zona = random.choice(ZONAS_ALICANTE)
        precio = random.randint(zona["rango_precio"][0], zona["rango_precio"][1])
        m2 = random.randint(70, 450)
        
        # Lógica de Oportunidad (algunos muy rebajados)
        es_oportunidad = random.random() < 0.15
        if es_oportunidad:
            precio = int(precio * 0.75) # 25% de descuento

        propiedad = {
            "id": i + 1,
            "titulo": f"{random.choice(TITULOS)} en {zona['barrio']}",
            "precio": precio,
            "precio_m2": round(precio / m2, 2),
            "m2": m2,
            "habitaciones": random.randint(1, 6),
            "baños": random.randint(1, 5),
            "zona": zona["barrio"],
            "ciudad": "Alicante",
            "tag": "FAKE_DATA" if not es_oportunidad else "OPORTUNIDAD_FAKE",
            "fecha_captura": datetime.now().isoformat(),
            "estado_interno": "DUMMY_FOR_REPLACEMENT",
            "destacada": random.random() < 0.2
        }
        propiedades.append(propiedad)
    
    output_path = 'data/alicante_initial_data.json'
    os.makedirs('data', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(propiedades, f, indent=4, ensure_ascii=False)
    
    print(f"📦 Generados {cantidad} anuncios de Alicante para Weperty (Marcados como FAKE)")
    return output_path

if __name__ == "__main__":
    generar_datos_fake()
