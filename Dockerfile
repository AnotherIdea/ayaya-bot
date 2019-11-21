FROM python:3.7.5-alpine3.10

WORKDIR /usr/src/

COPY requirements.txt ./

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY src/ .

ENTRYPOINT ["python3", "/usr/src/run.py"]
