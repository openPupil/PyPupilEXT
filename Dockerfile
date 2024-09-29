# Use an Ubuntu base image
FROM --platform=linux/amd64 ubuntu:22.04

# Set environment variables to avoid interaction
ENV DEBIAN_FRONTEND=noninteractive

# Install essential packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    git \
    build-essential \
    cmake \
    g++ \
    gcc \
    make \
    curl \
    zip \
    unzip \
    tar \
    pkg-config \
    libopencv-dev \
    ninja-build \
    autoconf \
    automake \
    libtool \
    bison \
    gperf \
    libx11-dev \
    libxft-dev \
    libxext-dev \
    libegl1-mesa-dev \
    libgles2-mesa-dev \
    libxrandr-dev \
    libglib2.0-dev \
    libxrandr-dev \
    libxcursor-dev \
    libxinerama-dev \
    libxi-dev \
    libxcomposite-dev \
    libatk1.0-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libxdamage-dev \
    nasm \
    libomp-dev \
    libomp5 \
    libeigen3-dev && \
    apt-get clean

# Setzen der LD_LIBRARY_PATH-Umgebungsvariable
ENV LD_LIBRARY_PATH="/usr/lib/llvm-14/lib:${LD_LIBRARY_PATH}"


# Install Miniconda with a reliable installation method
RUN wget -O /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/miniconda && \
    rm /tmp/miniconda.sh

# Set PATH for conda
ENV PATH="/opt/miniconda/bin:$PATH"

# Clone the PyPupilEXT repository
RUN git clone --recurse-submodules https://github.com/openPupil/PyPupilEXT.git /PyPupilEXT

# Change to the project directory
WORKDIR /PyPupilEXT

RUN conda init

RUN bash

# Create the conda environment using environment.yml
RUN conda env create -f environment.yml

# Activate the conda environment, build the package, and install the wheel file
RUN conda run --no-capture-output -n pypupilenv python setup.py bdist_wheel

RUN conda run --no-capture-output -n pypupilenv pip install dist/*.whl

# Default command to keep the container running with access to the conda environment
# CMD ["/bin/bash"]
