@echo off
echo ==========================================
echo 🚀 Desplegando Weperty (Web + CRM)
echo ==========================================

echo Selecciona el tipo de despliegue:
echo [A] Mayor (funcional mayor)
echo [B] Menor (funcional medio)
echo [C] Parche (funcional menor, estético, errores)
set /p TIPO_VER="> "

echo 🔄 Incrementando version...
python version_manager.py %TIPO_VER%

echo ➕ Añadiendo archivos del proyecto...
git add -A .

echo 🔄 Guardando cambios y subiendo a GitHub...
git commit -m "Despliegue automatico - Actualizacion de version"
git push

if %ERRORLEVEL% EQU 0 (
    echo ✅ Despliegue completado con exito.
    echo 🌐 Web Publica: https://weperty.com/
    echo 🔒 CRM Administrador: https://weperty.com/crm/login.html
) else (
    echo ⚠️ Hubo un error al subir a GitHub. Verifica tu conexion.
)

pause
