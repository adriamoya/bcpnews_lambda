# Pull base image.
FROM ubuntu:latest

# Install.
RUN \
  apt-get -y update && \
  apt-get install -y python3-pip && \
  apt-get install -y zip

# Copy the current directory contents into the container at /app
ADD . /working

WORKDIR /working

RUN make install
