@echo off
echo ==========================================
echo 🚀 Desplegando Dashboard Inmobiliario (Limpieza Total)
echo ==========================================

REM 1. Definir rutas
set SOURCE_HTML="precios_distritos_madrid.html"
set WEB_PROJECT_DIR="."
set TARGET_ROOT="inmobiliaria.html"
set TARGET_PUBLIC="public\inmobiliaria.html"

REM 2. Copiar archivo HTML actualizado
echo 📂 Copiando archivos...
REM copy /Y %SOURCE_HTML% %WEB_PROJECT_DIR%\%TARGET_ROOT%
REM copy /Y %SOURCE_HTML% %WEB_PROJECT_DIR%\%TARGET_PUBLIC%

REM 3. Entrar al directorio y limpiar commits sucios
echo 🔄 Limpiando Repositorio Git...
REM cd /d %WEB_PROJECT_DIR%

REM Deshacer el ultimo commit local (manteniendo cambios en local pero quitandolos del commit)
REM git reset --soft HEAD~1
REM git reset

REM Limpiar cualquier rastro de archivos no deseados del index
REM Solo queremos subir el dashboard. El resto se quedar en local sin commitear.

echo ➕ Añadiendo SOLO el dashboard...
git add %SOURCE_HTML%

REM Commit limpio
git commit -m "Actualizacion dashboard inmobiliario"

REM Push
echo ⬆️ Subiendo a GitHub...
git push

if %ERRORLEVEL% EQU 0 (
    echo ✅ Despliegue completado con exito.
    echo 🌐 Visita: https://davidlpena74-bit.github.io/inmobiliaria/
) else (
    echo ⚠️ Hubo un error al subir a GitHub. Verifica si aun quedan secretos.
)

pause
