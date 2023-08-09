FROM python:3.9-alpine

LABEL desc="OpenCalc v1"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /project
WORKDIR /project
COPY ./main.py /project/main.py
COPY ./models.py /project/models.py

RUN mkdir /project/static
COPY ./static /project/static

RUN mkdir /project/views
COPY views /project/views


EXPOSE 8590

ENTRYPOINT ["python", "main.py"]
