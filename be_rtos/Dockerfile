FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /be_rtos

COPY requirements.txt be_rtos/requirements.txt

RUN pip install -r be_rtos/requirements.txt

COPY ./be_rtos /be_rtos

