Examples of ECS services with autoscaling and AWS Fargate.

## Prerequisites

This template requires you to opt-in to the new ARN format for ECS Container Instances, Services and Tasks:

```bash
aws ecs put-account-setting-default --name serviceLongArnFormat --value enabled
aws ecs put-account-setting-default --name taskLongArnFormat --value enabled
aws ecs put-account-setting-default --name containerInstanceLongArnFormat --value enabled
```

You'll also need to setup the VPC & Subnet stacks from [sjakthol/aws-account-infra](https://github.com/sjakthol/aws-account-infra).

## Infrastructure

Create the infra (ECR repositories + ECS cluster) by running

```
make deploy-ecr deploy-ecs
```

## Services

### SQS Consumer

SQS Consumer service consumes an SQS queue. Deploy the service by running

```
# Container Image
(cd services/sqs-consumer/ && make push)

# Service
make deploy-service-ecs-consumer
```

Service starts with 0 tasks in service. Scaling policies have been set up to

* start first task when a message is sent to the SQS queue (latency between 2-3 minutes)
* scale service up and down (between 1 and 8 tasks) based on CPU utilization (target tracking)
* scale to zero if queue is empty and no messages have passed through it in past 15 minutes

These scaling policies are suitable for services where a startup delay of few minutes is acceptable.

You may use

```
aws sqs send-message --queue-url https://sqs.<region>.amazonaws.com/<account_id>/<region_prefix>-ecs-autoscaling-service-sqs-consumer-queue --message-body "$(date -Iseconds)"
```

or (requires `boto3`)
```
env QUEUE_URL=https://sqs.<region>.amazonaws.com/<account_id>/<region_prefix>-ecs-autoscaling-service-sqs-consumer-queue python3 producer.py
```

to send messages to the queue the service consumes.
