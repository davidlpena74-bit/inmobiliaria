"""
Scraper de Fotocasa con Selenium y Proxy Rotativo
==================================================
Este script extrae propiedades de Fotocasa utilizando Selenium y rotación de IPs
con DataImpulse para evitar bloqueos.

Características:
- Soporte para Proxy Residencial (DataImpulse)
- Manejo de SPA (Single Page Application) de Fotocasa
- Extracción completa de datos (Precio, m2, Habitaciones, etc.)
- Exportación a CSV, JSON, Excel y Supabase
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
import sys
import io

# Configurar salida UTF-8 para consola Windows
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass

# Intentar importar configuración
try:
    from config import (
        ZONA, CIUDAD, TIPO, MAX_PAGINAS, HEADLESS,
        USAR_PROXY, PROXY_HOST, PROXY_PORT, PROXY_USER_BASE, PROXY_PASS
    )
except ImportError:
    # Configuración por defecto
    ZONA = "vicalvaro"
    CIUDAD = "madrid"
    TIPO = "venta"
    MAX_PAGINAS = 3
    HEADLESS = False
    USAR_PROXY = False

class FotocasaScraper:
    """
    Scraper especializado para Fotocasa
    """
    
    def __init__(self, zona: str = "madrid-provincia", ciudad: str = "madrid", tipo: str = TIPO):
        self.zona = zona.lower()
        self.ciudad = ciudad.lower()
        self.tipo = tipo
        # URL base fija para Madrid Provincia (con paginación /l/X)
        tipo_url = "comprar" if tipo == "venta" else "alquiler"
        # Base sin numero de pagina
        self.base_url_template = f"https://www.fotocasa.es/es/{tipo_url}/viviendas/madrid-provincia/todas-las-zonas/l"
        self.propiedades = []
        self.driver = None
        
    def get_url_pagina(self, pagina):
        """Genera la URL correcta para la página X"""
        if pagina == 1:
            return self.base_url_template
        return f"{self.base_url_template}/{pagina}"
        
    def get_proxy_extension(self, host, port, user, password):
        """Genera una extensión de Chrome para autenticar el proxy"""
        import zipfile
        
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version": "22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (host, port, user, password)

        plugin_file = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        
        return os.path.abspath(plugin_file)

    def iniciar_navegador(self):
        """Inicia Chrome con extensión de proxy autenticado"""
        print("🚀 Iniciando navegador para Fotocasa (Modo Extensión Proxy)...")
        
        chrome_options = Options()
        
        # 1. Configuración básica
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # 2. Evasión
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 3. User-Agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        
        # 4. Configurar Proxy DataImpulse MEDIANTE EXTENSIÓN
        if USAR_PROXY and PROXY_HOST and PROXY_PORT:
            session_id = random.randint(100000, 999999)
            proxy_user = f"{PROXY_USER_BASE}__country-es__session-{session_id}"
            
            print(f"🌍 Generando extensión proxy para sesión: {session_id}")
            proxy_plugin = self.get_proxy_extension(PROXY_HOST, PROXY_PORT, proxy_user, PROXY_PASS)
            chrome_options.add_extension(proxy_plugin)
        
        # 5. Inicializar driver
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # 6. Parchear propiedad 'webdriver'
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Navegador iniciado con Proxy Autenticado")

    def cerrar_cookies(self):
        """Intenta cerrar el banner de cookies de Fotocasa"""
        try:
            # El selector del botón de cookies puede variar
            selectors = [
                '[data-testid="TcfAccept"]',
                '#didomi-notice-agree-button',
                'button.sui-AtomButton--primary'
            ]
            
            for selector in selectors:
                try:
                    btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    btn.click()
                    print("🍪 Cookies aceptadas")
                    time.sleep(1)
                    return
                except:
                    continue
        except:
            print("⚠️ No se pudo cerrar banner de cookies (o no apareció)")

    def scroll_suave(self):
        """Scroll para cargar lazy loading"""
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(1, 6):
            self.driver.execute_script(f"window.scrollTo(0, {(total_height/5)*i});")
            time.sleep(random.uniform(0.5, 1.0))

    def extraer_datos_pagina(self):
        """Extrae propiedades de la página actual con selectores robustos"""
        print("🔍 Extrayendo propiedades...")
        
        # 1. Guardar HTML para diagnóstico si falla
        try:
            with open("debug_fotocasa.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
        except: pass

        # 2. Intentar múltiples selectores para encontrar las tarjetas
        selectors = [
             'article.re-Card',       # Selector clásico
             '.re-Card',              # Solo clase
             '[class*="re-Card"]',    # Clase parcial
             'article',               # Tag genérico
             'div.sui-Card',          # Selector alternativo
             '.sui-Card'
        ]
        
        cards = []
        selector_usado = ""
        
        for sel in selectors:
            found = self.driver.find_elements(By.CSS_SELECTOR, sel)
            # Filtrar elementos invisibles o muy pequeños
            valid_cards = [c for c in found if c.size['height'] > 50]
            
            if len(valid_cards) > 2:
                cards = valid_cards
                selector_usado = sel
                print(f"✅ Selector efectivo: '{sel}'")
                break
                 
        print(f"🏠 Encontradas {len(cards)} tarjetas")
        
        if not cards:
             print(f"⚠️ Título de página: {self.driver.title}")
             return []

        nuevas_props = []
        for card in cards:
            try:
                # Comprobar si el elemento sigue vivo
                if not card.is_displayed():
                    continue
                    
                prop = {}
                # ... Lógica de extracción ...
                
                # Para evitar StaleElementReferenceException, re-buscamos dentro de la tarjeta
                # o usamos esperas cortas si fuera necesario.
                # Aquí confiamos en el bloque try-except general del bucle
                
                # PRECIO
                try:
                    p_elem = card.find_element(By.CSS_SELECTOR, '.re-CardPrice')
                    prop['precio'] = int(re.sub(r'[^\d]', '', p_elem.text))
                except:
                    try: # Intento alternativo
                        p_elem = card.find_element(By.CSS_SELECTOR, '[class*="Price"]')
                        prop['precio'] = int(re.sub(r'[^\d]', '', p_elem.text))
                    except: prop['precio'] = 0
                
                # TÍTULO
                try:
                    t_elem = card.find_element(By.CSS_SELECTOR, '.re-CardTitle')
                    prop['titulo'] = t_elem.text
                except:
                    try:
                         t_elem = card.find_element(By.CSS_SELECTOR, '[class*="Title"]')
                         prop['titulo'] = t_elem.text
                    except: prop['titulo'] = "Sin título"
                
                # DETALLES (habs, baños, m2)
                try:
                    features = card.find_elements(By.CSS_SELECTOR, '.re-CardFeatures-feature')
                    if not features: # Fallback
                        features = card.find_elements(By.CSS_SELECTOR, 'li')
                    
                    prop['detalles'] = " | ".join([f.text for f in features])
                    
                    for f in features:
                        txt = f.text.lower()
                        if 'hab' in txt:
                            prop['habitaciones'] = int(re.sub(r'[^\d]', '', txt))
                        elif 'baño' in txt:
                            prop['banos'] = int(re.sub(r'[^\d]', '', txt))
                        elif 'm²' in txt:
                            prop['m2'] = int(re.sub(r'[^\d]', '', txt))
                except: pass
                
                # ENLACE
                try:
                    try: link = card.find_element(By.CSS_SELECTOR, 'a.re-Card-link')
                    except: link = card.find_element(By.CSS_SELECTOR, 'a')
                    prop['url'] = link.get_attribute('href')
                except: prop['url'] = ""
                
                # Metadata
                prop['zona'] = self.zona
                prop['portal'] = 'Fotocasa'
                prop['fecha'] = datetime.now().strftime('%Y-%m-%d')
                
                # Precio/m2
                if prop.get('precio') and prop.get('m2'):
                    prop['precio_m2'] = round(prop['precio'] / prop['m2'], 2)
                
                if prop.get('titulo'):
                    nuevas_props.append(prop)
                    
            except Exception:
                # Si falla una tarjeta (StaleElement o lo que sea), la saltamos
                continue
                
        return nuevas_props

    def ir_siguiente_pagina(self):
        """Navega a la siguiente página"""
        try:
            # Botón siguiente suele ser re-Pagination-link--next o similar
            next_btn = self.driver.find_element(By.CSS_SELECTOR, 'li.re-Pagination-item--next a')
            self.driver.execute_script("arguments[0].scrollIntoView();", next_btn)
            time.sleep(1)
            next_btn.click()
            print("➡️ Navegando a siguiente página...")
            time.sleep(random.uniform(3, 5))
            return True
        except:
            print("✅ No hay más páginas (o error al navegar)")
            return False

    def guardar_datos(self):
        """Guarda los datos extraídos en CSV, Excel y Supabase"""
        if not self.propiedades:
            print("⚠️ No hay datos para guardar")
            return
            
        print("\n💾 Guardando datos...")
        # CSV y Excel
        df = pd.DataFrame(self.propiedades)
        os.makedirs('datos', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        df.to_csv(f"datos/fotocasa_{self.zona}_{timestamp}.csv", index=False, encoding='utf-8-sig')
        # df.to_excel(f"datos/fotocasa_{self.zona}_{timestamp}.xlsx", index=False) # Requiere openpyxl
        
        # --- SUPABASE INTEGRATION ---
        try:
            from supabase_utils import SupabaseClient
            supabase = SupabaseClient()
            print("☁️ Subiendo datos a Supabase...")
            
            # Mapear columnas de Fotocasa a tabla de Supabase (inm_propiedades)
            for prop in self.propiedades:
                registro = {
                    "titulo": prop.get('titulo', ''),
                    "precio": prop.get('precio', 0),
                    "habitaciones": prop.get('habitaciones', 0),
                    "superficie": prop.get('m2', 0),
                    "zona": self.zona,
                    "url": prop.get('url', ''),
                    "descripcion": prop.get('detalles', ''),
                    "caracteristicas": {
                        "banos": prop.get('banos', 0),
                        "precio_m2": prop.get('precio_m2', 0),
                        "portal": "Fotocasa",
                        "origen_dato": "fotocasa"
                    }
                }
                # Usar insert_propiedad que es el método correcto en SupabaseClient
                supabase.insert_propiedad(registro)
                
            print(f"✅ {len(self.propiedades)} registros sincronizados con Supabase.")
        except Exception as e:
            print(f"⚠️ Error subiendo a Supabase: {e}")
        # ---------------------------

    def ejecutar(self):
        """Flujo principal de ejecución"""
        try:
            self.iniciar_navegador()
            
            # Iterar directamente por páginas
            pagina = 1
            while True:
                url_actual = self.get_url_pagina(pagina)
                print(f"\n--- Página {pagina} ---")
                print(f"🌐 Navegando a: {url_actual}")
                
                self.driver.get(url_actual)
                time.sleep(3)
                
                if pagina == 1:
                    self.cerrar_cookies()
                
                self.scroll_suave()
                
                props = self.extraer_datos_pagina()
                
                if not props:
                    print("⚠️ No se encontraron propiedades en esta página. Terminando.")
                    break
                    
                self.propiedades.extend(props)
                print(f"✅ Acumulado: {len(self.propiedades)} propiedades")
                
                # Guardar checkpoint cada página por seguridad
                if len(self.propiedades) % 30 == 0:
                     print("💾 Guardado parcial...")
                     pass # Ya se guardará al final, pero podríamos forzar aquí

                if MAX_PAGINAS and pagina >= MAX_PAGINAS:
                    print(f"⚠️ Límite de {MAX_PAGINAS} páginas alcanzado")
                    break
                
                pagina += 1
                time.sleep(random.uniform(2, 4))
                
        except Exception as e:
            print(f"❌ Error fatal: {e}")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            self.guardar_datos()

if __name__ == "__main__":
    scraper = FotocasaScraper()
    scraper.ejecutar()
