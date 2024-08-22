# syntax=docker/dockerfile:1.7-labs

FROM python:3.12-slim-bookworm AS python-base

COPY requirements.txt ./
RUN pip install --no-cache-dir --no-cache -r requirements.txt
RUN pip uninstall -y setuptools pip wheel


FROM gcr.io/distroless/cc-debian12

COPY --from=python-base /usr/local/lib/ /usr/local/lib/
COPY --from=python-base /usr/local/bin/python /usr/local/bin/
COPY --from=python-base /etc/ld.so.cache /etc/

COPY --parents --from=python-base /lib/./*/libz.so.* /lib/
COPY --parents --from=python-base /usr/lib/./*/libffi* /usr/lib/
COPY --parents --from=python-base /lib/./*/libexpat* /lib/

COPY --from=python-base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

WORKDIR /app
COPY src ./

ENTRYPOINT ["/usr/local/bin/python", "/app/main.py"]