FROM python:3.8-slim
LABEL maintainer="jkaak"

RUN mkdir api
WORKDIR api
RUN mkdir app
RUN mkdir model

COPY requirements.txt .
ADD ./app ./app
ADD ./model ./model

RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "app/app.py"]