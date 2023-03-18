FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute
RUN apt update && apt install -y libxrender1 libxext6 libpq-dev gcc
RUN mkdir /ecolab-web
WORKDIR /ecolab-web
ADD requirements.txt /ecolab-web/
RUN pip install -r requirements.txt
ADD . /ecolab-web/