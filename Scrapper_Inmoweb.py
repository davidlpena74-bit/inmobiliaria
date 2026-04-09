"""
Scrapper_Inmoweb.py
===================
Agente para extraer todas las propiedades del CRM de Inmoweb.
Requiere autenticación con las credenciales configuradas en config.py.
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
import json
import config

class InmowebScrapper:
    def __init__(self):
        self.domain = config.INMOWEB_DOMAIN
        self.email = config.INMOWEB_EMAIL
        self.password = config.INMOWEB_PASS
        self.login_url = config.INMOWEB_LOGIN_URL
        self.propiedades = []
        self.driver = None

    def iniciar_navegador(self, headless=False):
        print("🚀 Iniciando navegador para Inmoweb...")
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Navegador listo.")

    def login(self):
        print(f"🔑 Accediendo a {self.login_url}...")
        self.driver.get(self.login_url)
        
        try:
            # Esperar a que los campos estén presentes
            wait = WebDriverWait(self.driver, 10)
            
            print("📝 Introduciendo credenciales...")
            # Dominio/Cuenta
            dom_field = wait.until(EC.presence_of_element_located((By.ID, "wxp_domain")))
            dom_field.send_keys(self.domain)
            
            # Email
            email_field = self.driver.find_element(By.NAME, "email")
            email_field.send_keys(self.email)
            
            # Password
            pass_field = self.driver.find_element(By.ID, "wxp_password")
            pass_field.send_keys(self.password)
            
            # Click Login
            login_btn = self.driver.find_element(By.ID, "m_login_signin_submit")
            login_btn.click()
            
            print("⏳ Esperando carga del panel...")
            # Esperar a que cargue el dashboard (buscamos un elemento común del panel)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m-header-menu")))
            print("✅ Login exitoso.")
            return True
            
        except Exception as e:
            print(f"❌ Error durante el login: {e}")
            return False

    def navegar_a_inmuebles(self):
        print("📁 Navegando a la lista de inmuebles...")
        # Basado en la investigación, la URL suele ser /inmuebles/
        # Si no, intentamos navegar por el menú
        self.driver.get("https://panel.inmoweb.es/inmuebles/")
        time.sleep(3)
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "m-datatable"))
            )
            print("✅ Lista de inmuebles cargada.")
            return True
        except:
            print("⚠️ No se encontró la tabla de inmuebles directamente. Intentando via menú...")
            return False

    def extraer_datos(self):
        print("🔍 Extrayendo datos de la tabla...")
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, ".m-datatable__row")
            print(f"🏠 Encontradas {len(rows)} filas en esta página.")
            
            for row in rows:
                try:
                    # La estructura exacta depende del cliente de Inmoweb, 
                    # pero solemos buscar las columnas por su atributo data-field o posición
                    cols = row.find_elements(By.TAG_NAME, "td")
                    
                    # Mapeo tentativo basado en Metronic theme usado por Inmoweb
                    datos = {
                        "ref": row.find_element(By.CSS_SELECTOR, "[data-field='Referencia']").text if row.find_elements(By.CSS_SELECTOR, "[data-field='Referencia']") else "",
                        "titulo": row.find_element(By.CSS_SELECTOR, "[data-field='Inmueble']").text if row.find_elements(By.CSS_SELECTOR, "[data-field='Inmueble']") else "",
                        "precio": row.find_element(By.CSS_SELECTOR, "[data-field='Precio']").text if row.find_elements(By.CSS_SELECTOR, "[data-field='Precio']") else "",
                        "municipio": row.find_element(By.CSS_SELECTOR, "[data-field='Municipio']").text if row.find_elements(By.CSS_SELECTOR, "[data-field='Municipio']") else "",
                        "operacion": row.find_element(By.CSS_SELECTOR, "[data-field='Operacion']").text if row.find_elements(By.CSS_SELECTOR, "[data-field='Operacion']") else "",
                        "fecha_captacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "fuente": "Inmoweb CRM"
                    }
                    
                    # Intentar obtener si está publicado en web propia (icono de globo)
                    publicado_web = False
                    web_col = row.find_elements(By.CSS_SELECTOR, "[data-field='Web'] i.fa-globe")
                    if web_col:
                        # Si el icono tiene color o clase active, está publicado
                        style = web_col[0].get_attribute("style")
                        if "color" in style or "text-success" in web_col[0].get_attribute("class"):
                            publicado_web = True
                    
                    datos["publicado_inmoweb_web"] = publicado_web
                    
                    if datos["ref"]:
                        self.propiedades.append(datos)
                except Exception as row_error:
                    print(f"⚠️ Error en una fila: {row_error}")
                    continue
                    
            return True
        except Exception as e:
            print(f"❌ Error extrayendo datos: {e}")
            return False

    def guardar_datos(self):
        os.makedirs('data', exist_ok=True)
        filename = 'data/inmoweb_properties.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.propiedades, f, indent=2, ensure_ascii=False)
        print(f"💾 Guardados {len(self.propiedades)} inmuebles en {filename}")

    def cerrar(self):
        if self.driver:
            self.driver.quit()
            print("🔒 Navegador cerrado.")

def main():
    scrapper = InmowebScrapper()
    try:
        scrapper.iniciar_navegador(headless=False) # False para ver que el login funciona
        if scrapper.login():
            if scrapper.navegar_a_inmuebles():
                scrapper.extraer_datos()
                # Aquí se podría añadir lógica de paginación si hay muchas propiedades
                scrapper.guardar_datos()
    finally:
        scrapper.cerrar()

if __name__ == "__main__":
    main()
