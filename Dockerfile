FROM python:3.8-slim

# Installation of the dependencies
RUN apt-get update \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN apt-get purge -y --auto-remove gcc

# Copy the source code to the build context
COPY app/ /app/
WORKDIR /app/
RUN mkdir data
RUN ls -la

EXPOSE 8000
CMD python dashboard.py
