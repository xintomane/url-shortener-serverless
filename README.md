# AWS Serverless URL Shortener

A serverless URL shortener built using **Amazon API Gateway, AWS Lambda, and DynamoDB**.

This project demonstrates cloud‑native architecture, observability, and scalable design using AWS managed services.

---

## 🏗 Architecture

```mermaid
graph TB
  subgraph Client
    C["Client / Browser"]
  end

  subgraph API["Amazon API Gateway (REST)"]
    APIGW["POST /shorten | GET /{code}"]
  end

  subgraph Compute["AWS Lambda"]
    L1["shortenUrl: generate short code + store mapping"]
    L2["redirectUrl: retrieve URL + increment clicks + return 302"]
  end

  subgraph Data["Amazon DynamoDB"]
    DB[("ShortUrls table (PK: shortCode)")]
  end

  subgraph Observability["Amazon CloudWatch"]
    CW["Logs & Monitoring"]
  end

  C -->|POST /shorten| APIGW
  APIGW --> L1
  L1 -->|PutItem| DB
  L1 --> APIGW
  APIGW --> C

  C -->|GET /{code}| APIGW
  APIGW --> L2
  L2 -->|GetItem + Update clicks| DB
  L2 -->|302 Location| APIGW
  APIGW --> C

  APIGW -. Access Logs .-> CW
  L1 -. Logs .-> CW
  L2 -. Logs .-> CW
```

---

## 🚀 Features

- Serverless architecture
- URL shortening & redirection
- Click analytics (atomic counter)
- DynamoDB TTL for automatic expiration
- API Gateway access logging
- CloudWatch observability
- High availability & auto scaling

---

## 🧰 Tech Stack

- Amazon API Gateway (REST)
- AWS Lambda (Python)
- Amazon DynamoDB
- Amazon CloudWatch Logs
- IAM Roles & Policies

---

## 🔌 API EndPoints

### Create short URL

**POST** `/shorten`

**Request**

```json
{ "url": "https://google.com" }
```

**Response**

```json
{ "shortCode": "p7BHUw" }
```

---

### Redirect

**GET** `/{code}`

Returns:

- HTTP 302 redirect
- `Location` header with original URL

---

## 🧪 Testing

### Create short URL

```bash
curl -X POST "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/shorten"   -H "Content-Type: application/json"   --data-raw '{"url":"https://google.com"}'
```

### Redirect

```bash
curl -i "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/p7BHUw"
```

---

## 🗄 DynamoDB Schema

**Table:** `ShortUrls`

| Attribute | Type        | Description          |
| --------- | ----------- | -------------------- |
| shortCode | String (PK) | unique short link    |
| longUrl   | String      | original URL         |
| createdAt | String      | timestamp            |
| clicks    | Number      | redirect counter     |
| ttl       | Number      | expiration timestamp |

TTL automatically deletes expired links.

---

## 📊 Observability

### API Gateway Access Logs

CloudWatch logs include:

- requestId
- path & method
- response status
- latency
- client IP

### Lambda Logs

Lambda execution logs are stored in CloudWatch for debugging and tracing.

---

## 🏗 AWS Best Practices Implemented

- Fully serverless & auto scaling
- Pay-per-use cost model
- IAM least-privilege roles
- Built-in high availability
- Observability with CloudWatch
- Data lifecycle management (TTL)

---

## 🔮 Future Improvements

- Custom domain + CloudFront
- WAF & rate limiting
- Authentication (Cognito / API keys)
- Link preview metadata
- Terraform IaC

---

## 👩🏽‍💻 Author

**Xintomane Mahange**  
Cloud Support Engineer @ AWS
