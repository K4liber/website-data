FROM python:3
ADD api/ /api
WORKDIR /api
RUN apt-get update
RUN python -m pip install -r requirements.txt
CMD python api.py