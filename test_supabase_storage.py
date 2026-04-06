import os
from supabase import create_client, Client
import config

def test_storage():
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    test_file = "tmp/test_storage.txt"
    os.makedirs("tmp", exist_ok=True)
    with open(test_file, "w") as f:
        f.write("test content")

    try:
        print(f"--- Intentando subir a bucket 'propiedades' ---")
        with open(test_file, "rb") as f:
            res = supabase.storage.from_("propiedades").upload(
                "connection_test.txt", 
                f, 
                {"content-type": "text/plain", "x-upsert": "true"}
            )
        print(f"✅ ÉXITO: {res}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nRECUERDA: Si ves un error 403, debes ejecutar el SQL del implementation_plan.md en tu dashboard de Supabase.")

if __name__ == "__main__":
    test_storage()
