FROM quay.io/astronomer/astro-runtime:12.8.0

USER root

# Instalar dependencias y Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

# Verificar instalaciones y mostrar versiones
RUN echo "📋 Verificando instalaciones:" && \
    chromium --version && \
    chromedriver --version

# Configurar ChromeDriver con permisos correctos para usuario astro
RUN mkdir -p /opt/chromedriver && \
    cp /usr/bin/chromedriver /opt/chromedriver/chromedriver && \
    chmod 755 /opt/chromedriver/chromedriver && \
    chown -R astro:astro /opt/chromedriver && \
    echo "✅ ChromeDriver configurado con permisos:" && \
    ls -la /opt/chromedriver/

# Variables de entorno
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/opt/chromedriver/chromedriver
ENV DISPLAY=:99

# Verificar permisos antes de cambiar usuario
RUN echo "🔍 Verificando permisos finales:" && \
    ls -la /opt/chromedriver/ && \
    echo "Usuario astro puede ejecutar:" && \
    su - astro -c "/opt/chromedriver/chromedriver --version" || echo "Error de permisos detectado"

USER astro