# Patterns: Data Structures, Cloud Architecture, Game Theory

<!-- repo-role: content-and-rendering -->

**Reusable patterns for building and reasoning about systems.** Formerly `cloud-patterns`.

## Role and boundary

This repo is the **content and rendering layer**: teachable patterns, diagrams, scenarios, quizzes, and deterministic
builders that turn committed YAML into committed Markdown, HTML, glossaries, flashcards, and visual review pages.

It does not acquire literature or index it:

- `tool-lit-review` searches, downloads, and analyses papers, then writes a schema-v1 `content-export`.
- `papers/tools/ingest.py` only **imports** that local export into `content/`. It never downloads, parses a PDF, or
  calls a sibling repo at runtime.
- `tool-rag` owns embedding and retrieval over PDFs. This repo consumes retrieval results; it does not store vectors.

The boundary in one line: **acquisition and analysis in `tool-lit-review`; content and presentation here; indexing and
retrieval in `tool-rag`.** A content build must run from committed files and local exports, with no network access.

### Design-intent guards

The boundary is enforced by tests, not prose. These run in `just test-unit` (the CI and pre-push gate):

| Invariant | Guard in `tests/unit/test_papers_content.py` |
|---|---|
| This repo declares the content role and names both neighbours | `test_readme_declares_the_content_role_and_neighbours` |
| No Python here imports a sibling tool or an acquisition/indexing library | `test_papers_tools_import_no_acquisition_or_indexing_code`, `test_no_python_in_the_repo_imports_a_sibling_tool` |
| PDFs stay in the producer's working folder, never in this repo | `test_papers_hold_no_pdf_files` |
| The importer refuses an unknown schema, an escaping PDF path, or a malformed checksum; a dry run writes nothing | `test_unknown_schema_is_refused`, `test_pdf_path_outside_the_folder_is_refused`, `test_dry_run_writes_nothing` |
| Re-import refreshes `source` metadata but preserves authored concepts, equations, claims and citations | `test_reimport_preserves_authored_fields` |
| Rendered output is derived only from committed YAML | `test_render_outputs_are_derived_from_committed_yaml` |
| Imported papers record original-summary rights, with no quoted PDF text | `test_imported_papers_record_original_summary_rights` |

The new review surfaces follow the same rule: `tests/unit/test_cards.py`, `tests/unit/test_visual.py`, and
`tests/unit/test_proofs.py` regenerate every checked-in output from committed glossaries, paper YAML, proof DAG YAML, and
diagram data, and refuse acquisition or sibling imports.

### Interview review surfaces

- `cards/` — one canonical deck from every committed `glossary.json`: `deck.json`, `anki.csv`, a local review page, and
  a timed terminal drill with local scheduling state.
- `visual/` — concept maps from paper YAML, an architecture diagram gallery, and proof-DAG rendering, all static and
  self-contained.
- `proofs/` — three real proof DAGs for amortized append, sliding-window linearity, and linear heapify, rendered as notes
  and review cards.

```bash
just -f proofs/justfile build && just -f visual/justfile build && just -f cards/justfile build
just -f cards/justfile review --minutes 30
just -f visual/justfile serve   # http://localhost:8000/visual/index.html
```

This repository holds three pattern families:

- **Data structures:** how information is shaped, indexed, and kept consistent.
- **Cloud architecture:** vendor-agnostic cloud design patterns, taught through hands-on practice with local emulators, infrastructure-as-code, and real-world scenarios. Learn once, apply anywhere (AWS, Azure, GCP, or any provider).
- **Game theory:** strategic interaction, incentives, and equilibria, applied to the decisions the other families create.

The cloud architecture family is the current content. The other two are scoped here and not yet written.

## 🗺️ Interactive Architecture Diagrams

Explore all 10 scenarios visually with clickable links to implementations:

👉 **[View Interactive Diagrams →](https://baseline0.github.io/patterns/)** (Live on GitHub Pages)

Each diagram links directly to:
- 📂 Terraform infrastructure code (AWS/Azure/GCP)
- 📖 Scenario README documentation
- 🏃 Local setup scripts

## 🎯 Philosophy

- **Vendor-agnostic**: Patterns first, provider details second
- **Cost-free**: Local emulators (Floci, LocalStack) run on your laptop
- **IaC-first**: Every pattern includes Terraform for AWS/Azure/GCP
- **Scenario-driven**: Learn through architecture exercises, not tutorials
- **Diagram + Code**: Architecture diagrams paired with working implementations

## 📚 What's Included

### **Part 1: Pattern Library** (`patterns/`)

Core cloud architecture patterns with:
- **Pattern summary**: What it solves, when to use it, trade-offs
- **Architecture diagram**: Visual reference (Draw.io source)
- **Local emulator setup**: Docker Compose to run locally
- **Terraform implementation**: AWS/Azure/GCP variants
- **Cost analysis**: Realistic pricing estimates (cloud)

**Patterns**:
1. **3-Tier Web Application** (load balancer → app servers → database)
2. **Serverless Event-Driven** (S3 → SNS/SQS → Lambda → Database)
3. **Microservices + Kubernetes** (Helm charts, service mesh optional)
4. **Data Lake & ETL** (object storage → data pipeline → warehouse)
5. **Multi-Region Disaster Recovery** (active-active, failover strategies)
6. **Event Sourcing + CQRS** (event log, separate read/write models)
7. **API Gateway + Caching** (CDN, API rate limiting, authentication)
8. **Hybrid Cloud** (on-prem ↔ cloud connectivity)

### **Part 2: Local Emulator Setup** (`docker-compose/`)

One-command local environment for each provider:

```bash
# AWS
docker-compose -f docker-compose/aws.yml up

# Azure
docker-compose -f docker-compose/azure.yml up

# GCP
docker-compose -f docker-compose/gcp.yml up
```

Services included:
- **AWS**: S3, DynamoDB, Lambda, SQS, SNS, API Gateway
- **Azure**: Blob Storage, Queue Storage, Functions, Service Bus
- **GCP**: Cloud Storage, Pub/Sub, Firestore, Cloud Functions

### **Part 3: Infrastructure-as-Code** (`terraform/`)

Production-ready Terraform for each pattern + provider:

```
terraform/
├── aws/
│   ├── 3-tier-web/
│   ├── serverless-event-driven/
│   ├── eks-microservices/
│   └── ...
├── azure/
│   ├── 3-tier-web/
│   ├── serverless-event-driven/
│   ├── aks-microservices/
│   └── ...
└── gcp/
    ├── 3-tier-web/
    ├── serverless-event-driven/
    ├── gke-microservices/
    └── ...
```

**Each includes**:
- `main.tf` — Infrastructure definition
- `variables.tf` — Parameterization (region, instance size, etc.)
- `outputs.tf` — What to display after deployment
- `terraform.tfvars.example` — Copy to `terraform.tfvars` to deploy
- `test.sh` — Validation script (runs `terraform plan`, checks syntax)

### **Part 4: Architecture Diagrams** (`diagrams/`)

Draw.io source files for each pattern:

```
diagrams/
├── 3-tier-web-app.drawio
├── serverless-event-driven.drawio
├── microservices-kubernetes.drawio
├── data-lake-etl.drawio
├── multi-region-dr.drawio
├── event-sourcing-cqrs.drawio
├── api-gateway-caching.drawio
└── hybrid-cloud.drawio
```

Open in [Draw.io](https://draw.io) (free, browser-based):
- Drag to edit
- Export as PNG/PDF for presentations
- AWS/Azure/GCP icon libraries included

### **Part 5: Scenario-Based Exercises** (`scenarios/`)

Real-world architecture challenges:

1. **E-commerce Platform** (1M daily users, 99.99% uptime, PCI compliance)
2. **Data Pipeline** (1TB/day ingestion, real-time analytics, 7-year retention)
3. **Migration Strategy** (on-prem VMs → cloud, zero downtime)
4. **Cost Optimization** (existing design, reduce 40% spend)
5. **Disaster Recovery** (RTO = 1 hr, RPO = 15 min)
6. **Security Hardening** (compliance, zero-trust, encryption)

**Each scenario includes**:
- Requirements document
- Success criteria (latency, availability, cost, compliance)
- Starter diagram (incomplete)
- Solution checklist
- Model solution (with trade-offs explained)

### **Part 6: Learning Path** (`LEARNING.md`)

Structured progression: Weeks 1-8

- **Week 1-2**: Fundamentals (Well-Architected Framework, diagramming)
- **Week 3-4**: Hands-on with emulators (serverless, databases)
- **Week 5-6**: Deep dives (pick 1-2 patterns, study deeply)
- **Week 7-8**: Mock scenarios (architect solutions under time pressure)

### **Part 7: References** (`references/`)

Best practices from each provider:

- **AWS**: Well-Architected Framework, Architecture Center
- **Azure**: Azure Architecture Center, design principles
- **GCP**: Architecture Framework, patterns & practices
- **Cross-provider**: CQRS, event sourcing, microservices patterns

### **Part 8: Paper Learning** (`papers/`)

Committed paper content and rendering. Paper acquisition is not here.

```bash
# In tool-lit-review: fetch and export metadata (the only downloader)
uv run tool-lit-review content-export --papers <working-folder> --output /tmp/papers.json

# Here: import the local export, then render committed YAML
just -f papers/justfile import-export /tmp/papers.json
just -f papers/justfile render 2401.12345
```

`import-export` preserves authored concepts, equations, claims, and citations on re-import. It refuses an unknown
export schema, a non-relative PDF path, or a malformed checksum. No network, no PDF parsing, no sibling import.

The export schema is owned by `tool-lit-review`; this importer pins the version it accepts. Adding a field is a
coordinated change: bump the producer's schema version, update both importer and guards, and keep both unit gates green.
Two real papers are imported and rendered from a local `qiea` export: the TSP quantum-genetic comparison
(`2409.13788v1`) and Halfway Escape Optimization (`2405.02850v7`). Both overviews are original summaries with
`rights.quotes: none`; no PDF text or quoted abstract is committed here.

### **Part 9: Review Modules** (`cards/`, `visual/`, `proofs/`)

`cards/` consumes the glossaries that each family builder already emits. It assigns stable ids, records provenance, and
regenerates a versioned deck, an Anki CSV, and an offline review page. `visual/` renders paper concept maps, the existing
architecture SVGs, and proof DAGs. `proofs/` owns three committed DAGs covering amortized append, sliding-window
linearity, and linear heapify; its YAML is the source for both the rendered notes and the DAG pages. Neither module
downloads, indexes, or imports a sibling tool. See each module's README for the schemas and commands.

## 🚀 Quick Start

### **Option 1: Local Practice (Recommended)**

```bash
# Clone repo
git clone <repo> patterns && cd patterns

# Start AWS emulator
docker-compose -f docker-compose/aws.yml up -d

# Deploy serverless pattern locally
cd patterns/serverless-event-driven
./local-setup.sh  # Creates S3 bucket, DynamoDB table, simulates Lambda

# Verify
aws --endpoint-url=http://localhost:4566 s3 ls
```

### **Option 2: Study Architectures**

```bash
# Open diagram
open diagrams/3-tier-web-app.drawio

# Read pattern guide
cat patterns/3-tier-web-app/README.md

# Review Terraform (all 3 providers side-by-side)
ls terraform/{aws,azure,gcp}/3-tier-web/
```

### **Option 3: Practice Scenarios**

```bash
# Review scenario
cat scenarios/ecommerce-platform/README.md

# 30-min timer: Design a solution, diagram in Draw.io
# Compare to model solution
cat scenarios/ecommerce-platform/SOLUTION.md
```

## 📖 Learning Outcomes

After completing this repo, you'll understand:

- ✅ **Vendor-agnostic patterns**: How to think about cloud architecture independent of provider
- ✅ **IaC best practices**: Terraform patterns, modularity, state management
- ✅ **Scalability trade-offs**: When to use horizontal vs. vertical scaling
- ✅ **Resilience design**: Multi-region, failover, circuit breakers
- ✅ **Cost optimization**: Reserved instances, spot pricing, caching strategies
- ✅ **Security architecture**: Zero-trust, encryption, compliance patterns
- ✅ **Data patterns**: ETL, event sourcing, CQRS, real-time analytics
- ✅ **Operational excellence**: Monitoring, logging, deployment strategies

## 🛠️ Technology Stack

- **Emulators**: Floci (AWS/Azure/GCP), LocalStack (AWS)
- **IaC**: Terraform 1.0+
- **Diagramming**: Draw.io
- **Containers**: Docker, Docker Compose
- **CLI Tools**: AWS CLI, Azure CLI, gcloud CLI (optional)
- **Testing**: `terraform validate`, `tflint`, `checkov`

## 📋 Project Structure

```
patterns/
├── README.md                      # This file
├── LEARNING.md                    # 8-week learning path
├── CONTRIBUTING.md                # How to add patterns
├── patterns/
│   ├── 3-tier-web-app/
│   ├── serverless-event-driven/
│   ├── microservices-kubernetes/
│   ├── data-lake-etl/
│   ├── multi-region-dr/
│   ├── event-sourcing-cqrs/
│   ├── api-gateway-caching/
│   └── hybrid-cloud/
├── terraform/
│   ├── aws/
│   ├── azure/
│   └── gcp/
├── docker-compose/
│   ├── aws.yml
│   ├── azure.yml
│   └── gcp.yml
├── diagrams/
│   └── *.drawio
├── scenarios/
│   ├── ecommerce-platform/
│   ├── data-pipeline/
│   ├── migration-strategy/
│   ├── cost-optimization/
│   ├── disaster-recovery/
│   └── security-hardening/
├── references/
│   ├── aws-waf/
│   ├── azure-patterns/
│   └── gcp-patterns/
├── data-structures/               # YAML source -> generated write-ups, quizzes, glossaries
├── testing/                       # YAML source -> generated testing-pattern content
├── data-engineering/              # playbook, templates, and a case study
├── papers/                        # imported paper metadata and local rendering
│   ├── content/                   # committed arxiv-*.yaml (imported, then authored)
│   └── tools/                     # import-export and render; no download or PDF parsing
├── cards/                         # canonical deck, Anki CSV, local and terminal review
├── visual/                        # concept maps, diagram gallery, proof DAG pages
├── proofs/                        # committed DAG source -> notes and review cards
│   ├── content/                   # three proof YAML sources
│   └── tools/                     # deterministic renderer; no network or sibling imports
└── .github/workflows/
    └── validate.yml               # CI: Terraform validation
```

## 🎯 Design Principles

1. **Pattern → Implementation**: Learn the pattern first (vendor-agnostic), then see how each provider implements it
2. **Local → Remote**: Practice locally with emulators before touching real cloud
3. **Diagram → Code**: Start with architecture diagrams, then translate to IaC
4. **Why → What**: Understand *why* a pattern exists before implementing *what*
5. **Trade-offs matter**: Every pattern has pros/cons; document them explicitly

## 🔗 External References

**Cloud Architecture**:
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [GCP Architecture Framework](https://cloud.google.com/architecture/framework)
- [Floci Emulator](https://floci.io/)
- [LocalStack](https://localstack.cloud/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest)

**Data Structures & Algorithms**:
- [LeetScrape](https://github.com/nikhil-ravi/LeetScrape) — Extract and analyze LeetCode problem metadata (patterns, topics, solutions)

## 💡 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new patterns, scenarios, or diagrams.

**Contribution areas**:
- New patterns (with Terraform + diagrams + scenarios)
- Scenario improvements (clearer requirements, model solutions)
- IaC optimizations (cost, security, maintainability)
- Documentation (typos, clarity, examples)

## 📄 License

MIT. Free to use, modify, and distribute.

---

**Start here**: [LEARNING.md](LEARNING.md) for the 8-week learning path, or jump to [patterns/](patterns/) to explore specific architecture patterns.
