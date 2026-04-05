# 🤖 Agente de Precios Inmobiliarios - Comunidad de Madrid

## 📋 Descripción

Agente especializado en la búsqueda automática de precios inmobiliarios para **todos los municipios de la Comunidad de Madrid**. El agente realiza scraping de múltiples fuentes (Idealista, Fotocasa, Pisos.com) y actualiza automáticamente la base de datos de Supabase.

## ✨ Características

- 🔍 **Búsqueda automática** en múltiples portales inmobiliarios
- 🌐 **Scraping asíncrono** para mayor velocidad
- 📊 **Cobertura completa** de +180 municipios de la Comunidad de Madrid
- 💾 **Actualización automática** en Supabase
- 📈 **Cálculo de rentabilidad** y ratios de recuperación
- 🛡️ **Manejo de errores** robusto
- ⏱️ **Rate limiting** para evitar bloqueos

## 🚀 Instalación

### 1. Instalar Python (si no lo tienes)

Descarga e instala Python desde: https://www.python.org/downloads/

**IMPORTANTE**: Durante la instalación, marca la opción **"Add Python to PATH"**

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## 📖 Uso

### Opción 1: Búsqueda Completa (Todos los Municipios)

```bash
python agente_precios.py
```

Esto procesará **todos los municipios** de la Comunidad de Madrid. El proceso puede tardar varias horas.

### Opción 2: Búsqueda Limitada (Prueba)

Edita `agente_precios.py` y modifica la línea:

```python
resultados = await agente.ejecutar_busqueda_completa(limite=10)
```

Esto procesará solo los primeros 10 municipios para hacer pruebas.

### Opción 3: Búsqueda de Municipios Específicos

Puedes modificar el código para buscar solo municipios específicos:

```python
agente = PreciosInmobiliariosAgent()
agente.municipios = ["Alcobendas", "Pozuelo-de-Alarcon", "Majadahonda"]
resultados = await agente.ejecutar_busqueda_completa()
```

## 📊 Salida

El agente genera:

1. **Actualización en Supabase**: Los datos se guardan automáticamente en la tabla `inm_municipios`
2. **Archivo JSON**: `resultados_busqueda.json` con todos los datos recopilados
3. **Log en consola**: Progreso en tiempo real de la búsqueda

## 🗂️ Estructura de Datos

Cada municipio procesado contiene:

```json
{
  "municipio": "Alcobendas",
  "precio_venta": 4838,
  "precio_alquiler": 17.8,
  "rentabilidad": 4.42,
  "ratio_recuperacion": 22.6,
  "fuentes": 2,
  "fecha": "2026-02-14T18:53:00"
}
```

## 🌐 Fuentes de Datos

El agente busca en:

1. **Idealista** - Portal líder en España
2. **Fotocasa** - Segunda fuente más importante
3. **Pisos.com** - Fuente complementaria

Los precios se promedian entre todas las fuentes disponibles para mayor precisión.

## ⚙️ Configuración

### Variables de Entorno

Asegúrate de tener configurado `config.py` con tus credenciales de Supabase:

```python
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-api-key"
```

### Rate Limiting

El agente incluye pausas aleatorias entre 2-5 segundos entre municipios para evitar ser bloqueado. Puedes ajustar esto en:

```python
await asyncio.sleep(random.uniform(2, 5))
```

## 📈 Municipios Cubiertos

El agente cubre **+180 municipios** organizados por zonas:

- ✅ **Madrid Capital** (21 distritos)
- ✅ **Zona Norte** (30+ municipios)
- ✅ **Zona Oeste** (40+ municipios)
- ✅ **Zona Sur** (35+ municipios)
- ✅ **Zona Este** (30+ municipios)
- ✅ **Sierra Norte** (25+ municipios)

## 🔧 Solución de Problemas

### Error: "Python no encontrado"

Instala Python y asegúrate de marcar "Add to PATH" durante la instalación.

### Error: "ModuleNotFoundError: No module named 'aiohttp'"

Ejecuta:
```bash
pip install -r requirements.txt
```

### Error: "Supabase connection failed"

Verifica que `config.py` tenga las credenciales correctas de Supabase.

### Pocos datos encontrados

Algunos municipios pequeños pueden no tener suficientes anuncios. Esto es normal.

## 📝 Notas

- El scraping puede ser bloqueado por los portales si se hace muy frecuentemente
- Se recomienda ejecutar el agente **máximo 1 vez al día**
- Los precios son aproximados y pueden variar según la fuente
- El agente respeta los `robots.txt` y usa rate limiting

## 🎯 Próximas Mejoras

- [ ] Integración con API oficial de Idealista
- [ ] Scraping de datos históricos
- [ ] Detección automática de tendencias
- [ ] Alertas de oportunidades de inversión
- [ ] Exportación a Excel/CSV

## 📞 Soporte

Si encuentras algún problema, revisa:
1. Que Python esté instalado correctamente
2. Que todas las dependencias estén instaladas
3. Que las credenciales de Supabase sean correctas
4. Que tengas conexión a Internet

---

**Desarrollado para WEPERTY REAL ESTATE** 🏠
