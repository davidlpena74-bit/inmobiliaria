"""
Script de Prueba del Agente de Precios
Busca precios de 5 municipios como ejemplo
"""

import asyncio
from agente_precios import PreciosInmobiliariosAgent

async def prueba_rapida():
    """Prueba rápida con 5 municipios"""
    print("🚀 Iniciando prueba del Agente de Precios Inmobiliarios")
    print("=" * 60)
    
    agente = PreciosInmobiliariosAgent()
    
    # Seleccionar solo 5 municipios para la prueba
    agente.municipios = [
        "Alcobendas",
        "Pozuelo-de-Alarcon",
        "Majadahonda",
        "Tres-Cantos",
        "Las-Rozas-de-Madrid"
    ]
    
    print(f"\n📍 Municipios a buscar: {len(agente.municipios)}")
    for i, mun in enumerate(agente.municipios, 1):
        print(f"  {i}. {mun.replace('-', ' ')}")
    
    print("\n⏳ Iniciando búsqueda... (esto puede tardar 1-2 minutos)\n")
    
    # Ejecutar búsqueda
    resultados = await agente.ejecutar_busqueda_completa()
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    if resultados:
        print(f"\n✅ Municipios con datos: {len(resultados)}")
        print("\nDetalles:")
        for r in resultados:
            print(f"\n  🏘️  {r['municipio']}")
            if r.get('precio_venta'):
                print(f"     💰 Venta: {r['precio_venta']:,.0f} €/m²")
            if r.get('precio_alquiler'):
                print(f"     🏠 Alquiler: {r['precio_alquiler']:,.1f} €/m²")
            print(f"     📡 Fuentes: {r.get('fuentes', 0)}")
    else:
        print("\n⚠️  No se encontraron datos")
    
    print("\n" + "=" * 60)
    print("✅ Prueba completada!")
    print("💾 Los datos han sido guardados en Supabase")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(prueba_rapida())
