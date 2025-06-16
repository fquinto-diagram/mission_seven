#!/bin/bash

# Comandos que requieren el código fuente (se ejecutan cuando el código está montado)
echo "Inicializando aplicación..."

# Convertir traducciones si existen
if [ -f "app/config/translations/convert_translations.py" ]; then
    echo "Convirtiendo traducciones..."
    python -m app.config.translations.convert_translations || echo "No se pudieron convertir las traducciones"
fi

# Dar permisos de ejecución si es necesario
chmod +x start.sh 2>/dev/null || true

echo "Iniciando aplicación..."

if [ "$ENVIRONMENT" = "production" ]; then
    gunicorn -c gunicorn.conf.py app.main:app
else
    echo "Modo desarrollo: Hot reload habilitado"
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app --reload-exclude="*.pyc" --reload-exclude="__pycache__" --reload-exclude=".git/objects" --reload-exclude=".git/logs"
fi 