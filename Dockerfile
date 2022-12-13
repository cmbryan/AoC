FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y \
        vim-tiny \
    && rm -rf /var/lib/apt/lists/*

# install required python packages (see requirements.txt for details)
RUN pip install \
    numpy \
    black
