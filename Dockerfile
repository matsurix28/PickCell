FROM python:3.11.6

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    libmtdev-dev \
    && pip install --upgrade pip \
    && pip install --user --upgrade \
    opencv-python \
    isort \
    plotly \
    easyocr \
    kivy \
    Cython==0.29.33 \
    virtualenv \
    && echo 'export PATH=$PATH:~/.local/bin/' >> ~/.bashrc