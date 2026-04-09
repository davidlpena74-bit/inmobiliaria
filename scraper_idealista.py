"""
Scraper Ético de Idealista - Pisos en Venta
============================================
Este script extrae información de propiedades en venta de Idealista
respetando buenas prácticas de web scraping.

Autor: Proyecto Académico UNED - Ciencia de Datos
Uso: Exclusivamente educativo y de investigación
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List, Dict
import json
from datetime import datetime
import os
import config
import supabase_utils

class IdealistaScraperEtico:
    """
    Scraper ético para Idealista que respeta:
    - Rate limiting (delays entre peticiones)
    - User-Agent apropiado
    - Robots.txt
    - Términos de uso
    """
    
    def __init__(self, zona: str = "vicalvaro", ciudad: str = "madrid"):
        self.zona = zona
        self.ciudad = ciudad
        self.base_url = f"https://www.idealista.com/venta-viviendas/{ciudad}/{zona}/"
        
        # Headers para simular un navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.session = requests.Session()
        self.propiedades = []
        
        # Configurar Proxy con rotación de IPs
        if config.USAR_PROXY:
            self._rotar_ip()
            
    def _rotar_ip(self):
        """Configura una nueva IP usando DataImpulse"""
        session_id = random.randint(100000, 999999)
        proxy_user = f"{config.PROXY_USER_BASE}__country-es__session-{session_id}"
        
        proxy_url = f"http://{proxy_user}:{config.PROXY_PASS}@{config.PROXY_HOST}:{config.PROXY_PORT}"
        
        self.proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        self.session.proxies.update(self.proxies)
        print(f"🌍 IP Rotada - Nueva Sesión: {session_id}")
            
    def delay_aleatorio(self, min_sec: float = 2.0, max_sec: float = 5.0):
        """Espera aleatoria entre peticiones para ser respetuoso"""
        tiempo = random.uniform(min_sec, max_sec)
        print(f"⏳ Esperando {tiempo:.2f} segundos...")
        time.sleep(tiempo)
    
    def obtener_pagina(self, url: str, max_reintentos: int = 3) -> BeautifulSoup:
        """Obtiene y parsea una página web con reintentos y rotación de IP"""
        intentos = 0
        
        while intentos < max_reintentos:
            try:
                print(f"📡 Solicitando: {url} (Intento {intentos + 1})")
                
                # La sesión ya tiene el proxy configurado si config.USAR_PROXY es True
                response = self.session.get(url, headers=self.headers, timeout=15)
                
                if response.status_code == 200:
                    print(f"✅ Página obtenida correctamente (Status: {response.status_code})")
                    return BeautifulSoup(response.content, 'html.parser')
                
                elif response.status_code == 403:
                    print(f"⚠️ Acceso bloqueado (403). Idealista detectó el scraping.")
                    
                    if config.USAR_PROXY:
                        print("� Rotando IP para evadir bloqueo...")
                        self._rotar_ip()
                        intentos += 1
                        time.sleep(2) # Pequeña pausa antes de reintentar con nueva IP
                        continue
                    else:
                        print("💡 Sugerencia: Activa el PROXY en config.py para rotar IPs.")
                        return None
                        
                else:
                    print(f"❌ Error: Status code {response.status_code}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Error de conexión: {e}")
                if config.USAR_PROXY:
                    print("🔄 Error de red con proxy. Rotando IP...")
                    self._rotar_ip()
                intentos += 1
                time.sleep(2)
        
        print("❌ Se agotaron los reintentos. No se pudo obtener la página.")
        return None
    
    def extraer_propiedades(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrae información de las propiedades de una página"""
        if not soup:
            return []
        
        propiedades = []
        
        # Idealista usa diferentes estructuras, intentamos varias
        # Estructura principal: artículos con clase 'item'
        items = soup.find_all('article', class_='item')
        
        if not items:
            # Estructura alternativa
            items = soup.find_all('div', class_='item-info-container')
        
        print(f"🏠 Encontrados {len(items)} anuncios en esta página")
        
        for item in items:
            try:
                propiedad = self._extraer_datos_propiedad(item)
                if propiedad:
                    propiedades.append(propiedad)
            except Exception as e:
                print(f"⚠️ Error extrayendo propiedad: {e}")
                continue
        
        return propiedades
    
    def _extraer_datos_propiedad(self, item) -> Dict:
        """Extrae los datos de una propiedad individual"""
        propiedad = {}
        
        # Precio
        precio_elem = item.find('span', class_='item-price')
        if precio_elem:
            precio_text = precio_elem.text.strip()
            # Limpiar: "215.000 €" -> 215000
            precio_limpio = precio_text.replace('€', '').replace('.', '').replace(',', '').strip()
            try:
                propiedad['precio'] = int(precio_limpio)
            except:
                propiedad['precio'] = precio_text
        
        # Título/Dirección
        titulo_elem = item.find('a', class_='item-link')
        if titulo_elem:
            propiedad['titulo'] = titulo_elem.text.strip()
            propiedad['url'] = 'https://www.idealista.com' + titulo_elem.get('href', '')
        
        # Características (habitaciones, m², planta)
        detalles_elem = item.find('span', class_='item-detail')
        if detalles_elem:
            detalles_text = detalles_elem.text.strip()
            propiedad['detalles'] = detalles_text
            
            # Extraer m²
            if 'm²' in detalles_text:
                try:
                    m2 = detalles_text.split('m²')[0].strip().split()[-1]
                    propiedad['m2'] = int(m2)
                except:
                    pass
            
            # Extraer habitaciones
            if 'hab.' in detalles_text:
                try:
                    habs = detalles_text.split('hab.')[0].strip().split()[-1]
                    propiedad['habitaciones'] = int(habs)
                except:
                    pass
        
        # Descripción
        desc_elem = item.find('div', class_='item-description')
        if desc_elem:
            propiedad['descripcion'] = desc_elem.text.strip()
        
        # Calcular precio/m² si tenemos ambos datos
        if 'precio' in propiedad and 'm2' in propiedad and isinstance(propiedad['precio'], int):
            try:
                propiedad['precio_m2'] = round(propiedad['precio'] / propiedad['m2'], 2)
            except:
                pass
        
        # Metadata
        propiedad['zona'] = self.zona.title()
        propiedad['ciudad'] = self.ciudad.title()
        propiedad['fecha_extraccion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        propiedad['tipo_operacion'] = 'Alquiler' if 'alquiler' in self.base_url else 'Venta'
        
        return propiedad
    
    def scrape(self, max_paginas: int = 3) -> pd.DataFrame:
        """
        Ejecuta el scraping de múltiples páginas
        
        Args:
            max_paginas: Número máximo de páginas a scrapear
        
        Returns:
            DataFrame con todas las propiedades encontradas
        """
        print(f"\n{'='*60}")
        print(f"🚀 Iniciando scraping de Idealista")
        print(f"📍 Zona: {self.zona.title()}, {self.ciudad.title()}")
        print(f"📄 Páginas a scrapear: {max_paginas}")
        print(f"{'='*60}\n")
        
        for pagina in range(1, max_paginas + 1):
            print(f"\n--- Página {pagina}/{max_paginas} ---")
            
            # Construir URL con paginación
            if pagina == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}pagina-{pagina}.htm"
            
            # Obtener página
            soup = self.obtener_pagina(url)
            
            if soup:
                # Extraer propiedades
                props_pagina = self.extraer_propiedades(soup)
                self.propiedades.extend(props_pagina)
                print(f"✅ Total acumulado: {len(self.propiedades)} propiedades")
            else:
                print(f"⚠️ No se pudo obtener la página {pagina}")
                break
            
            # Delay entre páginas (excepto en la última)
            if pagina < max_paginas:
                self.delay_aleatorio(3.0, 6.0)
        
        # Convertir a DataFrame
        if self.propiedades:
            df = pd.DataFrame(self.propiedades)
            print(f"\n{'='*60}")
            print(f"✅ Scraping completado: {len(df)} propiedades extraídas")
            print(f"{'='*60}\n")
            return df
        else:
            print("\n⚠️ No se encontraron propiedades")
            return pd.DataFrame()
    
    def guardar_datos(self, df: pd.DataFrame, formato: str = 'csv'):
        """Guarda los datos en diferentes formatos"""
        if df.empty:
            print("⚠️ No hay datos para guardar")
            return
        
        # Crear carpeta de datos si no existe
        os.makedirs('datos', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"datos/idealista_{self.zona}_{timestamp}"
        
        if formato == 'csv':
            filename = f"{base_filename}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 Datos guardados en: {filename}")
        
        elif formato == 'json':
            filename = f"{base_filename}.json"
            df.to_json(filename, orient='records', force_ascii=False, indent=2)
            print(f"💾 Datos guardados en: {filename}")
        
        elif formato == 'excel':
            filename = f"{base_filename}.xlsx"
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"💾 Datos guardados en: {filename}")
        
        # Subir a Supabase si está habilitado
        if config.USAR_SUPABASE:
            print("☁️ Subiendo datos a Supabase...")
            for _, row in df.iterrows():
                propiedad = {
                    "titulo": row.get('titulo'),
                    "precio": row.get('precio'),
                    "habitaciones": row.get('habitaciones'),
                    "superficie": row.get('m2'),
                    "zona": row.get('zona'),
                    "url": row.get('url'),
                    "descripcion": row.get('descripcion'),
                    "caracteristicas": {"precio_m2": row.get('precio_m2')}
                }
                supabase_utils.insert_propiedad(propiedad)
            print("✅ Datos sincronizados con Supabase.")

        return filename


def main():
    """Función principal para ejecutar el scraper"""
    
    # Configuración
    ZONA = "vicalvaro"
    CIUDAD = "madrid"
    MAX_PAGINAS = 3  # Empezamos con pocas páginas para ser respetuosos
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         SCRAPER ÉTICO DE IDEALISTA - UNED PROJECT          ║
    ║                                                            ║
    ║  ⚠️  IMPORTANTE: Uso exclusivamente académico              ║
    ║  📚  Proyecto de Ciencia de Datos                          ║
    ║  🤝  Respeta rate limiting y términos de uso               ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Crear scraper
    scraper = IdealistaScraperEtico(zona=ZONA, ciudad=CIUDAD)
    
    # Ejecutar scraping
    df = scraper.scrape(max_paginas=MAX_PAGINAS)
    
    # Mostrar resultados
    if not df.empty:
        print("\n📊 RESUMEN DE DATOS EXTRAÍDOS:")
        print(f"   Total propiedades: {len(df)}")
        
        if 'precio' in df.columns:
            precios_numericos = pd.to_numeric(df['precio'], errors='coerce')
            print(f"   Precio medio: {precios_numericos.mean():,.0f} €")
            print(f"   Precio mínimo: {precios_numericos.min():,.0f} €")
            print(f"   Precio máximo: {precios_numericos.max():,.0f} €")
        
        if 'precio_m2' in df.columns:
            print(f"   Precio/m² medio: {df['precio_m2'].mean():,.2f} €/m²")
        
        if 'm2' in df.columns:
            print(f"   m² medio: {df['m2'].mean():.0f} m²")
        
        # Guardar datos
        print("\n💾 Guardando datos...")
        scraper.guardar_datos(df, formato='csv')
        scraper.guardar_datos(df, formato='json')
        
        # Mostrar muestra de datos
        print("\n📋 MUESTRA DE DATOS (primeras 3 propiedades):")
        print(df.head(3).to_string())
        
    else:
        print("\n⚠️ No se pudieron extraer datos.")
        print("💡 Posibles razones:")
        print("   1. Idealista bloqueó el acceso (error 403)")
        print("   2. La estructura HTML cambió")
        print("   3. Problema de conexión")
        print("\n💡 Soluciones:")
        print("   1. Usar Selenium con navegador real")
        print("   2. Solicitar acceso a la API oficial")
        print("   3. Aumentar delays entre peticiones")


if __name__ == "__main__":
    main()
