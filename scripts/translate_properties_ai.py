import os
import sys
import time
import json

# Añadir el raíz del proyecto al path para importar config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from supabase import create_client, Client
from deep_translator import GoogleTranslator

# Configuración de Supabase
supabase_url = config.SUPABASE_URL
supabase_key = config.SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

# Idiomas objetivo
LANGS = ["en", "de", "nl"]

def translate_text(text, target_lang):
    """Traduce un texto usando Google Translator (vía deep-translator)"""
    if not text or len(text.strip()) == 0:
        return ""
    try:
        # GoogleTranslator detecta automáticamente el idioma de origen (probablemente 'es')
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Error traduciendo a {target_lang}: {e}")
        return None

def process_translations():
    """Busca propiedades en Supabase y genera sus traducciones si faltan"""
    print("--- Iniciando proceso de traducción dinámica ---")
    
    # 1. Obtener propiedades que necesitan traducción
    # Seleccionamos las que tienen el campo 'traducciones' vacío o incompleto
    response = supabase.table("inm_propiedades").select("id, titulo, descripcion, traducciones").execute()
    propiedades = response.data

    if not propiedades:
        print("No se encontraron propiedades para procesar.")
        return

    count = 0
    for p in propiedades:
        p_id = p['id']
        titulo_base = p['titulo']
        desc_base = p['descripcion']
        traducciones_actuales = p.get('traducciones') or {}
        
        needs_update = False
        
        for lang in LANGS:
            if lang not in traducciones_actuales:
                print(f"Traduciendo propiedad ID {p_id} al {lang}...")
                
                titulo_trans = translate_text(titulo_base, lang)
                desc_trans = translate_text(desc_base, lang)
                
                if titulo_trans and desc_trans:
                    traducciones_actuales[lang] = {
                        "titulo": titulo_trans,
                        "descripcion": desc_trans
                    }
                    needs_update = True
                    # Pequeño delay para evitar bloqueos por rate limiting
                    time.sleep(1)
        
        if needs_update:
            # 2. Actualizar en Supabase
            try:
                supabase.table("inm_propiedades").update({"traducciones": traducciones_actuales}).eq("id", p_id).execute()
                print(f"Propiedad ID {p_id} actualizada con éxito.")
                count += 1
            except Exception as e:
                print(f"Error actualizando ID {p_id}: {e}")

    print(f"--- Proceso finalizado. Total de propiedades traducidas/actualizadas: {count} ---")

if __name__ == "__main__":
    process_translations()
