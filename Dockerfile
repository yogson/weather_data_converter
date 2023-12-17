FROM python:3.11 as base
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y libeccodes-dev
RUN pip install --no-cache-dir -r requirements.txt

FROM base
VOLUME /data
ENV TEMP_DIR=/data/temp
ENV SOURCE_DIR=/data/src
ENV OUTPUT_DIR=/data/output

COPY ./src /app
RUN rm /app/local_settings.py
CMD ["python", "-W", "ignore", "main.py"]
