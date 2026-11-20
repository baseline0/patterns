terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "lambda_exec" {
  name = "event-driven-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_sqs_queue" "events_dead_letter" {
  name = "event-driven-dead-letter"
}

resource "aws_sqs_queue" "events" {
  name = "event-driven-events"

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.events_dead_letter.arn
    maxReceiveCount     = 3
  })
}

resource "aws_lambda_function" "consumer" {
  function_name = "event-driven-consumer"
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri     = "111122223333.dkr.ecr.us-east-1.amazonaws.com/event-driven-consumer:latest"
}

resource "aws_lambda_event_source_mapping" "events" {
  event_source_arn = aws_sqs_queue.events.arn
  function_name    = aws_lambda_function.consumer.arn
}

resource "aws_dynamodb_table" "processed_events" {
  name         = "event-driven-processed-events"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "event_id"

  attribute {
    name = "event_id"
    type = "S"
  }
}
