import sys
import os

# Añadir el directorio raíz al path para poder importar supabase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase_utils import SupabaseClient
import re

# Configurar salida UTF-8 para consola Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def clean_rental_titles():
    print("🔄 Iniciando limpieza de títulos de propiedades...")
    client = SupabaseClient()
    
    try:
        # 1. Obtener todas las propiedades
        response = client.client.table("inm_propiedades").select("id, titulo").execute()
        props = response.data
        
        if not props:
            print("⚠️ No hay propiedades en la base de datos.")
            return

        print(f"📊 Procesando {len(props)} propiedades...")
        updated_count = 0
        
        for p in props:
            original_title = p.get('titulo', '')
            if not original_title:
                continue
                
            # Limpiar ", for rent" y ", for sale"
            # Usando regex para ser robustos con espacios
            new_title = re.sub(r',\s*for\s*rent', '', original_title, flags=re.IGNORECASE)
            new_title = re.sub(r',\s*for\s*sale', '', new_title, flags=re.IGNORECASE)
            new_title = new_title.strip()
            
            if new_title != original_title:
                # Actualizar en Supabase
                try:
                    client.client.table("inm_propiedades").update({"titulo": new_title}).eq("id", p['id']).execute()
                    print(f"   ✅ Actualizado ID {p['id']}: '{original_title}' -> '{new_title}'")
                    updated_count += 1
                except Exception as e:
                    print(f"   ❌ Error actualizando ID {p['id']}: {e}")
                    
        print(f"\n✨ Proceso completado. Se actualizaron {updated_count} propiedades.")

    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    clean_rental_titles()
