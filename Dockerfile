# Use an Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to avoid interaction
ENV DEBIAN_FRONTEND=noninteractive

# Install essential packages and Miniconda
RUN apt-get update && \
    apt-get install -y \
    wget \
    git \
    build-essential \
    cmake \
    g++ \
    pkg-config \
    libopencv-dev \
    libeigen3-dev && \
    apt-get clean

# Install Miniconda
# You may change this accoridng to your current architecture
RUN wget -O /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/miniconda && \
    rm /tmp/miniconda.sh

# Set PATH for conda
ENV PATH="/opt/miniconda/bin:$PATH"

# Clone the PyPupilEXT repository
RUN git clone --recurse-submodules https://github.com/openPupil/PyPupilEXT.git /PyPupilEXT

# Change to the project directory
WORKDIR /PyPupilEXT

# Create the conda environment using environment.yml
RUN conda env create -f environment.yml

# Activate the conda environment, build the package, and install the wheel file
RUN /opt/miniconda/bin/conda run -n pypupilenv python setup.py bdist_wheel && \
    /opt/miniconda/bin/conda run -n pypupilenv pip install dist/*.whl

# Default command to keep the container running with access to the conda environment
CMD ["/bin/bash"]
