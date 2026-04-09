import time
import json
import re
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_coldwell_banker(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        # Wait for key elements to load
        wait = WebDriverWait(driver, 20)
        
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        except:
            pass

        time.sleep(3)

        # 1. Title
        titulo = ""
        try:
            titulo = driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            pass
        
        # 2. Price
        precio = 0
        try:
            price_elem = driver.find_element(By.CSS_SELECTOR, ".property-info__item--price .property-info__item-value")
            precio_str = price_elem.text.strip()
            match_price = re.search(r'([\d\.,]+)', precio_str)
            if match_price:
                precio = float(match_price.group(1).replace(".", "").replace(",", ""))
        except:
            pass

        # Bedrooms
        habitaciones = 0
        try:
            rooms_elem = driver.find_element(By.CSS_SELECTOR, ".property-info__item--bedrooms .property-info__item-value")
            habitaciones = int(rooms_elem.text.strip())
        except:
            pass

        # Bathrooms
        banos = 0
        try:
            baths_elem = driver.find_element(By.CSS_SELECTOR, ".property-info__item--bathrooms .property-info__item-value")
            banos = int(baths_elem.text.strip())
        except:
            pass

        # Surface
        superficie = 0
        try:
            size_elem = driver.find_element(By.CSS_SELECTOR, ".property-info__item--size .property-info__item-value")
            match_sup = re.search(r'(\d+)', size_elem.text)
            if match_sup:
                superficie = float(match_sup.group(1))
        except:
            pass

        # 4. Description
        descripcion = ""
        try:
            desc_elem = driver.find_element(By.CSS_SELECTOR, ".description._contentStyle")
            descripcion = desc_elem.text.strip()
        except:
            pass

        # 5. Features
        features = []
        try:
            feature_elems = driver.find_elements(By.CSS_SELECTOR, ".property-attributes__features .property-attributes__value")
            for feat in feature_elems:
                txt = feat.text.strip()
                if txt:
                    features.append(txt)
        except:
            pass
            
        # 3. Reference - Improved extraction
        referencia = ""
        try:
            # Fallback 1: Extract from description if it has #ref:
            ref_match = re.search(r'#ref:([A-Z0-9]+)', descripcion)
            if ref_match:
                referencia = ref_match.group(1)
            else:
                # Fallback 2: Find the div that contains "Reference" then get its sibling info div
                ref_label = driver.find_element(By.XPATH, "//div[contains(@class, 'attributes__block-title') and contains(text(), 'Reference')]")
                ref_val = ref_label.find_element(By.XPATH, "./following-sibling::div")
                referencia = ref_val.text.strip()
        except:
            try:
                # Fallback 3: Check all attribute values
                ref_all = driver.find_elements(By.CSS_SELECTOR, ".property-attribute__value")
                for item in ref_all:
                    text = item.text.strip()
                    if re.match(r'^[A-Z0-9]{3,}', text) and len(text) < 15:
                        referencia = text
                        break
            except:
                pass

        # 6. Images
        images = []
        try:
            img_elems = driver.find_elements(By.CSS_SELECTOR, ".propertyTopImage__image")
            for img in img_elems:
                href = img.get_attribute("href")
                if href:
                    images.append(href)
        except:
            pass

        # Location from URL
        url_parts = url.split("/")
        zona = ""
        ciudad = ""
        if len(url_parts) > 5:
            ciudad = url_parts[4].replace("-", " ").title()
            zona = url_parts[5].replace("-", " ").title()

        # Schema mapping
        all_features_text = " ".join(features).lower() + " " + descripcion.lower() + " " + titulo.lower()
        has_pool = any(k in all_features_text for k in ["pool", "piscina"])
        has_ac = any(k in all_features_text for k in ["air conditioning", "a/c", "aire acondicionado", "climatizado"])
        has_garage = any(k in all_features_text for k in ["garage", "garaje", "parking", "estacionamiento", "aparcamiento"])
        has_garden = any(k in all_features_text for k in ["garden", "jardín"])
        has_elevator = any(k in all_features_text for k in ["elevator", "ascensor"])
        has_storage = any(k in all_features_text for k in ["storage room", "trastero", "almacén"])

        propiedad = {
            "referencia": referencia,
            "titulo": titulo,
            "tipo": "Villa" if "villa" in titulo.lower() else "House",
            "precio": precio,
            "habitaciones": habitaciones,
            "banos": banos,
            "superficie": superficie,
            "zona": zona,
            "url": url,
            "agente": "coldwellbanker",
            "descripcion": descripcion,
            "imagenes_url": list(dict.fromkeys(images)), # Unique images
            "latitud": 38.7891,
            "longitud": 0.1631,
            "publicar_web": True,
            "estado_publicacion": "Activo",
            "origen_datos": "COLDWELL_BANKER",
            "caracteristicas": {
                "ciudad": ciudad,
                "cod_postal": "",
                "pais": "España",
                "pool": has_pool,
                "elevator": has_elevator,
                "garage": has_garage,
                "garden": has_garden,
                "air_conditioner": has_ac,
                "storage_room": has_storage,
                "year_built": 0,
                "features_list": features
            }
        }
        
        return propiedad

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        data = scrape_coldwell_banker(target_url)
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print("Usage: python scripts/scraper_coldwellbanker.py [URL]")
