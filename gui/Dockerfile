# Dockerfile for next_frontend

FROM ubuntu:14.04
MAINTAINER Lalit Jain, lalitkumarj@gmail.com
# Install basic applications
RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-distribute \ 
    python-pip \
    python-numpy \
    python-scipy \
	python-gevent \
    python-matplotlib

# Install gunicorn
RUN pip install gunicorn

# Copy the code over, we will over write this volument
COPY . /next_frontend
WORKDIR /next_frontend

# Install python dependencies for next_backend
ADD requirements.txt /requirements.txt
RUN pip install -U -r requirements.txt

# Expose port 8000 to the host
EXPOSE 8000



