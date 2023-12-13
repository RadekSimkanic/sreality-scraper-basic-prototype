# Base image
FROM python:3.12

# Scrapy Installation
RUN pip install scrapy

# HTTP server (Flask)
RUN pip install flask
RUN pip install psycopg2-binary

# Working Directory
WORKDIR /app

# Copy src
COPY . /app

# Requirements
RUN pip install -r requirements.txt

# Prepare run.sh
RUN chmod +x run.sh
RUN sed -i 's/\r$//' /app/run.sh && chmod +x /app/run.sh