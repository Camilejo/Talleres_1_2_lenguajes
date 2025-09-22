@echo off
echo ================================================
echo    INSTALACION AUTOMATICA - TALLERES AUTOMATAS
echo ================================================
echo.
echo Creando entorno virtual...
python -m venv .venv

echo.
echo Activando entorno virtual...
call .venv\Scripts\activate

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ================================================
echo    INSTALACION COMPLETADA EXITOSAMENTE
echo ================================================
echo.
echo Para usar el proyecto:
echo 1. Activa el entorno: .venv\Scripts\activate
echo 2. Ejecuta cualquier automata: python at1ej1.py
echo.
pause