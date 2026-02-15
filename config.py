"""
Configuración del Scraper de Idealista
======================================
Archivo de configuración centralizado para el scraper
"""

# ========================================
# CONFIGURACIÓN GENERAL
# ========================================
ZONA = "vicalvaro"
CIUDAD = "madrid"
TIPO = "venta"  # "venta" o "alquiler"

# Límite de páginas a scrapear (None = todas las páginas)
MAX_PAGINAS = None  # Cambia a un número para limitar (ej: 5)

# Modo headless (sin interfaz gráfica)
HEADLESS = False  # True para ejecutar en segundo plano

# ========================================
# OPTIMIZACIONES
# ========================================
# Las imágenes están bloqueadas por defecto para accesos ligeros
# Esto reduce el ancho de banda en ~70% y acelera el scraping ~3x

# ========================================
# CONFIGURACIÓN DE SUPABASE
# ========================================
# Necesitas crear un proyecto en supabase.com
USAR_SUPABASE = True  # Cambia a False si no quieres subir a la nube
SUPABASE_URL = "https://dwbvegnxmyvpolvofkfn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3YnZlZ254bXl2cG9sdm9ma2ZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc1Mzg1NTUsImV4cCI6MjA4MzExNDU1NX0.eT5ZSce8H8Yk8pWKyLUYChU0HtmZljywP4eEQd5FkOI"

# ========================================
# CONFIGURACIÓN DE PROXY (DataImpulse)
# ========================================
# Activa el proxy para evitar bloqueos y rotar IPs

# ========================================
# CONFIGURACIÓN DE PROXY (DataImpulse)
# ========================================
# Activa el proxy para evitar bloqueos y rotar IPs

USAR_PROXY = True  # Activado para rotación de IPs

# Credenciales de DataImpulse
# Formato: gw.dataimpulse.com:823
PROXY_HOST = "gw.dataimpulse.com"    # Host del proxy
PROXY_PORT = "823"                    # Puerto del proxy
PROXY_USER_BASE = "43eae80e80002d6d67b2" # Usuario base de DataImpulse
PROXY_PASS = "4a8d1549c089df41"          # Contraseña de DataImpulse

# La rotación de IPs se hace añadiendo __session-RANDOM al usuario
# Esto se manejará en el scraper

# ========================================
# DELAYS Y TIMING
# ========================================
# Delays entre peticiones (en segundos)
DELAY_MIN = 2.0  # Mínimo
DELAY_MAX = 5.0  # Máximo

# Delay entre páginas (más largo para ser respetuoso)
DELAY_PAGINA_MIN = 4.0
DELAY_PAGINA_MAX = 7.0

# ========================================
# EXPORTACIÓN
# ========================================
# Formatos de exportación
EXPORTAR_CSV = True
EXPORTAR_JSON = True
EXPORTAR_EXCEL = True

# ========================================
# ZONAS DISPONIBLES EN MADRID
# ========================================
# Puedes cambiar ZONA a cualquiera de estas:
ZONAS_MADRID = [
    "vicalvaro",
    "chamberi",
    "salamanca",
    "retiro",
    "centro",
    "chamartin",
    "moncloa-aravaca",
    "ciudad-lineal",
    "hortaleza",
    "tetuan",
    "arganzuela",
    "carabanchel",
    "usera",
    "puente-de-vallecas",
    "moratalaz",
    "latina",
    "fuencarral-el-pardo",
    "villa-de-vallecas",
    "vicalvaro",
    "san-blas-canillejas",
    "barajas"
]

# ========================================
# NOTAS IMPORTANTES
# ========================================
"""
1. PROXY DataImpulse:
   - Evita bloqueos de IP
   - Permite scraping continuo
   - Rotar IPs automáticamente
   - Necesitas cuenta en DataImpulse

2. BLOQUEO DE IMÁGENES:
   - Activado por defecto
   - Reduce ancho de banda ~70%
   - Acelera scraping ~3x
   - No afecta extracción de datos

3. LÍMITE DE PÁGINAS:
   - None = todas las páginas (ej: 345 propiedades)
   - Número = límite de páginas (ej: 5 páginas = ~75 propiedades)
   - Recomendado empezar con 2-3 páginas para probar

4. HEADLESS MODE:
   - True = sin interfaz gráfica (más rápido)
   - False = ver el navegador (útil para debugging)
"""
