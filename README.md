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

### 2. Automatic

Build Dockerfile and run container.

```shell
docker build -t lambda_crawl .
docker run -it --rm --name lambda_crawl -v $(pwd):/working lambda_crawl

# in the container shell
make install && make build
```
Upload manually or automatically the zip file to the lambda function.

## Setting up the Lambda

### 1. Triggers
#### 1.1. CloudWatch Events

Build an event rule that triggers the first newspaper crawling (i.e. `cincodias`). The cron expression is `30 07 ? * MON-FRI *` and the input passed to the function is a JSON `{"newspaper": "cincodias"}`.

This will trigger the first crawl. Subsequent crawls will be triggered using S3 events (every time a list of downloaded articles from a newspaper is stored in the S3 bucket, an event will be triggered and this same lambda will launch a new crawler).

#### 1.2. S3 Events

Within the S3 properties (advanced settings), set an event to trigger a notification after an object is put. Event is `Put` and Filter suffix is `urls.csv` (lambda's output).
