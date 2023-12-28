FROM python:3.10-alpine

#RUN python -m venv /opt/venv

WORKDIR /src
COPY ./requirements.txt /src/requirements.txt
#RUN . /opt/venv/bin/activate && pip install --no-cache-dir --upgrade -r \
    #/src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
RUN pip install --upgrade pip
COPY . /src
#CMD . /opt/venv/bin/activate && exec python -m app.main

