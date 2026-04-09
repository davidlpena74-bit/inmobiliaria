import json
import random
import os
from datetime import datetime

# CONFIGURACIÓN ALICANTE (Zonas de influencia Weperty)
ZONAS_ALICANTE = [
    # PREMIUM
    {"barrio": "Jávea / Xàbia", "rango_precio": (500000, 3500000), "m2_medio": 5500},
    {"barrio": "Altea Hills", "rango_precio": (850000, 4500000), "m2_medio": 7000},
    {"barrio": "Moraira", "rango_precio": (600000, 4000000), "m2_medio": 6000},
    {"barrio": "Benitachell / El Poble Nou de Benitatxell", "rango_precio": (400000, 2500000), "m2_medio": 4500},
    {"barrio": "Benissa", "rango_precio": (550000, 3800000), "m2_medio": 5200},
    {"barrio": "Cabo de las Huertas", "rango_precio": (600000, 2500000), "m2_medio": 5500},
    {"barrio": "San Juan Playa", "rango_precio": (450000, 1200000), "m2_medio": 4500},
    
    # MEDIUM
    {"barrio": "Dénia", "rango_precio": (200000, 1500000), "m2_medio": 2800},
    {"barrio": "Calpe / Calp", "rango_precio": (180000, 1800000), "m2_medio": 3200},
    {"barrio": "Alicante Centro", "rango_precio": (250000, 650000), "m2_medio": 3200},
    {"barrio": "Finestrat", "rango_precio": (300000, 2000000), "m2_medio": 3500},
    {"barrio": "Benidorm", "rango_precio": (150000, 2500000), "m2_medio": 3800},
    {"barrio": "Santa Pola", "rango_precio": (120000, 800000), "m2_medio": 2200},
    {"barrio": "Torrevieja", "rango_precio": (90000, 700000), "m2_medio": 1800},
    {"barrio": "L'Alfàs del Pi", "rango_precio": (220000, 1200000), "m2_medio": 2600},
    {"barrio": "La Nucia", "rango_precio": (200000, 950000), "m2_medio": 2400},
    {"barrio": "Muchavista / Campello", "rango_precio": (350000, 950000), "m2_medio": 3800},

    # ACCESS / INTERIOR
    {"barrio": "Pedreguer", "rango_precio": (120000, 600000), "m2_medio": 1600},
    {"barrio": "Polop", "rango_precio": (180000, 750000), "m2_medio": 1900},
    {"barrio": "Gata de Gorgos", "rango_precio": (100000, 500000), "m2_medio": 1400},
    {"barrio": "Xaló", "rango_precio": (150000, 800000), "m2_medio": 1700},
    {"barrio": "El Verger", "rango_precio": (130000, 550000), "m2_medio": 1800},
    {"barrio": "Orba", "rango_precio": (120000, 650000), "m2_medio": 1550},
    {"barrio": "Monforte del Cid", "rango_precio": (140000, 450000), "m2_medio": 1500},
    {"barrio": "Sella", "rango_precio": (90000, 400000), "m2_medio": 1200},
    {"barrio": "Benidoleig", "rango_precio": (110000, 550000), "m2_medio": 1500},
    {"barrio": "Pego", "rango_precio": (100000, 600000), "m2_medio": 1400}
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
            "tipo_operacion": "Alquiler" if precio < 10000 else "Venta",
            "estado_interno": "DUMMY_FOR_REPLACEMENT",
            "destacada": random.random() < 0.2
        }
        propiedades.append(propiedad)
    
    output_path = 'data/alicante_initial_data.json'
    os.makedirs('data', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(propiedades, f, indent=4, ensure_ascii=False)
    
    print(f"Generados {cantidad} anuncios de Alicante para Weperty (Marcados como FAKE)")
    return output_path

if __name__ == "__main__":
    generar_datos_fake()
