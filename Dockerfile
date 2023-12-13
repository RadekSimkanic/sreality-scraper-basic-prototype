# Base image
FROM python:3.12

# Scrapy Installation
RUN pip install scrapy

# HTTP server (Flask)
RUN pip install flask
RUN pip install psycopg2-binary

# wait-for-it
ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Working Directory
WORKDIR /app

# Copy src
COPY . /app

# Requirements
RUN pip install -r requirements.txt

# Wait and Execute
CMD ["wait-for-it", "postgres:5432", "--", "./run.sh"]