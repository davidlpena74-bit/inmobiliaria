"""
Scrapper_Weperti.py
===================
Agente para extraer las propiedades actualmente publicadas en la web weperti.com.
Permite identificar qué inmuebles están "al aire".
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
import config

class WepertiScrapper:
    def __init__(self):
        self.base_url = config.WEPERTI_URL
        # Usualmente la búsqueda está en una URL específica, intentamos la raíz o /buscar
        self.search_url = f"{self.base_url}/inmuebles/madrid/" # Ajustar según necesidad
        self.propiedades = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def scrape_published(self):
        print(f"🌐 Accediendo a la web pública: {self.base_url}...")
        try:
            # En weperti.com, la búsqueda parece estar integrada. 
            # Intentamos obtener la página principal o la de inmuebles.
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"❌ Error al acceder a la web (Status: {response.status_code})")
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Selectores identificados por el subagente:
            # Card: .resultados .row > div.punto_mapa
            items = soup.select(".resultados .row div.punto_mapa")
            
            if not items:
                # Intento alternativo (si están en otra subpágina)
                print("⚠️ No se encontraron items en la Home. Reintentando en /inmuebles/...")
                response = requests.get(f"{self.base_url}/inmuebles/", headers=self.headers, timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.select(".resultados .row div.punto_mapa")

            print(f"🏠 Encontrados {len(items)} anuncios publicados.")
            
            for item in items:
                try:
                    ref_elem = item.select_one(".referencia .numeroRef")
                    title_elem = item.select_one(".subTitulo a")
                    price_elem = item.select_one(".precio .actual")
                    
                    if ref_elem and title_elem:
                        ref = ref_elem.text.strip().replace("Ref: ", "")
                        propiedad = {
                            "ref": ref,
                            "titulo": title_elem.text.strip(),
                            "url": title_elem.get("href"),
                            "precio": price_elem.text.strip() if price_elem else "",
                            "fecha_scrapping": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "fuente": "Weperti Pública"
                        }
                        self.propiedades.append(propiedad)
                except Exception as e:
                    print(f"⚠️ Error procesando item: {e}")
                    continue
                    
            return True
        except Exception as e:
            print(f"❌ Error durante el scrapping: {e}")
            return False

    def guardar_datos(self):
        os.makedirs('data', exist_ok=True)
        filename = 'data/weperti_published.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.propiedades, f, indent=2, ensure_ascii=False)
        print(f"💾 Guardados {len(self.propiedades)} inmuebles publicados en {filename}")

def main():
    scrapper = WepertiScrapper()
    if scrapper.scrape_published():
        scrapper.guardar_datos()

if __name__ == "__main__":
    main()
