"""
Agente Especializado en Búsqueda de Precios Inmobiliarios
Comunidad de Madrid - Todos los Municipios

Este agente automatiza la recopilación de datos inmobiliarios de múltiples fuentes
y actualiza la base de datos de Supabase con información real y actualizada.
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import json
from datetime import datetime
from supabase_utils import SupabaseClient
import time
import config

class PreciosInmobiliariosAgent:
    """
    Agente inteligente para buscar precios inmobiliarios en la Comunidad de Madrid
    """
    
    def __init__(self):
        self.supabase = SupabaseClient()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Lista completa de municipios de la Comunidad de Madrid
        self.municipios = self._cargar_municipios()
        
    def _get_proxy_url(self) -> Optional[str]:
        """Genera una URL de proxy con sesión rotativa"""
        if not config.USAR_PROXY:
            return None
            
        session_id = random.randint(100000, 999999)
        # Usar PROXY_USER_BASE si existe, si no user normal
        user_base = getattr(config, 'PROXY_USER_BASE', config.PROXY_USER)
        proxy_user = f"{user_base}__country-es__session-{session_id}"
        
        return f"http://{proxy_user}:{config.PROXY_PASS}@{config.PROXY_HOST}:{config.PROXY_PORT}"

    def _cargar_municipios(self) -> List[str]:
        """Carga la lista completa de municipios de la Comunidad de Madrid"""
        return [
            # Madrid Capital (21 distritos)
            "Madrid-Salamanca", "Madrid-Chamberi", "Madrid-Chamartin", "Madrid-Retiro",
            "Madrid-Centro", "Madrid-Arganzuela", "Madrid-Vicalvaro", "Madrid-Villaverde",
            "Madrid-Puente-de-Vallecas", "Madrid-Usera", "Madrid-Villa-de-Vallecas",
            "Madrid-Ciudad-Lineal", "Madrid-Moncloa-Aravaca", "Madrid-Tetuan",
            "Madrid-Hortaleza", "Madrid-Fuencarral-El-Pardo", "Madrid-Moratalaz",
            "Madrid-Latina", "Madrid-Carabanchel", "Madrid-San-Blas-Canillejas", "Madrid-Barajas",
            
            # Zona Norte
            "Alcobendas", "San-Sebastian-de-los-Reyes", "Tres-Cantos", "Colmenar-Viejo",
            "San-Agustin-del-Guadalix", "Algete", "Paracuellos-de-Jarama", "Cobeña",
            "Daganzo-de-Arriba", "Ajalvir", "Torrejon-de-Ardoz", "Alcala-de-Henares",
            "Meco", "Camarma-de-Esteruelas", "Torres-de-la-Alameda", "Loeches",
            "Mejorada-del-Campo", "Velilla-de-San-Antonio", "San-Fernando-de-Henares",
            "Coslada", "Rivas-Vaciamadrid", "Arganda-del-Rey", "Campo-Real",
            
            # Zona Oeste
            "Pozuelo-de-Alarcon", "Majadahonda", "Las-Rozas-de-Madrid", "Boadilla-del-Monte",
            "Villanueva-de-la-Cañada", "Villaviciosa-de-Odon", "Brunete", "Villanueva-del-Pardillo",
            "Torrelodones", "Galapagar", "Collado-Villalba", "Alpedrete", "Moralzarzal",
            "Cercedilla", "Navacerrada", "Los-Molinos", "Guadarrama", "El-Escorial",
            "San-Lorenzo-de-El-Escorial", "Valdemorillo", "Navalagamella", "Quijorna",
            "Villanueva-de-Perales", "Sevilla-la-Nueva", "Navalcarnero", "Arroyomolinos",
            "Mostoles", "Fuenlabrada", "Leganes", "Getafe", "Pinto", "Valdemoro",
            "Parla", "Humanes-de-Madrid", "Griñon", "Torrejon-de-la-Calzada",
            "Torrejon-de-Velasco", "Cubas-de-la-Sagra", "Batres", "Serranillos-del-Valle",
            
            # Zona Sur
            "Alcorcon", "San-Martin-de-la-Vega", "Ciempozuelos", "Titulcia",
            "Chinchon", "Colmenar-de-Oreja", "Belmonte-de-Tajo", "Villarejo-de-Salvanes",
            "Aranjuez", "Valdelaguna", "Morata-de-Tajuña", "Perales-de-Tajuña",
            
            # Zona Este
            "Coslada", "San-Fernando-de-Henares", "Torrejon-de-Ardoz", "Alcala-de-Henares",
            "Meco", "Azuqueca-de-Henares", "Los-Santos-de-la-Humosa", "Anchuelo",
            "Santorcaz", "Nuevo-Baztan", "Villar-del-Olmo", "Ambite", "Orusco",
            
            # Sierra Norte
            "Manzanares-el-Real", "Soto-del-Real", "Guadalix-de-la-Sierra",
            "El-Molar", "Pedrezuela", "Talamanca-de-Jarama", "El-Vellón",
            "Torrelaguna", "Patones", "Torremocha-de-Jarama", "El-Berrueco",
            "Cervera-de-Buitrago", "Gascones", "Garganta-de-los-Montes",
            "Gargantilla-del-Lozoya", "Lozoya", "Pinilla-del-Valle", "Rascafria",
            "Alameda-del-Valle", "Buitrago-del-Lozoya", "Somosierra", "La-Acebeda",
            "Montejo-de-la-Sierra", "Puebla-de-la-Sierra", "Prádena-del-Rincón",
            "La-Hiruela", "Horcajuelo-de-la-Sierra", "Robledillo-de-la-Jara",
            
            # Otros municipios importantes
            "Villa-del-Prado", "Aldea-del-Fresno", "Casarrubuelos", "Cubas",
            "Moraleja-de-Enmedio", "El-Alamo", "Batres", "Torrejón-de-Velasco"
        ]

    # ... (resto de _cargar_municipios)

    async def buscar_precio_idealista(self, municipio: str, session: aiohttp.ClientSession) -> Optional[Dict]:
        """
        Busca precios en Idealista para un municipio específico
        """
        try:
            # Normalizar nombre del municipio para URL
            municipio_url = municipio.lower().replace(' ', '-').replace('_', '-')
            
            # URLs de búsqueda
            url_venta = f"https://www.idealista.com/venta-viviendas/{municipio_url}-madrid/"
            url_alquiler = f"https://www.idealista.com/alquiler-viviendas/{municipio_url}-madrid/"
            
            # Obtener proxy rotado
            proxy = self._get_proxy_url()
            if proxy:
                print(f"🌍 Usando proxy rotativo para {municipio}")
            
            # Buscar precio de venta
            async with session.get(url_venta, headers=self.headers, proxy=proxy) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extraer precio medio de venta
                    precio_venta = self._extraer_precio_medio(soup)
                    
            # Esperar un poco para no saturar el servidor
            await asyncio.sleep(random.uniform(1, 3))
            
            # Buscar precio de alquiler
            async with session.get(url_alquiler, headers=self.headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extraer precio medio de alquiler
                    precio_alquiler = self._extraer_precio_alquiler(soup)
            
            if precio_venta or precio_alquiler:
                return {
                    'municipio': municipio,
                    'precio_venta': precio_venta,
                    'precio_alquiler': precio_alquiler,
                    'fuente': 'Idealista',
                    'fecha': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Error buscando {municipio} en Idealista: {str(e)}")
            
        return None
    
    def _extraer_precio_medio(self, soup: BeautifulSoup) -> Optional[float]:
        """Extrae el precio medio de venta de la página"""
        try:
            # Buscar en diferentes selectores posibles
            selectores = [
                '.avg-price',
                '.price-tag',
                '[data-test="price-average"]',
                '.item-price',
                '.price-row'
            ]
            
            for selector in selectores:
                elemento = soup.select_one(selector)
                if elemento:
                    texto = elemento.get_text()
                    # Extraer número del texto
                    precio = ''.join(filter(str.isdigit, texto))
                    if precio:
                        return float(precio)
                        
        except Exception as e:
            print(f"Error extrayendo precio: {e}")
            
        return None
    
    def _extraer_precio_alquiler(self, soup: BeautifulSoup) -> Optional[float]:
        """Extrae el precio medio de alquiler de la página"""
        return self._extraer_precio_medio(soup)
    
    async def buscar_precio_fotocasa(self, municipio: str, session: aiohttp.ClientSession) -> Optional[Dict]:
        """
        Busca precios en Fotocasa para un municipio específico
        """
        try:
            municipio_url = municipio.lower().replace(' ', '-')
            url = f"https://www.fotocasa.es/es/comprar/viviendas/{municipio_url}/todas-las-zonas/l"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extraer datos de Fotocasa
                    precio = self._extraer_precio_fotocasa(soup)
                    
                    if precio:
                        return {
                            'municipio': municipio,
                            'precio_venta': precio,
                            'fuente': 'Fotocasa',
                            'fecha': datetime.now().isoformat()
                        }
                        
        except Exception as e:
            print(f"❌ Error buscando {municipio} en Fotocasa: {str(e)}")
            
        return None
    
    def _extraer_precio_fotocasa(self, soup: BeautifulSoup) -> Optional[float]:
        """Extrae precio de Fotocasa"""
        try:
            precio_elem = soup.select_one('.re-CardPrice')
            if precio_elem:
                texto = precio_elem.get_text()
                precio = ''.join(filter(str.isdigit, texto))
                if precio:
                    return float(precio)
        except:
            pass
        return None
    
    async def procesar_municipio(self, municipio: str, session: aiohttp.ClientSession) -> Dict:
        """
        Procesa un municipio completo buscando en todas las fuentes
        """
        print(f"🔍 Buscando datos para: {municipio}")
        
        resultados = []
        
        # Buscar en Idealista
        resultado_idealista = await self.buscar_precio_idealista(municipio, session)
        if resultado_idealista:
            resultados.append(resultado_idealista)
        
        # Buscar en Fotocasa
        resultado_fotocasa = await self.buscar_precio_fotocasa(municipio, session)
        if resultado_fotocasa:
            resultados.append(resultado_fotocasa)
        
        # Combinar resultados
        if resultados:
            precio_venta_promedio = sum(r.get('precio_venta', 0) for r in resultados if r.get('precio_venta')) / len([r for r in resultados if r.get('precio_venta')])
            precio_alquiler_promedio = sum(r.get('precio_alquiler', 0) for r in resultados if r.get('precio_alquiler')) / len([r for r in resultados if r.get('precio_alquiler')]) if any(r.get('precio_alquiler') for r in resultados) else None
            
            return {
                'municipio': municipio,
                'precio_venta': precio_venta_promedio,
                'precio_alquiler': precio_alquiler_promedio,
                'fuentes': len(resultados),
                'fecha': datetime.now().isoformat()
            }
        
        return None
    
    async def ejecutar_busqueda_completa(self, limite: int = None):
        """
        Ejecuta la búsqueda completa de todos los municipios
        """
        print("🚀 Iniciando búsqueda completa de precios inmobiliarios")
        print(f"📊 Total de municipios a procesar: {len(self.municipios)}")
        
        municipios_a_procesar = self.municipios[:limite] if limite else self.municipios
        
        async with aiohttp.ClientSession() as session:
            resultados = []
            
            for i, municipio in enumerate(municipios_a_procesar, 1):
                print(f"\n[{i}/{len(municipios_a_procesar)}] Procesando: {municipio}")
                
                resultado = await self.procesar_municipio(municipio, session)
                
                if resultado:
                    resultados.append(resultado)
                    print(f"✅ Datos encontrados para {municipio}")
                    
                    # Guardar en Supabase
                    self._guardar_en_supabase(resultado)
                else:
                    print(f"⚠️ No se encontraron datos para {municipio}")
                
                # Pausa entre municipios para no saturar
                await asyncio.sleep(random.uniform(2, 5))
        
        print(f"\n🎉 Búsqueda completada!")
        print(f"✅ Municipios con datos: {len(resultados)}")
        print(f"⚠️ Municipios sin datos: {len(municipios_a_procesar) - len(resultados)}")
        
        return resultados
    
    def _guardar_en_supabase(self, datos: Dict):
        """Guarda los datos en Supabase"""
        try:
            # Calcular rentabilidad si tenemos ambos precios
            rentabilidad = None
            ratio_recuperacion = None
            
            if datos.get('precio_venta') and datos.get('precio_alquiler'):
                rentabilidad = (datos['precio_alquiler'] * 12 / datos['precio_venta']) * 100
                ratio_recuperacion = datos['precio_venta'] / (datos['precio_alquiler'] * 12)
            
            registro = {
                'nombre': datos['municipio'].replace('-', ' ').title(),
                'precio_venta': datos.get('precio_venta'),
                'precio_alquiler': datos.get('precio_alquiler'),
                'rentabilidad': rentabilidad,
                'ratio_recuperacion': ratio_recuperacion,
                'updated_at': datetime.now().isoformat()
            }
            
            self.supabase.upsert_municipio(registro)
            print(f"💾 Guardado en Supabase: {registro['nombre']}")
            
        except Exception as e:
            print(f"❌ Error guardando en Supabase: {str(e)}")


async def main():
    """Función principal"""
    agente = PreciosInmobiliariosAgent()
    
    # Ejecutar búsqueda completa (puedes limitar con limite=10 para pruebas)
    resultados = await agente.ejecutar_busqueda_completa(limite=10)
    
    # Guardar resultados en JSON
    with open('resultados_busqueda.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print("\n📄 Resultados guardados en: resultados_busqueda.json")


if __name__ == "__main__":
    asyncio.run(main())
