FROM python:3.13-slim

ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=1000

# Crear usuario no root con UID y GID reales
RUN groupadd --gid ${USER_GID} ${USERNAME} \
  && useradd --uid ${USER_UID} --gid ${USER_GID} -m -s /bin/bash ${USERNAME}

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
  bash \
  build-essential \
  gcc \
  git \
  libffi-dev \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libxml2 \
  libxslt1.1 \
  shared-mime-info \
  curl \
  gettext \
  && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements.txt y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Crear directorio para alembic y cambiar permisos de /app
RUN mkdir -p /app/alembic/versions \
  && chown -R ${USERNAME}:${USERNAME} /app

# Cambiar a usuario no root
USER ${USERNAME}

# Stage de desarrollo
FROM python:3.13-slim as development

ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=1000

# Crear usuario no root
RUN groupadd --gid ${USER_GID} ${USERNAME} \
  && useradd --uid ${USER_UID} --gid ${USER_GID} -m -s /bin/bash ${USERNAME}

WORKDIR /app

# Instalar dependencias del sistema y watchfiles para hot reload
RUN apt-get update && apt-get install -y \
  bash \
  build-essential \
  gcc \
  git \
  libffi-dev \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libxml2 \
  libxslt1.1 \
  shared-mime-info \
  curl \
  gettext \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir watchfiles

# Crear directorios necesarios
RUN mkdir -p /app/alembic/versions \
  && chown -R ${USERNAME}:${USERNAME} /app

# Cambiar a usuario no root
USER ${USERNAME}

# Comando por defecto - el código se monta via volumen
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--timeout-keep-alive", "30", "--limit-concurrency", "1000", "--backlog", "2048"]
