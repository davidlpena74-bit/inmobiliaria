@echo off
echo ==========================================
echo 🚀 Desplegando Weperty (Web + CRM)
echo ==========================================

echo ➕ Añadiendo archivos del proyecto...
git add -A .

echo 🔄 Guardando cambios con marca Weperty...
git commit -m "Identidad visual integrada: Logo corporativo en Landing, Login y CRM"

echo ⬆️ Subiendo a GitHub...
git push

if %ERRORLEVEL% EQU 0 (
    echo ✅ Despliegue completado con exito.
    echo 🌐 Web Publica: https://weperty.com/
    echo 🔒 CRM Administrador: https://weperty.com/crm/login.html
) else (
    echo ⚠️ Hubo un error al subir a GitHub. Verifica tu conexion.
)

pause
