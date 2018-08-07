## Installation

### 1. Manual installation
#### 1.1. Docker container

Spin up an [Ubuntu](https://hub.docker.com/_/ubuntu/) container:

```shell
docker run -v <directory with your code>:/working -it --rm ubuntu
```

* The `-v` flag makes your code directory available inside the container in a directory called “working”.
* The `-it` flag means you get to interact with this container.
* The `--rm` flag means Docker will remove the container when you’re finished.
* `ubuntu` is the name of an official container image containing, you guessed it, Ubuntu. If this container image isn’t already on your machine, Docker will download it for you.

Install pip and zip:
```shell
apt-get update
apt-get install python-pip
apt-get install zip
```
Move into the working directory (you should be able to see your Lambda function code here):
```shell
cd working
```
#### 1.2. Makefile

```shell
# Install virtualenv
make install

# Build zip
make build

# Delete and deploy to new lambda function
make lambda
```

## 2. Automatic

Build Dockerfile and run container.

```shell
docker build -t test_lambda .
docker run -it --rm --name test_lambda $(pwd):/working test_lambda

# in the container shell
make install && make build
```
