FROM python:3.11.6-slim

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    git \
    tk-dev \
    libsm6 

RUN pip install \
    opencv-python \
    easyocr \
    matplotlib \
    tkinterdnd2 \
    isort \
    tkhtmlview \
    plotly
