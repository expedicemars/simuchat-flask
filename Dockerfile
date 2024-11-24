# syntax=docker/dockerfile:1

#FROM python:3.14.0a2-slim-bookworm

#WORKDIR /python-docker
#RUN apt-get update
#RUN apt-get install -y g++

#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt

#COPY . .

#CMD [ "python3", "-m" , "gunicorn", "--worker-class", "eventlet", "-w", "1", "--access-logfile", "-" ,"application:app"]

# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /simuchat

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]
CMD ["main.py"]

FROM builder as dev-envs

#RUN <<EOF
#apk update
#apk add git
#EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
