# hadoop-exporter:0.1.0

FROM python:3.6.9

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /opt/

WORKDIR /opt

ENTRYPOINT ["python", "main.py"]
