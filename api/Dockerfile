FROM python:3
COPY . /code
WORKDIR /code
RUN apt-get update
RUN pip install -r requirements.txt
RUN pip install -e .
ENTRYPOINT ["/docker_entrypoint.sh"]