# Provider mappings

> Generated from `content/`. Edit YAML, then run `tools/build.py`.

Vendor-agnostic pattern first; provider details second. Every fixture is `terraform plan`-only.

## Event-driven processing

Producers publish events to a managed queue or topic; a consumer function processes them and moves repeated failures to a dead-letter destination, with a managed store for processed-event state. The pattern is provider-neutral and every fixture is plan-only and cost-free.

| Provider | Services | Emulator | Fixture | Watch out |
| --- | --- | --- | --- | --- |
| AWS | SQS queue with dead-letter queue + AWS Lambda + DynamoDB | Floci for local AWS emulation; LocalStack is an alternative. Fixtures never deploy. | `terraform/aws/event-driven` | The event source mapping and redrive policy reference ARNs; verify both resolve in the plan without live state. |
| AZURE | Azure Storage Queues with poison queue + Azure Functions + Table Storage | Floci for local Azure emulation. Fixtures are plan-only and require no live account. | `terraform/azure/event-driven` | Storage Queue and Table names must be lowercase, and Function App names are globally unique. |
| GCP | Pub/Sub topic with dead-letter topic + Cloud Functions + Firestore | Floci for local GCP emulation. Fixtures use placeholder project and source values only. | `terraform/gcp/event-driven` | Dead-letter policies need a topic id and delivery attempt count; keep the trigger and subscription on the same project. |

## Serverless API

A managed HTTP endpoint fronts a short-lived, stateless function that reads and writes a managed table or document store. The pattern is provider-neutral: route the request, run the handler, persist the result. Every fixture is plan-only and cost-free.

| Provider | Services | Emulator | Fixture | Watch out |
| --- | --- | --- | --- | --- |
| AWS | API Gateway HTTP API + AWS Lambda + DynamoDB | Floci for local AWS API emulation; LocalStack is an alternative. Fixtures never deploy. | `terraform/aws/serverless-api` | Lambda invoke permissions and integration URIs are easy to miswire; check the API Gateway source ARN in the plan. |
| AZURE | API Management + Azure Functions + Table Storage | Floci for local Azure emulation. Fixtures are plan-only and require no live account. | `terraform/azure/serverless-api` | Function App and Storage Account names are globally unique, and API Management needs publisher details even in a plan. |
| GCP | Cloud Run endpoint + Cloud Functions + Firestore | Floci for local GCP emulation. Fixtures use placeholder project and source values only. | `terraform/gcp/serverless-api` | Cloud Functions needs a runtime, entry point, and source location at plan time; supply placeholders, never credentials. |
