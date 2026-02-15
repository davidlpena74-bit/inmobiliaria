# 🏠 Scraper Completo de Idealista - Proyecto UNED

Scraper profesional de Idealista con **paginación automática**, **bloqueo de imágenes** y **soporte para proxy DataImpulse**.

## ✨ Características Principales

### 🎯 Paginación Completa
- ✅ Obtiene **TODAS las propiedades** disponibles (ej: 345 en Vicálvaro)
- ✅ Navegación automática entre páginas
- ✅ Detección automática del total de propiedades

### ⚡ Optimizaciones de Rendimiento
- ✅ **Bloqueo de imágenes** → Reduce ancho de banda ~70%
- ✅ **Accesos ligeros** → Scraping ~3x más rápido
- ✅ **Delays aleatorios** → Comportamiento humano
- ✅ **Scroll suave** → Evita detección de bots

### 🔒 Proxy DataImpulse
- ✅ Soporte completo para VPN DataImpulse
- ✅ Evita bloqueos de IP
- ✅ Rotación automática de IPs
- ✅ Scraping continuo sin interrupciones

### 📊 Extracción de Datos
- Precio (€)
- Superficie (m²)
- Precio/m² (calculado)
- Habitaciones
- Baños
- Título/Dirección
- Descripción
- URL del anuncio
- Metadata (zona, ciudad, fecha)

---

## 🚀 Instalación

### 1. Instalar Python
Si no tienes Python instalado:
- Descarga desde: https://www.python.org/downloads/
- **Importante**: Marca "Add Python to PATH" durante la instalación

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar ChromeDriver

El scraper usa Selenium con Chrome. Opciones:

**Opción A - Automática (Recomendada):**
```bash
pip install webdriver-manager
```

**Opción B - Manual:**
1. Descarga ChromeDriver: https://chromedriver.chromium.org/
2. Colócalo en la carpeta del proyecto o en PATH

---

## ⚙️ Configuración

### Archivo `config.py`

Edita `config.py` para configurar el scraper:

```python
# Zona a scrapear
ZONA = "vicalvaro"  # Cambia a cualquier zona de Madrid
CIUDAD = "madrid"
TIPO = "venta"  # o "alquiler"

# Límite de páginas
MAX_PAGINAS = None  # None = todas, o un número (ej: 5)

# Modo headless
HEADLESS = False  # True = sin interfaz gráfica

# ========================================
# PROXY DataImpulse (OPCIONAL)
# ========================================
USAR_PROXY = False  # Cambia a True para activar

# Tus credenciales de DataImpulse
PROXY_HOST = "gate.dataimpulse.com"
PROXY_PORT = "823"
PROXY_USER = "tu_usuario"
PROXY_PASS = "tu_contraseña"
```

### Configuración de Proxy DataImpulse

Si tienes cuenta en DataImpulse:

1. Obtén tus credenciales en https://dataimpulse.com
2. Edita `config.py`:
   ```python
   USAR_PROXY = True
   PROXY_USER = "tu_usuario_real"
   PROXY_PASS = "tu_contraseña_real"
   ```
3. Ejecuta el scraper normalmente

**Beneficios del proxy:**
- ✅ Evita bloqueos de IP
- ✅ Permite scraping masivo
- ✅ Rotación automática de IPs
- ✅ Mayor tasa de éxito

---

## 🎯 Uso

### Ejecución Básica

```bash
python scraper_selenium_completo.py
```

Esto:
1. Lee la configuración de `config.py`
2. Inicia Chrome (con imágenes bloqueadas)
3. Navega por TODAS las páginas de Vicálvaro
4. Extrae las **345 propiedades** (o las que haya)
5. Guarda en CSV, JSON y Excel

### Ejemplos de Configuración

#### Ejemplo 1: Scrapear Vicálvaro completo (345 propiedades)
```python
ZONA = "vicalvaro"
MAX_PAGINAS = None  # Todas las páginas
```

#### Ejemplo 2: Solo primeras 3 páginas (~45 propiedades)
```python
ZONA = "vicalvaro"
MAX_PAGINAS = 3
```

#### Ejemplo 3: Chamberí con proxy
```python
ZONA = "chamberi"
MAX_PAGINAS = None
USAR_PROXY = True
```

#### Ejemplo 4: Alquiler en Salamanca
```python
ZONA = "salamanca"
TIPO = "alquiler"
MAX_PAGINAS = 5
```

---

## 📊 Salida de Datos

Los datos se guardan en `datos/` con timestamp:

```
datos/
├── idealista_vicalvaro_venta_20260214_133000.csv
├── idealista_vicalvaro_venta_20260214_133000.json
└── idealista_vicalvaro_venta_20260214_133000.xlsx
```

### Formato CSV

```csv
titulo,precio,m2,precio_m2,habitaciones,banos,detalles,descripcion,url,zona,ciudad,tipo,fecha_extraccion
"Piso en Calle...",215000,75,2866.67,3,2,"3 hab., 75 m²,...","Piso reformado...","https://...","Vicálvaro","Madrid","venta","2026-02-14 13:30:00"
```

---

## 🎓 Zonas Disponibles en Madrid

Puedes scrapear cualquiera de estas zonas cambiando `ZONA` en `config.py`:

- `vicalvaro` (345 propiedades)
- `chamberi`
- `salamanca`
- `retiro`
- `centro`
- `chamartin`
- `moncloa-aravaca`
- `ciudad-lineal`
- `hortaleza`
- `tetuan`
- `arganzuela`
- `carabanchel`
- `usera`
- `puente-de-vallecas`
- `moratalaz`
- `latina`
- `fuencarral-el-pardo`
- `villa-de-vallecas`
- `san-blas-canillejas`
- `barajas`

---

## 🔧 Solución de Problemas

### Error: "ChromeDriver not found"
```bash
pip install webdriver-manager
```

### Error: "Selenium not installed"
```bash
pip install selenium
```

### Error 403 (Acceso bloqueado)
- **Solución 1**: Activa el proxy DataImpulse
- **Solución 2**: Aumenta los delays en `config.py`
- **Solución 3**: Reduce `MAX_PAGINAS`

### El scraper es muy lento
- ✅ Las imágenes ya están bloqueadas por defecto
- ✅ Activa modo headless: `HEADLESS = True`
- ✅ Usa proxy para evitar CAPTCHAs

### No encuentra propiedades
- Verifica que la zona existe en Idealista
- Comprueba la URL manualmente
- Revisa los selectores CSS (pueden cambiar)

---

## 📈 Análisis de Rentabilidad

Una vez tengas los datos, puedes:

### 1. Comparar Compra vs Alquiler

```python
# Scrapear venta
TIPO = "venta"
python scraper_selenium_completo.py

# Scrapear alquiler
TIPO = "alquiler"
python scraper_selenium_completo.py

# Calcular ratio precio/alquiler en Excel o Python
```

### 2. Análisis por Zonas

Scrapea múltiples zonas y compara:
- Precio/m² medio por zona
- Rentabilidad (ratio compra/alquiler)
- Zonas con mejor relación calidad/precio

### 3. Exportar a Google Sheets

Usa `exportar_google_sheets.html` para visualizar y analizar los datos.

---

## ⚠️ Consideraciones Éticas y Legales

### ✅ Buenas Prácticas Implementadas

1. **Delays aleatorios** entre peticiones (2-7 segundos)
2. **Scroll suave** para simular comportamiento humano
3. **User-Agent realista** para no parecer bot
4. **Bloqueo de imágenes** para reducir carga en servidores
5. **Respeto a robots.txt** (uso académico)

### ⚠️ Limitaciones

- **Uso académico exclusivamente** (UNED - Ciencia de Datos)
- **No usar con fines comerciales**
- **Respetar los términos de servicio de Idealista**
- **No sobrecargar los servidores** (usa delays apropiados)

### 💡 Alternativa Recomendada

**Solicita acceso a la API oficial de Idealista:**
- Más estable y confiable
- Datos estructurados en JSON
- Sin riesgo de bloqueos
- Soporte oficial

Usa este proyecto como justificación para tu solicitud.

---

## 📚 Próximos Pasos

1. ✅ **Ejecuta el scraper** con Vicálvaro
2. ✅ **Exporta a Google Sheets** para análisis
3. ✅ **Amplía a más zonas** de Madrid
4. ✅ **Scrapea alquiler** para calcular rentabilidad
5. ✅ **Solicita la API** de Idealista con este proyecto

---

## 🤝 Soporte

**Proyecto académico** - UNED  
Grado en Ingeniería Informática (Ciencia de Datos)

---

## 📝 Changelog

### v2.0 (2026-02-14)
- ✅ Paginación automática completa (345 propiedades)
- ✅ Bloqueo de imágenes (acceso ligero)
- ✅ Soporte para proxy DataImpulse
- ✅ Archivo de configuración centralizado
- ✅ Optimizaciones de rendimiento

### v1.0 (2026-02-14)
- ✅ Scraper básico con BeautifulSoup
- ✅ Exportación a CSV/JSON/Excel
- ✅ Datos de ejemplo

---

**¡Disfruta analizando el mercado inmobiliario de Madrid! 🏠📊**
