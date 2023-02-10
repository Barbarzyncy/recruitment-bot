FROM python:3.9-buster as base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

ARG GROUP_GID=102
ARG USER_UID=1000

RUN addgroup --system --gid $GROUP_GID bot
RUN useradd -m -g bot -u $USER_UID bot
RUN chown -R bot: /app
RUN chmod +x /app/docker/entrypoint.sh

ENTRYPOINT ["/app/docker/entrypoint.sh"]
EXPOSE 8000
