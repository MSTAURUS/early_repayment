FROM alpine:latest AS build

RUN apk add --no-cache python3 py3-pip

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir --no-compile -r /tmp/requirements.txt \
    # Удаляем pip, setuptools, wheel и чистим кэш/тесты
    && pip3 uninstall -y pip setuptools wheel 2>/dev/null || true \
    && find /opt/venv -type d \( -name "__pycache__" -o -name "tests" -o -name "test" -o -name "docs" \) -exec rm -rf {} + || true

FROM alpine:latest AS release

LABEL desc="OpenCalc v2"

RUN apk add --no-cache python3

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /project /project/static /project/views
WORKDIR /project
COPY ./main.py ./models.py ./consts.py ./func.py /project/
COPY ./static /project/static
COPY views /project/views

EXPOSE 8564

ENTRYPOINT ["python", "main.py"]
