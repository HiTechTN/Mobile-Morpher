FROM python:3.10-slim-bookworm

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Installation d'Apktool v3.0.2 et Android SDK (apksigner)
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/build-tools/36.0.0

RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/cmdline-tools.zip && \
    unzip -q /tmp/cmdline-tools.zip -d $ANDROID_HOME/cmdline-tools && \
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    yes | sdkmanager --licenses > /dev/null 2>&1 && \
    sdkmanager "build-tools;36.0.0" > /dev/null 2>&1 && \
    rm -rf /tmp/cmdline-tools.zip $ANDROID_HOME/cmdline-tools/latest/packages.xml && \
    wget -q https://github.com/iBotPeaches/Apktool/releases/download/v3.0.2/apktool_3.0.2.jar -O /usr/local/bin/apktool.jar && \
    wget -q https://raw.githubusercontent.com/iBotPeaches/Apktool/refs/heads/main/scripts/linux/apktool -O /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

WORKDIR /app

# Copie des requirements et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
