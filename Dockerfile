FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    git \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    liblzma-dev \
    libgdbm-dev \
    libnss3-dev \
    libgdbm-compat-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Python 3.13
WORKDIR /usr/src
RUN curl -O https://www.python.org/ftp/python/3.13.0/Python-3.13.0a6.tgz && \
    tar -xf Python-3.13.0a6.tgz && \
    cd Python-3.13.0a6 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall


RUN ln -s /usr/local/bin/python3.13 /usr/bin/python && \
    ln -s /usr/local/bin/pip3.13 /usr/bin/pip

WORKDIR /app
COPY . /app

RUN pip3.13 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3.13", "/app/app.py"]