# Some defaults
AWS ?= aws
AWS_REGION ?= eu-north-1
AWS_PROFILE ?= default

AWS_CMD := $(AWS) --profile $(AWS_PROFILE) --region $(AWS_REGION)
AWS_ACCOUNT_ID = $(eval AWS_ACCOUNT_ID := $(shell $(AWS_CMD) sts get-caller-identity --query Account --output text))$(AWS_ACCOUNT_ID)

NAME := $(notdir $(patsubst %/,%,$(dir $(abspath $(firstword $(MAKEFILE_LIST))))))
ECR_REPOSITORY = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/ecs-autoscaling/$(NAME)

login:
	$(AWS_CMD) ecr get-login-password | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

build:
	docker build -t $(NAME) .

push: build login
	docker tag $(NAME):latest $(ECR_REPOSITORY):latest
	docker push $(ECR_REPOSITORY):latest
