import os
from supabase import create_client, Client

SUPABASE_URL = "https://dwbvegnxmyvpolvofkfn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3YnZlZ254bXl2cG9sdm9ma2ZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc1Mzg1NTUsImV4cCI6MjA4MzExNDU1NX0.eT5ZSce8H8Yk8pWKyLUYChU0HtmZljywP4eEQd5FkOI"

def main():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Actualizar todas las propiedades que tengan el agente antiguo
    print("Actualizando propiedades en Supabase...")
    response = supabase.table("inm_propiedades") \
        .update({"agente": "Weperty Properties"}) \
        .eq("agente", "info@weperti.com") \
        .execute()
    
    print(f"Propiedades actualizadas: {len(response.data)}")

if __name__ == "__main__":
    main()
