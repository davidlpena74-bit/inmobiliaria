"""
Scrapper_Inmoweb.py
===================
Agente para extraer todas las propiedades del CRM de Inmoweb.
Versión optimizada con selectores verificados y soporte para paginación.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import os
import config

class InmowebScrapper:
    def __init__(self):
        self.domain = config.INMOWEB_DOMAIN
        self.email = config.INMOWEB_EMAIL
        self.password = config.INMOWEB_PASS
        self.login_url = config.INMOWEB_LOGIN_URL
        self.propiedades = []
        self.driver = None

    def iniciar_navegador(self, headless=True):
        print("Iniciando navegador...")
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=chrome_options)
        print("Navegador listo.")

    def login(self):
        print("Accediendo a login...")
        self.driver.get(self.login_url)
        wait = WebDriverWait(self.driver, 15)
        try:
            # Rellenar Dominio
            wait.until(EC.presence_of_element_located((By.ID, "wxp_domain"))).send_keys(self.domain)
            # Rellenar Email
            self.driver.find_element(By.NAME, "email").send_keys(self.email)
            # Rellenar Password
            self.driver.find_element(By.ID, "wxp_password").send_keys(self.password)
            # Submit
            self.driver.find_element(By.ID, "m_login_signin_submit").click()
            
            # Verificar éxito (esperar a que aparezca la botonera superior o similar)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m-header-menu")))
            print("Login exitoso.")
            return True
        except Exception as e:
            print("Error en login: " + str(e))
            return False

    def navegar_a_propiedades(self):
        url_inmuebles = "https://panel180.inmoweb.es/property/?feature[]=stat:::-1"
        print("Navegando a lista completa...")
        self.driver.get(url_inmuebles)
        time.sleep(5)
        return True

    def extraer_pagina_actual(self):
        print("Extrayendo datos de la pagina...")
        try:
            # Esperar a que las filas estén presentes
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.wxp_data_container"))
            )
            
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.wxp_data_container")
            for row in rows:
                try:
                    # Referencia está en td:nth-child(3)
                    ref = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
                    
                    # Publication Status (Columna 7)
                    # El selector verificado es label[data-title="Mi web"] input
                    try:
                        web_checkbox = row.find_element(By.CSS_SELECTOR, 'label[data-title="Mi web"] input')
                        esta_publicado = web_checkbox.get_attribute("checked") is not None
                    except:
                        esta_publicado = False

                    self.propiedades.append({
                        "ref": ref,
                        "publicado_web": esta_publicado,
                        "capturado_el": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as row_e:
                    print("Error en una fila: " + str(row_e))
            
            print("Pagina procesada. Total acumulado: " + str(len(self.propiedades)))
            return True
        except Exception as e:
            print("Error extrayendo pagina: " + str(e))
            return False

    def siguiente_pagina(self):
        try:
            # El botón "Siguiente" suele tener clase 'next'
            next_btn = self.driver.find_element(By.CSS_SELECTOR, "a.next")
            if "disabled" in next_btn.get_attribute("class") or not next_btn.is_enabled():
                return False
            
            print("Pasando a la siguiente pagina...")
            next_btn.click()
            time.sleep(4)
            return True
        except:
            return False

    def guardar(self):
        os.makedirs('data', exist_ok=True)
        path = 'data/inmoweb_full_sync.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.propiedades, f, indent=2, ensure_ascii=False)
        print("Datos guardados en " + path)

    def cerrar(self):
        if self.driver:
            self.driver.quit()

def main():
    bot = InmowebScrapper()
    try:
        bot.iniciar_navegador(headless=True)
        if bot.login():
            bot.navegar_a_propiedades()
            
            while True:
                bot.extraer_pagina_actual()
                if not bot.siguiente_pagina():
                    break
            
            bot.guardar()
    finally:
        bot.cerrar()

if __name__ == "__main__":
    main()
