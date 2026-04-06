import json
import time
import random
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WepertiScraper:
    def __init__(self, headless=True):
        self.base_url = "https://www.weperti.com/results/?id_tipo_operacion=2"
        self.properties_data = []
        self.driver = self._init_driver(headless)

    def _init_driver(self, headless):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        # Bloquear imágenes en la fase de listado para mayor velocidad
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=chrome_options)

    def get_all_links(self):
        print("INFO: Obteniendo lista completa de enlaces (Paginación por URL)...", flush=True)
        links = []
        
        # Weperti usa i=offset y c=count. Con 83 propiedades, necesitamos i=0, 33, 66
        offsets = [0, 33, 66]
        
        for offset in offsets:
            url = f"{self.base_url}&i={offset}&c=33"
            print(f"INFO: Cargando página con offset {offset}...", flush=True)
            self.driver.get(url)
            time.sleep(4) # Esperar a que cargue el listado

            # Encontrar todos los enlaces a propiedades usando el selector verificado
            items = self.driver.find_elements(By.CSS_SELECTOR, ".masInfoPropiedad")
            if not items:
                items = self.driver.find_elements(By.CSS_SELECTOR, "#listOffers .punto_mapa a[href*='.html']")

            page_links = 0
            for item in items:
                href = item.get_attribute("href")
                if href and ".html" in href:
                    if href not in links:
                        links.append(href)
                        page_links += 1
            
            print(f"INFO: Se encontraron {page_links} enlaces nuevos en esta página. Total: {len(links)}", flush=True)

        return links

    def scrape_detail(self, url):
        print(f"INFO: Scrapeando: {url}", flush=True)
        self.driver.get(url)
        time.sleep(2)
        
        data = {"url": url}
        
        try:
            # 1. Referencia (Prioridad: Último elemento del breadcrumb)
            try:
                breadcrumb_items = self.driver.find_elements(By.CSS_SELECTOR, ".breadcrumb li, .breadcrumbs li")
                if breadcrumb_items:
                    ref_text = breadcrumb_items[-1].text.strip()
                    if ref_text and len(ref_text) > 3:
                        # Limpiar si contiene "Ref:"
                        if ":" in ref_text: ref_text = ref_text.split(":", 1)[1].strip()
                        # Solo si parece una referencia (no es el título de la página)
                        if not any(word in ref_text.lower() for word in ["apartment", "villa", "bungalow", "home"]):
                            data['referencia'] = ref_text.upper()
                
                # Si no se encontró o parece el "portal ID" (empieza por GB), buscar por patrón en el body
                if 'referencia' not in data or data['referencia'].startswith('GB'):
                    page_text = self.driver.find_element(By.TAG_NAME, "body").text
                    # Patrón: 3+ letras seguidas de 3+ alfanuméricos (ej: LAUSJW650, ALQYAGO)
                    matches = re.findall(r'([A-Z]{3,}[A-Z0-9]{3,})', page_text)
                    excluded = ["APARTMENT", "BUNGALOW", "VILLA", "BEDROOMS", "BATHROOMS", "CONSTRUCTED", "INVENTORY", "LOCATION"]
                    for m in matches:
                        if m not in excluded and len(m) < 15:
                            data['referencia'] = m
                            break
            except:
                pass

            # Fallback final: Extraer el portal ID de la URL
            if 'referencia' not in data:
                match = re.search(r'-(gb\d+)\.html', url, re.I)
                if match:
                    data['referencia'] = match.group(1).upper()
                else:
                    data['referencia'] = "UNK-" + str(int(time.time()))
            
            # Extraer también el ID numérico de la URL como backup
            match_id = re.search(r'-gb(\d+)\.html', url, re.I)
            if match_id:
                data['inmoweb_id'] = match_id.group(1)

            # 2. Título
            try:
                data['titulo'] = self.driver.find_element(By.TAG_NAME, "h1").text.strip()
            except:
                data['titulo'] = "Propiedad Weperti"

            # 3. Datos detallados (Descripción y Características)
            caracteristicas = {}
            try:
                # El subagente identificó que la info está en bloques .detallesFicha
                ficha_blocks = self.driver.find_elements(By.CSS_SELECTOR, ".detallesFicha")
                for block in ficha_blocks:
                    try:
                        header_elem = block.find_element(By.TAG_NAME, "h3")
                        header_text = header_elem.text.lower()
                        
                        if "description" in header_text:
                            # Extraer descripción (quitando el título)
                            full_text = block.text.strip()
                            data['descripcion'] = full_text.split("\n", 1)[1].strip() if "\n" in full_text else full_text
                        
                        elif "extras" in header_text or "features" in header_text or "características" in header_text:
                            # Extraer características
                            items = block.find_elements(By.TAG_NAME, "li")
                            for item in items:
                                text = item.text.strip()
                                if ":" in text:
                                    k, v = text.split(":", 1)
                                    caracteristicas[k.strip()] = v.strip()
                                else:
                                    caracteristicas[text] = True
                    except:
                        continue
                
                # 4. Sidebar Features (.caracteristicas li)
                sidebar_items = self.driver.find_elements(By.CSS_SELECTOR, ".caracteristicas li")
                for item in sidebar_items:
                    text = item.text.strip()
                    if ":" in text:
                        k, v = text.split(":", 1)
                        caracteristicas[k.strip()] = v.strip()
            except:
                pass
            data['caracteristicas'] = caracteristicas

            # 5. Imágenes (Full resolution desde Fotorama)
            images = []
            try:
                # Extraer URLs de las imágenes en el contenedor de Fotorama
                img_elems = self.driver.find_elements(By.CSS_SELECTOR, ".fotorama__stage .fotorama__img, .fotorama__nav .fotorama__img")
                for img in img_elems:
                    src = img.get_attribute("src")
                    if src:
                        # Inmoweb a veces usa /thumb/ o ?x=... para redimensionar
                        # Intentamos obtener la imagen original
                        original_src = src.replace("/thumb/585_335/", "/image/").replace("/thumb/115_115/", "/image/").split("?")[0]
                        if original_src not in images: images.append(original_src)
            except:
                pass
            data['imagenes_url'] = images

            # 5. Coordenadas (Desde el div #mapa)
            try:
                map_elem = self.driver.find_element(By.ID, "mapa")
                data['latitud'] = map_elem.get_attribute("data-lat")
                data['longitud'] = map_elem.get_attribute("data-lng")
            except:
                data['latitud'] = None
                data['longitud'] = None

            # 6. Características Técnicas
            caracteristicas = {}
            try:
                features = self.driver.find_elements(By.CSS_SELECTOR, ".list-features li, .tech-sheet-item")
                for feat in features:
                    text = feat.text.strip()
                    if ":" in text:
                        k, v = text.split(":", 1)
                        caracteristicas[k.strip()] = v.strip()
            except:
                pass
            data['caracteristicas'] = caracteristicas

            return data
        except Exception as e:
            print(f"❌ Error scrapeando {url}: {e}")
            return None

    def run(self, limit=None):
        links = self.get_all_links()
        if limit:
            links = links[:limit]
            print(f"INFO: Limitado a {limit} propiedades por test.", flush=True)
        
        # Cargar datos existentes para no repetir
        existing_refs = []
        if os.path.exists("data/weperti_full_export.json"):
            try:
                with open("data/weperti_full_export.json", 'r', encoding='utf-8') as f:
                    self.properties_data = json.load(f)
                    existing_refs = [p.get('url') for p in self.properties_data]
                    print(f"INFO: Resumiendo. {len(existing_refs)} propiedades ya procesadas.", flush=True)
            except:
                self.properties_data = []

        for i, link in enumerate(links):
            if link in existing_refs:
                continue

            prop_data = self.scrape_detail(link)
            if prop_data:
                self.properties_data.append(prop_data)
                print(f"INFO: {i+1}/{len(links)}: {prop_data['referencia']} capturada.", flush=True)
                
                # Guardar en lotes de 5 para no perder avances (instrucción del usuario)
                if len(self.properties_data) % 5 == 0:
                    print(f"INFO: Guardando lote de progreso ({len(self.properties_data)} propiedades)...", flush=True)
                    self.save_data()
            
            # Delay aleatorio para evitar bloques
            time.sleep(random.uniform(1, 3))

        # Guardar todo al final
        self.save_data()
        self.driver.quit()

    def save_data(self):
        output_file = "data/weperti_full_export.json"
        os.makedirs("data", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.properties_data, f, indent=2, ensure_ascii=False)
        # print(f"SUCCESS: Archivo ACTUALIZADO: {output_file}", flush=True)

if __name__ == "__main__":
    scraper = WepertiScraper(headless=True)
    # Para producción, quitar el limite o aumentarlo
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    scraper.run(limit=limit)
