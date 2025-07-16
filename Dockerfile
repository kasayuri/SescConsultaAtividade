# Use a imagem base do Python fornecida pelo DevContainer
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgbm1 \
    libpangoft2-1.0-0 \
    libjpeg-dev \
    libxshmfence1 \
    xdg-utils \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Microsoft Edge
RUN wget https://packages.microsoft.com/keys/microsoft.asc -qO - | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" && \
    apt-get update && apt-get install -y microsoft-edge-stable

# Instalar o Edge WebDriver
RUN wget -q https://msedgedriver.azureedge.net/$(microsoft-edge --version | awk '{print $3}')/edgedriver_linux64.zip && \
    unzip edgedriver_linux64.zip && \
    mv msedgedriver /usr/local/bin/ && \
    rm edgedriver_linux64.zip

# Instalar firefox para testes Jules
RUN apt-get update && apt-get install -y firefox-esr

# Definir o diretório de trabalho
WORKDIR /workspaces/SescConsultaAtividade

# Instalar dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt
