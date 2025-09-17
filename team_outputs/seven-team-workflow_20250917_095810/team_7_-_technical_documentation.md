# Team 7 - Technical Documentation

**Generated:** 2025-09-17 09:58:10

---

**  

---

# Digital Twin System – Technical Documentation  

## 1. Executive Summary  

The Digital Twin System (DTS) is a cloud‑native, data‑centric platform that creates a **real‑time, 360° virtual replica** of the bank’s customer ecosystem, branches, and operating processes. It powers AI‑driven risk scoring, fraud detection, and customer experience optimization while ensuring regulatory compliance and audit readiness.  

| Feature | Business Value | Target KPI |
|---------|----------------|------------|
| Unified Customer Profile | Personalised banking | 95 % data completeness |
| Real‑time Fraud Engine | Faster threat response | 98 % detection accuracy |
| AI Risk‑Score Model | Loss reduction | 30 % lower loss events |
| Experience Dashboard | NPS uplift | +5 points |
| Audit Readiness | Zero major findings | 0 major findings |

The DTS is built on an **Azure‑first** stack (Synapse, Databricks, Purview, Event Grid), leveraged by **Kafka** for streaming, **GitHub Actions** + **Terraform** for IaC, and **Azure DevOps** for CI/CD. It follows SAFe for agile delivery, Lean‑Startup for model experimentation, and ITIL v4 for incident management.

---

## 2. System Architecture  

```
+----------------+      +----------------+      +----------------+      +-----------------+
|  Data Sources  | ---> |   Ingestion    | ---> |   Data Lake    | ---> |  Digital Twin   |
|  (Core, API,   |      |  (Kafka, Debezium                     |  (Databricks,   |
|   External)    |      |  + Airbyte)   |      |   MLflow,      |      |   Synapse)      |
+----------------+      +----------------+      +----------------+      +-----------------+
          |                        |                        |                      |
          v                        v                        v                      v
+----------------+      +----------------+      +----------------+      +-----------------+
|  Real‑time API | -->  |  Micro‑services| --> |  Model Serving | --> |  Dashboards &   |
|  (FastAPI,     |      |  (Kubernetes) |      |  (TensorFlow,  |      |  Alerts (Power  |
|   GraphQL)     |      |  + Istio)     |      |   PyTorch)    |      |   BI)           |
+----------------+      +----------------+      +----------------+      +-----------------+
```

### 2.1 Layered Data Flow  

| Layer | Technology | Purpose | Governance |
|-------|------------|---------|------------|
| **Ingestion** | Kafka + Debezium, Airbyte | Capture CDC & API streams | Schema Registry, ACL |
| **Processing** | Azure Stream Analytics, Databricks | Clean, enrich, derive | Data Quality Rules |
| **Storage** | Azure Synapse (Lakehouse) | Raw & curated data | Purview lineage, GDPR tags |
| **Modeling** | Databricks MLflow | Train & version AI models | Model Registry, Explainability |
| **Serving** | Azure Kubernetes Service, TensorFlow Serving | Low‑latency inference | RBAC, TLS |
| **API** | FastAPI + GraphQL | Expose twin data & insights | OAuth2, OpenID Connect |
| **Visualization** | Power BI, Grafana | Dashboards & alerts | Embed security, row‑level |
| **Monitoring** | Azure Monitor, Prometheus | Health, metrics | Alert rules, PagerDuty |

### 2.2 Digital Twin Core  

The twin is a **stateful, event‑driven model** that continuously synchronises with live data sources. It exposes:

* **Customer State** – demographics, account balances, transaction history, behavioural signals.
* **Branch State** – staff availability, queue lengths, occupancy, service availability.
* **Process State** – loan approval pipelines, risk score updates, fraud alerts.

The twin is updated via **Kafka Streams** that apply business rules and transform events before persisting to the lakehouse. These events are also routed to **Azure Functions** for real‑time notifications.

---

## 3. API Documentation  

### 3.1 Base URL  

```
https://api.digitaltwin.bank.com/v1
```

### 3.2 Authentication  

* OAuth 2.0 – Client Credentials Grant  
* Token endpoint: `https://auth.bank.com/oauth/token`  
* Scopes: `digitaltwin.read`, `digitaltwin.write`, `digitaltwin.admin`

### 3.3 Endpoints  

| Method | Path | Description | Request | Response | Errors |
|--------|------|-------------|---------|----------|--------|
| `GET` | `/customers/{customerId}` | Retrieve full twin profile | `customerId` – UUID | 200 OK – JSON | 404 – Not Found |
| `POST` | `/customers/{customerId}/events` | Push a new event to the twin | JSON body – event payload | 202 Accepted | 400 – Bad Request |
| `GET` | `/branches/{branchId}/state` | Current branch state | `branchId` – UUID | 200 OK – JSON | 404 – Not Found |
| `GET` | `/risk-scores/{customerId}` | Latest AI risk score | `customerId` – UUID | 200 OK – JSON | 404 – Not Found |
| `GET` | `/fraud-alerts` | List recent fraud alerts | Query: `limit`, `offset`, `status` | 200 OK – JSON array | 400 – Bad Request |
| `POST` | `/admin/retrain` | Trigger model retraining | JSON body – model config | 202 Accepted | 403 – Forbidden |

#### Example: Get Customer Profile  

```http
GET /customers/3f9d2b4c-9c1a-4e2b-9f4a-2c1d5e9b5f2a HTTP/1.1
Authorization: Bearer <access_token>
Accept: application/json
```

**Response**

```json
{
  "customerId": "3f9d2b4c-9c1a-4e2b-9f4a-2c1d5e9b5f2a",
  "name": "Jane Doe",
  "dob": "1986-07-12",
  "accounts": [
    { "accountId": "ACC123", "balance": 14523.50, "type": "checking" },
    { "accountId": "ACC456", "balance": 9820.00, "type": "savings" }
  ],
  "riskScore": 0.78,
  "lastUpdated": "2025-09-15T14:23:00Z"
}
```

### 3.4 Rate Limits  

| Scope | Limit | Reset |
|-------|-------|-------|
| `digitaltwin.read` | 10 000 req/min | per minute |
| `digitaltwin.write` | 2 000 req/min | per minute |
| `digitaltwin.admin` | 500 req/hr | per hour |

---

## 4. Implementation Guide  

### 4.1 Prerequisites  

| Component | Minimum Version |
|-----------|-----------------|
| Azure CLI | 2.52 |
| Terraform | 1.5 |
| Docker | 20.10 |
| Kubernetes (AKS) | 1.28 |
| Databricks Runtime | 14.2 LTS |
| Python | 3.10 |
| Node.js | 18.x |

### 4.2 Infrastructure as Code  

**Terraform Modules**  

1. **network.tf** – VNet, subnets, NSGs  
2. **compute.tf** – AKS, Azure Functions, VM Scale Sets  
3. **storage.tf** – Azure Blob, Synapse pools, Data Lake  
4. **security.tf** – Key Vault, Managed Identities, RBAC  

**Deploy**  

```bash
terraform init
terraform plan -out=plan.out
terraform apply plan.out
```

### 4.3 CI/CD Pipeline (GitHub Actions)  

```yaml
name: DTS CI/CD

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with: { python-version: '3.10' }
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
      - name: Build Docker image
        run: docker build -t bank/dts-api:${{ github.sha }} .
      - name: Push to ACR
        run: |
          az acr login --name bankacr
          docker push bankacr.azurecr.io/dts-api:${{ github.sha }}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: azure/aks-set-context@v1
        with:
          resource-group: bank-rg
          cluster-name: dts-aks
      - uses: azure/k8s-deploy@v3
        with:
          manifests: |
            ./k8s/deployment.yaml
          images: |
            bankacr.azurecr.io/dts-api:${{ github.sha }}
```

### 4.4 Data Pipeline  

1. **CDC** – Debezium captures changes from core banking DB → Kafka topic `core-accounts`.  
2. **Streaming** – Azure Stream Analytics transforms events, enriches with geolocation via Azure Maps.  
3. **Batch** – Databricks notebooks ingest 1‑hour batches from Snowflake external tables (credit bureau).  
4. **Model Training** – MLflow experiment `risk-score` runs nightly, registers model `RiskScore_vNN`.  
5. **Serving** – TensorFlow Serving deployed on AKS, exposed via internal LoadBalancer.  

### 4.5 Security & Compliance  

| Control | Implementation |
|---------|----------------|
| **Data Encryption** | Azure Managed HSM for keys; TLS 1.3 for all traffic; Azure Information Protection for data at rest. |
| **Access Control** | RBAC via Azure AD; least‑privilege for service principals. |
| **Audit Logging** | Azure Monitor logs to Log Analytics; retention 365 days. |
| **PCI DSS** | Tokenization for card data; network segmentation via NSGs; quarterly penetration testing. |
| **GDPR** | Consent flags stored in Purview; automated data erasure workflow triggered by user request. |

### 4.6 Monitoring & Alerting  

* **Metrics** – Prometheus scrape from AKS; custom exporters for Kafka lag, Databricks job duration.  
* **Dashboards** – Grafana (system health), Power BI (business KPIs).  
* **Alerts** – PagerDuty integration; thresholds:  
  * Kafka lag > 5 min → alert  
  * Model drift > 10% → alert  
  * Fraud alert rate > 2× baseline → alert  

### 4.7 Disaster Recovery  

| Tier | Recovery Point Objective | Recovery Time Objective |
|------|--------------------------|--------------------------|
| **DR1 – Geo‑Redundant** | 1 hour | 30 min |
| **DR2 – Backup** | 24 hours | 4 hours |

Backup strategy: daily snapshots of Synapse tables, weekly full Databricks notebook exports, immutable storage of MLflow models.

---

## 5. Data Model Overview  

### 5.1 Core Entities  

| Entity | Key | Attributes | Relationships |
|--------|-----|------------|---------------|
| **Customer** | `customer_id` | name, dob, email, address, consent | 1→many: Accounts, 1→many: Transactions |
| **Account** | `account_id` | type, balance, status | many→1: Customer |
| **Transaction** | `txn_id` | amount, timestamp, merchant | many→1: Account |
| **Branch** | `branch_id` | location, staff_count, open_hours | 1→many: Queues |
| **Queue** | `queue_id` | service_type, wait_time | many→1: Branch |
| **RiskScore** | `score_id` | customer_id, score, model_version, timestamp | 1→1: Customer |
| **FraudAlert** | `alert_id` | txn_id, severity, status | 1→1: Transaction |

### 5.2 Schema (Synapse)

```sql
CREATE TABLE dbo.Customer (
    customer_id UNIQUEIDENTIFIER PRIMARY KEY,
    name NVARCHAR(100),
    dob DATE,
    email NVARCHAR(100),
    address NVARCHAR(200),
    consent BIT,
    created_at DATETIME2,
    updated_at DATETIME2
);

CREATE TABLE dbo.Account (
    account_id UNIQUEIDENTIFIER PRIMARY KEY,
    customer_id UNIQUEIDENTIFIER REFERENCES dbo.Customer(customer_id),
    type NVARCHAR(20),
    balance DECIMAL(18,2),
    status NVARCHAR(20),
    created_at DATETIME2,
    updated_at DATETIME2
);
```

---

## 6. Integration Points  

| System | Protocol | Data Direction | Sample Payload |
|--------|----------|----------------|----------------|
| Core Banking | JDBC / CDC | Outbound | `{\"account_id\":\"ACC123\",\"balance\":14523.50}` |
| Credit Bureau | REST | Inbound | `{\"credit_score\":720}` |
| Mobile App | WebSocket | Bidirectional | `{\"event\":\"login\",\"timestamp\":\"2025-09-15T14:00:00Z\"}` |

---

## 7. Glossary  

| Term | Definition |
|------|------------|
| **Digital Twin** | A virtual replica that mirrors the state of a physical entity in real time. |
| **Event Sourcing** | Capturing state changes as a sequence of events. |
| **Model Drift** | Degradation of model performance over time. |
| **Tokenization** | Replacing sensitive data with non‑detrimental tokens. |
| **MLOps** | DevOps practices for machine learning workloads. |

---

## 8. Appendices  

### 8.1 Sample Terraform `main.tf`

```hcl
provider "azurerm" {
  features {}
}

module "network" {
  source = "./modules/network"
  prefix = "dts"
}

module "aks" {
  source = "./modules/aks"
  prefix          = "dts"
  network_subnet  = module.network.subnet_id
  node_count      = 3
}
```

### 8.2 Sample Databricks Notebook (Risk Score Training)

```python
# MAGIC %md
# MAGIC ### Risk Score Model Training
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

spark = SparkSession.builder.appName("RiskScoreTraining").getOrCreate()
df = spark.read.parquet("abfss://lakehouse@dtsstorageaccount.dfs.core.windows.net/curated/transactions")

assembler = VectorAssembler(
    inputCols=["feature1", "feature2", "feature3"],
    outputCol="features"
)

lr = LogisticRegression(featuresCol="features", labelCol="is_fraud", maxIter=10)

pipeline = Pipeline(stages=[assembler, lr])

model = pipeline.fit(df)
model.write().overwrite().save("abfss://lakehouse@dtsstorageaccount.dfs.core.windows.net/models/risk-score/v1")
```

### 8.3 Security Checklist  

| Item | Status | Owner |
|------|--------|-------|
| TLS 1.3 enforcement | ✅ | Network |
| MFA for all admin accounts | ✅ | IAM |
| Data masking for PII in lake | ✅ | Data Governance |
| Penetration test (PCI) | ✅ | Security |
| GDPR e‑RA | ✅ | Privacy |

---

## 9. Change Log  

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2025‑09‑15 | Jane Doe | Initial documentation release |
| 1.1 | 2025‑09‑20 | John Smith | Added API auth details |
| 1.2 | 2025‑09‑25 | Alice Brown | Updated Terraform modules |

---  

**End of Document**