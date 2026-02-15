"""
Scraper Mejorado de Idealista con Selenium
===========================================
Este scraper usa Selenium para obtener TODAS las propiedades disponibles
mediante paginación automática.

Características:
- Paginación automática hasta obtener todas las propiedades
- Manejo de anti-bot con delays aleatorios
- Extracción completa de datos
- Exportación a múltiples formatos
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import random
from datetime import datetime
import os
import re


class IdealistaScraperSelenium:
    """
    Scraper robusto con Selenium que obtiene TODAS las propiedades
    """
    
    def __init__(self, zona: str = "vicalvaro", ciudad: str = "madrid", tipo: str = "venta"):
        self.zona = zona
        self.ciudad = ciudad
        self.tipo = tipo  # "venta" o "alquiler"
        self.base_url = f"https://www.idealista.com/{tipo}-viviendas/{ciudad}/{zona}/"
        self.propiedades = []
        self.driver = None
        
    def iniciar_navegador(self, headless: bool = False, usar_proxy: bool = False, 
                          proxy_host: str = None, proxy_port: str = None,
                          proxy_user: str = None, proxy_pass: str = None):
        """
        Inicia el navegador Chrome con opciones anti-detección
        
        Args:
            headless: Ejecutar sin interfaz gráfica
            usar_proxy: Activar proxy (DataImpulse VPN)
            proxy_host: Host del proxy (ej: "gate.dataimpulse.com")
            proxy_port: Puerto del proxy (ej: "823")
            proxy_user: Usuario del proxy
            proxy_pass: Contraseña del proxy
        """
        print("🚀 Iniciando navegador...")
        
        chrome_options = Options()
        
        # ========================================
        # OPTIMIZACIÓN: BLOQUEAR IMÁGENES
        # ========================================
        # Esto hace el scraping MUCHO más rápido y ligero
        prefs = {
            "profile.managed_default_content_settings.images": 2,  # Bloquear imágenes
            "profile.default_content_setting_values.notifications": 2,  # Bloquear notificaciones
            "profile.managed_default_content_settings.stylesheets": 2,  # Opcional: bloquear CSS
            "profile.managed_default_content_settings.cookies": 1,  # Permitir cookies
            "profile.managed_default_content_settings.javascript": 1,  # Permitir JS
            "profile.managed_default_content_settings.plugins": 2,  # Bloquear plugins
            "profile.managed_default_content_settings.popups": 2,  # Bloquear popups
            "profile.managed_default_content_settings.geolocation": 2,  # Bloquear geolocalización
            "profile.managed_default_content_settings.media_stream": 2,  # Bloquear media
        }
        chrome_options.add_experimental_option("prefs", prefs)
        print("🚫 Imágenes bloqueadas (acceso ligero activado)")
        
        # ========================================
        # CONFIGURACIÓN DE PROXY (DataImpulse)
        # ========================================
        if usar_proxy and proxy_host and proxy_port:
            if proxy_user and proxy_pass:
                # Proxy con autenticación
                proxy_string = f"{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
                chrome_options.add_argument(f'--proxy-server=http://{proxy_string}')
                print(f"🔒 Proxy configurado: {proxy_host}:{proxy_port} (con autenticación)")
            else:
                # Proxy sin autenticación
                chrome_options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')
                print(f"🔒 Proxy configurado: {proxy_host}:{proxy_port}")
        
        # ========================================
        # ANTI-DETECCIÓN
        # ========================================
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent realista
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # ========================================
        # OPTIMIZACIONES DE RENDIMIENTO
        # ========================================
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins-discovery')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Headless mode
        if headless:
            chrome_options.add_argument('--headless=new')  # Nuevo headless mode
            print("👻 Modo headless activado")
        
        # Otras opciones
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--lang=es-ES')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        
        # Iniciar navegador
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Modificar webdriver property para evitar detección
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Configurar timeouts
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(5)
        
        print("✅ Navegador iniciado correctamente")
        
    def delay_aleatorio(self, min_sec: float = 2.0, max_sec: float = 5.0):
        """Espera aleatoria entre acciones"""
        tiempo = random.uniform(min_sec, max_sec)
        print(f"⏳ Esperando {tiempo:.2f} segundos...")
        time.sleep(tiempo)
    
    def scroll_suave(self):
        """Hace scroll suave por la página para simular comportamiento humano"""
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(1, 10):
            scroll_to = (total_height / 10) * i
            self.driver.execute_script(f"window.scrollTo(0, {scroll_to});")
            time.sleep(random.uniform(0.2, 0.5))
    
    def obtener_numero_total_propiedades(self):
        """Extrae el número total de propiedades disponibles"""
        try:
            # Idealista muestra el total en diferentes lugares, intentamos varios selectores
            selectores = [
                "h1",
                ".listing-title",
                ".main-info__title-main",
                "[data-testid='total-results']"
            ]
            
            for selector in selectores:
                try:
                    elemento = self.driver.find_element(By.CSS_SELECTOR, selector)
                    texto = elemento.text
                    
                    # Buscar números en el texto (ej: "345 viviendas en venta")
                    numeros = re.findall(r'\d+', texto.replace('.', ''))
                    if numeros:
                        total = int(numeros[0])
                        print(f"📊 Total de propiedades encontradas: {total}")
                        return total
                except:
                    continue
            
            print("⚠️ No se pudo determinar el número total de propiedades")
            return None
            
        except Exception as e:
            print(f"⚠️ Error obteniendo total: {e}")
            return None
    
    def extraer_propiedades_pagina(self):
        """Extrae todas las propiedades de la página actual"""
        propiedades_pagina = []
        
        try:
            # Esperar a que carguen los items
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article.item"))
            )
            
            # Scroll suave para cargar todo
            self.scroll_suave()
            
            # Encontrar todos los artículos de propiedades
            items = self.driver.find_elements(By.CSS_SELECTOR, "article.item")
            print(f"🏠 Encontrados {len(items)} anuncios en esta página")
            
            for item in items:
                try:
                    propiedad = self._extraer_datos_item(item)
                    if propiedad:
                        propiedades_pagina.append(propiedad)
                except Exception as e:
                    print(f"⚠️ Error extrayendo propiedad: {e}")
                    continue
            
        except TimeoutException:
            print("⚠️ Timeout esperando propiedades")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return propiedades_pagina
    
    def _extraer_datos_item(self, item):
        """Extrae datos de un item individual"""
        propiedad = {}
        
        try:
            # Precio
            try:
                precio_elem = item.find_element(By.CSS_SELECTOR, ".item-price")
                precio_text = precio_elem.text.strip()
                # Limpiar: "215.000 €" -> 215000
                precio_limpio = re.sub(r'[^\d]', '', precio_text)
                if precio_limpio:
                    propiedad['precio'] = int(precio_limpio)
            except:
                pass
            
            # Título y URL
            try:
                titulo_elem = item.find_element(By.CSS_SELECTOR, "a.item-link")
                propiedad['titulo'] = titulo_elem.text.strip()
                propiedad['url'] = titulo_elem.get_attribute('href')
            except:
                pass
            
            # Características (m², habitaciones, baños)
            try:
                detalles = item.find_elements(By.CSS_SELECTOR, ".item-detail")
                detalles_text = " ".join([d.text for d in detalles])
                propiedad['detalles'] = detalles_text
                
                # Extraer m²
                m2_match = re.search(r'(\d+)\s*m²', detalles_text)
                if m2_match:
                    propiedad['m2'] = int(m2_match.group(1))
                
                # Extraer habitaciones
                hab_match = re.search(r'(\d+)\s*hab', detalles_text)
                if hab_match:
                    propiedad['habitaciones'] = int(hab_match.group(1))
                
                # Extraer baños
                bano_match = re.search(r'(\d+)\s*baño', detalles_text)
                if bano_match:
                    propiedad['banos'] = int(bano_match.group(1))
                    
            except:
                pass
            
            # Descripción
            try:
                desc_elem = item.find_element(By.CSS_SELECTOR, ".item-description")
                propiedad['descripcion'] = desc_elem.text.strip()
            except:
                pass
            
            # Calcular precio/m²
            if 'precio' in propiedad and 'm2' in propiedad and propiedad['m2'] > 0:
                propiedad['precio_m2'] = round(propiedad['precio'] / propiedad['m2'], 2)
            
            # Metadata
            propiedad['zona'] = self.zona.title()
            propiedad['ciudad'] = self.ciudad.title()
            propiedad['tipo'] = self.tipo
            propiedad['fecha_extraccion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return propiedad if propiedad else None
            
        except Exception as e:
            return None
    
    def ir_siguiente_pagina(self):
        """Navega a la siguiente página de resultados"""
        try:
            # Buscar botón de siguiente página
            siguiente = self.driver.find_element(By.CSS_SELECTOR, ".icon-arrow-right-after")
            
            # Scroll hasta el botón
            self.driver.execute_script("arguments[0].scrollIntoView();", siguiente)
            time.sleep(1)
            
            # Hacer clic
            siguiente.click()
            print("➡️ Navegando a siguiente página...")
            
            # Esperar a que cargue la nueva página
            time.sleep(random.uniform(3, 5))
            return True
            
        except NoSuchElementException:
            print("✅ No hay más páginas (última página alcanzada)")
            return False
        except Exception as e:
            print(f"⚠️ Error navegando a siguiente página: {e}")
            return False
    
    def scrape_todas_las_paginas(self, max_paginas: int = None, headless: bool = False,
                                  usar_proxy: bool = False, proxy_host: str = None,
                                  proxy_port: str = None, proxy_user: str = None,
                                  proxy_pass: str = None):
        """
        Scrape todas las páginas disponibles
        
        Args:
            max_paginas: Límite de páginas (None = todas)
            headless: Ejecutar sin interfaz gráfica
            usar_proxy: Activar proxy DataImpulse
            proxy_host: Host del proxy
            proxy_port: Puerto del proxy
            proxy_user: Usuario del proxy
            proxy_pass: Contraseña del proxy
        """
        print(f"\n{'='*60}")
        print(f"🚀 Iniciando scraping completo de Idealista")
        print(f"📍 Zona: {self.zona.title()}, {self.ciudad.title()}")
        print(f"📄 Tipo: {self.tipo.title()}")
        if max_paginas:
            print(f"📄 Límite de páginas: {max_paginas}")
        else:
            print(f"📄 Scrapeando TODAS las páginas disponibles")
        print(f"{'='*60}\n")
        
        try:
            # Iniciar navegador con configuración
            self.iniciar_navegador(
                headless=headless,
                usar_proxy=usar_proxy,
                proxy_host=proxy_host,
                proxy_port=proxy_port,
                proxy_user=proxy_user,
                proxy_pass=proxy_pass
            )
            
            # Ir a la primera página
            print(f"🌐 Navegando a: {self.base_url}")
            self.driver.get(self.base_url)
            self.delay_aleatorio(3, 5)
            
            # Obtener total de propiedades
            total_esperado = self.obtener_numero_total_propiedades()
            
            # Aceptar cookies si aparecen
            try:
                cookie_btn = self.driver.find_element(By.ID, "didomi-notice-agree-button")
                cookie_btn.click()
                print("🍪 Cookies aceptadas")
                time.sleep(1)
            except:
                pass
            
            # Scrapear páginas
            pagina = 1
            while True:
                print(f"\n--- Página {pagina} ---")
                
                # Extraer propiedades de la página actual
                props_pagina = self.extraer_propiedades_pagina()
                self.propiedades.extend(props_pagina)
                
                print(f"✅ Extraídas {len(props_pagina)} propiedades")
                print(f"📊 Total acumulado: {len(self.propiedades)} propiedades")
                
                # Verificar si alcanzamos el límite
                if max_paginas and pagina >= max_paginas:
                    print(f"\n⚠️ Límite de {max_paginas} páginas alcanzado")
                    break
                
                # Intentar ir a siguiente página
                if not self.ir_siguiente_pagina():
                    break
                
                pagina += 1
                self.delay_aleatorio(4, 7)  # Delay más largo entre páginas
            
            print(f"\n{'='*60}")
            print(f"✅ Scraping completado")
            print(f"📊 Total de propiedades extraídas: {len(self.propiedades)}")
            if total_esperado:
                print(f"📊 Total esperado: {total_esperado}")
                cobertura = (len(self.propiedades) / total_esperado) * 100
                print(f"📊 Cobertura: {cobertura:.1f}%")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"❌ Error durante el scraping: {e}")
        
        finally:
            # Cerrar navegador
            if self.driver:
                self.driver.quit()
                print("🔒 Navegador cerrado")
        
        # Convertir a DataFrame
        if self.propiedades:
            return pd.DataFrame(self.propiedades)
        else:
            return pd.DataFrame()
    
    def guardar_datos(self, df: pd.DataFrame, formato: str = 'csv'):
        """Guarda los datos en diferentes formatos"""
        if df.empty:
            print("⚠️ No hay datos para guardar")
            return
        
        os.makedirs('datos', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"datos/idealista_{self.zona}_{self.tipo}_{timestamp}"
        
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
        
        return filename


def main():
    """Función principal"""
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║      SCRAPER COMPLETO DE IDEALISTA CON SELENIUM            ║
    ║                                                            ║
    ║  🎯 Obtiene TODAS las propiedades mediante paginación      ║
    ║  📊 Ejemplo: 345 propiedades en Vicálvaro                  ║
    ║  🚫 Imágenes bloqueadas (acceso ligero)                    ║
    ║  🔒 Soporte para proxy DataImpulse                         ║
    ║  ⚠️  Uso exclusivamente académico                          ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Intentar importar configuración
    try:
        from config import (
            ZONA, CIUDAD, TIPO, MAX_PAGINAS, HEADLESS,
            USAR_PROXY, PROXY_HOST, PROXY_PORT, PROXY_USER_BASE, PROXY_PASS
        )
        print("✅ Configuración cargada desde config.py")
    except ImportError:
        # Configuración por defecto si no existe config.py
        print("⚠️ No se encontró config.py, usando configuración por defecto")
        ZONA = "vicalvaro"
        CIUDAD = "madrid"
        TIPO = "venta"
        MAX_PAGINAS = None
        HEADLESS = False
        USAR_PROXY = False
        PROXY_HOST = None
        PROXY_PORT = None
        PROXY_USER = None
        PROXY_USER_BASE = None
        PROXY_PASS = None
    
    # Generar usuario Proxy con sesión aleatoria si es necesario
    PROXY_USER = None
    if USAR_PROXY and PROXY_USER_BASE:
        session_id = random.randint(100000, 999999)
        PROXY_USER = f"{PROXY_USER_BASE}__country-es__session-{session_id}"
        print(f"🌍 IP Rotada - Nueva Sesión: {session_id}")

    # Mostrar configuración
    print(f"\n📋 CONFIGURACIÓN:")
    print(f"   Zona: {ZONA}")
    print(f"   Ciudad: {CIUDAD}")
    print(f"   Tipo: {TIPO}")
    print(f"   Páginas: {'Todas' if MAX_PAGINAS is None else MAX_PAGINAS}")
    print(f"   Headless: {'Sí' if HEADLESS else 'No'}")
    print(f"   Proxy: {'Activado ✅' if USAR_PROXY else 'Desactivado'}")
    if USAR_PROXY:
        print(f"   Proxy Host: {PROXY_HOST}:{PROXY_PORT}")
    print()
    
    # Crear scraper
    scraper = IdealistaScraperSelenium(zona=ZONA, ciudad=CIUDAD, tipo=TIPO)
    
    # Ejecutar scraping completo
    df = scraper.scrape_todas_las_paginas(
        max_paginas=MAX_PAGINAS,
        headless=HEADLESS,
        usar_proxy=USAR_PROXY,
        proxy_host=PROXY_HOST,
        proxy_port=PROXY_PORT,
        proxy_user=PROXY_USER,
        proxy_pass=PROXY_PASS
    )
    
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
        
        if 'habitaciones' in df.columns:
            print(f"   Habitaciones media: {df['habitaciones'].mean():.1f}")
        
        # Guardar datos
        print("\n💾 Guardando datos...")
        scraper.guardar_datos(df, formato='csv')
        scraper.guardar_datos(df, formato='json')
        scraper.guardar_datos(df, formato='excel')
        
        # Mostrar muestra
        print("\n📋 MUESTRA DE DATOS (primeras 5 propiedades):")
        columnas = ['titulo', 'precio', 'm2', 'precio_m2', 'habitaciones']
        columnas_disponibles = [c for c in columnas if c in df.columns]
        print(df[columnas_disponibles].head(5).to_string(index=False))
        
    else:
        print("\n⚠️ No se pudieron extraer datos")


if __name__ == "__main__":
    main()
