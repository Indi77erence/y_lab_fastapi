FROM python:3.10-alpine

RUN mkdir '/y_lab'

WORKDIR /y_lab

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
