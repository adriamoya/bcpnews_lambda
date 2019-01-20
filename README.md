# [BBB Crawling Lambda](https://medium.com/@adriamoyaortiz/classifying-news-to-build-a-newsletter-with-deep-learning-part-2-cd6104fa7317)

This project contains scripts and dependencies to deploy the BBB crawling process on AWS Lambda.

* The python application (lambda function) lives in `/crawl_lambda` directory. It's a lightweight set of crawlers built with [`requests`](http://docs.python-requests.org/en/master/) and [`beautifulsoup`](https://pypi.org/project/beautifulsoup4/). Each crawler scrapes a different online newspaper and extracts links to articles.

* Python libraries and other dependencies are stored in the virtual environment and must be included in the final package that is uploaded to AWS. The `lxml` library is automatically copied into the final package (this is not really necessary since we are no longer using the [`newspaper3k`](https://newspaper.readthedocs.io/en/latest/) library to parse the articles).

This application can be uploaded to AWS Lambda by using [`zappa`](https://github.com/Miserlou/Zappa). However, here it is configured to spin up a `docker` container with the same OS (`ubuntu`), use the Makefile commands to install and build the final package and manually upload the zipped application to AWS.

## Execution logic

1. The lambda function is executed every day from a CloudWatch event rule using a cron expression (`30 07 ? * MON-FRI *`).
2. The lambda handler triggers the first spider (`cincodias`).
3. Urls extracted from Cincodías are stored into a S3 bucket.
4. The S3 bucket, after the put event, calls the lambda function again.
5. This time, the lambda triggers a new spider (`elconfidencial`). This is possible because the handler receives the event coming from the bucket and it can determine which crawler to launch based on that event.
6. The new spiders downloads and stores the new urls into S3.
7. This process is repeated until the last spider is triggered. At this point, the crawling process is finished and the lambda spins up an EC2 instance that will run the article download, classification, text similarity and email sending processes (using a crontab job that is launched when booting the instance). The instance will stop after the newsletter is sent (by another lambda).

## Directory structure

```shell
# tree . -I __pycache__ --dirsfirst -L 3 > tree.txt
.
├── crawl_lambda
│   ├── crawlers
│   │   ├── __init__.py
│   │   ├── cincodias.py
│   │   ├── elconfidencial.py
│   │   ├── eleconomista.py
│   │   └── expansion.py
│   └── crawl.py
├── env
│   ├── bin
│   ├── include
│   ├── lib
│   └── pip-selfcheck.json
├── lxml
├── package
│   ├── tmp
│   │   ├── PIL
│   │   ├── Pillow-5.2.0.dist-info
│   │   ├── PyYAML-3.13.dist-info
│   │   ├── ...
│   │   ├── feedparser.py
│   │   ├── requests_file.py
│   │   └── six.py
│   └── crawl_lambda.zip
├── Dockerfile
├── Makefile
├── README.md
├── bluecap_bbb_crawl.yaml
└── requirements.txt
```

## Deployment

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
# (might not work if heavy package)
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
