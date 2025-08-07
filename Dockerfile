FROM alpine:latest AS build

RUN apk add --no-cache python3 py3-pip

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN pip3 uninstall -y pip setuptools packaging

FROM alpine:latest AS release

LABEL desc="OpenCalc v1"

RUN apk add --no-cache python3

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir /project
WORKDIR /project
COPY ./main.py /project/main.py
COPY ./models.py /project/models.py
COPY ./consts.py /project/consts.py
COPY ./func.py /project/func.py

RUN mkdir /project/static
COPY ./static /project/static

RUN mkdir /project/views
COPY views /project/views


EXPOSE 8590

ENTRYPOINT ["python", "main.py"]
