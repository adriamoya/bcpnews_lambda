
PROJECT = test_lambda
VIRTUAL_ENV = env
FUNCTION_NAME = test_lambda
AWS_REGION = us-east-2
FUNCTION_HANDLER = lambda_handler
LAMBDA_ROLE = arn:aws:iam::653047368971:role/service-role/sendNewsletters

# Default commands
install: virtual
build: clean_package build_package_temp copy_python remove_unused zip
lambda: lambda_delete lambda_create

virtual:
	@echo "--> Setup and activate virtualenv"
	if test ! -d "$(VIRTUAL_ENV)"; then \
		pip3 install virtualenv; \
		virtualenv $(VIRTUAL_ENV); \
		( \
			. ./$(VIRTUAL_ENV)/bin/activate; \
			pip install -r requirements.txt; \
		); \
		# AWS Lambda can write only to /tmp, so in settings.py we need to change DATA_DIRECTORY
		sed -i -e "s:.newspaper_scraper:/tmp/.newspaper_scraper:g" $(VIRTUAL_ENV)/lib/python3.6/site-packages/newspaper/settings.py; \
	fi
	@echo ""

clean_package:
	rm -rf ./package/*

build_package_temp:
	mkdir -p ./package/tmp/lib
	cp -a ./$(PROJECT)/. ./package/tmp/

copy_python:
	if test -d $(VIRTUAL_ENV)/lib; then \
		cp -r lxml/ $(VIRTUAL_ENV)/lib/python3.6/site-packages/lxml/; \
		cp -a $(VIRTUAL_ENV)/lib/python3.6/site-packages/. ./package/tmp/; \
	fi
	if test -d $(VIRTUAL_ENV)/lib64; then \
		cp -r lxml/ $(VIRTUAL_ENV)/lib64/python3.6/site-packages/lxml/; \
		cp -a $(VIRTUAL_ENV)/lib64/python3.6/site-packages/. ./package/tmp/; \
	fi

remove_unused:
	rm -rf ./package/tmp/wheel*
	rm -rf ./package/tmp/easy-install*
	rm -rf ./package/tmp/setuptools*

zip:
	find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
	find . -name '.DS_Store' -type f -delete
	cd ./package/tmp && zip -r ../$(PROJECT).zip .

lambda_delete:
	aws lambda delete-function \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME)

lambda_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://./package/$(PROJECT).zip \
		--role $(LAMBDA_ROLE) \
		--handler $(PROJECT).$(FUNCTION_HANDLER) \
		--runtime python3.6 \
		--timeout 60 \
		--memory-size 128
