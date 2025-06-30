# API Backend

Proyecto backend con FastAPI y Docker.

## Requisitos

- Docker
- Docker Compose

## Instalación

1. Clonar el repositorio
2. Configurar el archivo .env (usar .env.example como guía)
3. Configurar el archivo .env (usar .env.example como guía)

   - Configurar las variables de base de datos (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
   - Configurar las variables de correo electrónico (MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_FROM_NAME)

4. Ejecutar Docker Compose:

```bash
docker-compose up -d
```

4. Crear y ejecutar las migraciones:

```bash
Crear
En dev-container
alembic revision --autogenerate -m "descripción: Por ejemplo, 'create users table'"

docker-compose exec app alembic revision --autogenerate -m "descripción: Por ejemplo, 'create users table'"

```

```bash
docker-compose exec app alembic upgrade head

En dev-container
alembic upgrade head
```

5. (Opcional) Poblar la base de datos con datos de prueba:

```bash
docker-compose exec app bash -c "PYTHONPATH=/app python app/modules/common/seeder/seeder.py"
```

> **_NOTE:_** Si estamos en un dev container, ejecutamos `python -m app.modules.common.seeder.seeder`

## Configuración de Variables de Entorno

El proyecto utiliza un archivo `.env` para la configuración. Copia el archivo `.env.example` a `.env` y configura las siguientes variables:

### Variables de Base de Datos

- `DB_HOST`: Host de la base de datos (por defecto en docker: db)
- `DB_PORT`: Puerto de la base de datos (por defecto: 3306)
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_NAME`: Nombre de la base de datos
- `DATABASE_URL`: URL de conexión a la base de datos (se genera automáticamente)

### Variables de JWT

- `SECRET_KEY`: Clave secreta para JWT
- `ALGORITHM`: Algoritmo de encriptación (por defecto: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token en minutos

### Variables de la API

- `PROJECT_NAME`: Nombre del proyecto
- `PROJECT_DESCRIPTION`: Descripción del proyecto
- `PROJECT_VERSION`: Versión del proyecto

### Variables de Entorno

- `DEBUG`: Modo debug (True/False)
- `ENVIRONMENT`: Entorno de ejecución (development/production)

## Desarrollo

La API estará disponible en: http://localhost:8000

Documentación de la API en: http://localhost:8000/docs

## Estructura del Proyecto

```
.
├── app
│   ├── config          # Configuración de la aplicación
│   ├── libraries       # Bibliotecas y utilidades
│   ├── modules         # Módulos de la aplicación
│   │   ├── auth        # Módulo de autenticación
│   │   │   ├── models      # Modelos de datos
│   │   │   ├── repositories # Repositorios para acceso a datos
│   │   │   ├── routes      # Rutas de la API
│   │   │   ├── schemas     # Esquemas de datos
│   │   │   └── dependencies.py # Dependencias del módulo
│   │   ├── common      # Módulo común
│   │   │   ├── router      # Router principal
│   │   │   ├── schemas     # Esquemas comunes
│   │   │   └── seeder      # Datos de prueba
│   │   └── ...         # Otros módulos (Products, Users, etc.)
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Comandos importantes

- Para crear los archivos de traducción

```bash
docker-compose exec app bash -c "PYTHONPATH=/app python app/config/translations/convert_translations.py"

En dev-container:
`python -m app.config.translations.convert_translations`
```

## Accesos

Usuario: dfalco@dsdiagram.es
Contraseña: password

Usuario: gabriel@diagram.es
Contraseña: password
