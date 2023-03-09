FROM python:3.9-alpine

LABEL desc="OpenCalc v1"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /project
WORKDIR /project
COPY ./main.py /project/main.py

EXPOSE 80

ENTRYPOINT ["python", "main.py"]
