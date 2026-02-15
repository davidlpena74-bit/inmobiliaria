import os
from supabase import create_client, Client
import config

# Inicializar cliente de Supabase
supabase_url = config.SUPABASE_URL
supabase_key = config.SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

# Nombres de las tablas con prefijo del proyecto
TBL_MUNICIPIOS = "inm_municipios"
TBL_PROPIEDADES = "inm_propiedades"

def upsert_municipio(data):
    """Inserta o actualiza un municipio en inm_municipios"""
    try:
        response = supabase.table(TBL_MUNICIPIOS).upsert(data, on_conflict="nombre").execute()
        return response
    except Exception as e:
        print(f"Error Supabase (municipio): {e}")
        return None

def insert_propiedad(data):
    """Inserta una propiedad en inm_propiedades vinculada a su municipio"""
    try:
        # Primero intentamos buscar el ID del municipio por nombre
        mun_name = data.get('zona')
        if mun_name:
            mun_res = supabase.table(TBL_MUNICIPIOS).select("id").eq("nombre", mun_name).execute()
            if mun_res.data:
                data['municipio_id'] = mun_res.data[0]['id']

        response = supabase.table(TBL_PROPIEDADES).upsert(data, on_conflict="url").execute()
        return response
    except Exception as e:
        print(f"Error Supabase (propiedad): {e}")
        return None

def get_all_municipios():
    """Obtiene todos los municipios para el mapa/dashboard"""
    try:
        response = supabase.table(TBL_MUNICIPIOS).select("*").order("nombre").execute()
        return response.data
    except Exception as e:
        print(f"Error obtener municipios: {e}")
        return []

class SupabaseClient:
    """Clase wrapper para operaciones de Supabase"""
    
    def __init__(self):
        self.client = supabase
        
    def upsert_municipio(self, data):
        """Inserta o actualiza un municipio"""
        return upsert_municipio(data)
    
    def insert_propiedad(self, data):
        """Inserta una propiedad"""
        return insert_propiedad(data)
    
    def get_all_municipios(self):
        """Obtiene todos los municipios"""
        return get_all_municipios()
