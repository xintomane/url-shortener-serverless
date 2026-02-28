# AWS Serverless URL Shortener

A serverless URL shortener built on AWS using **API Gateway**, **Lambda**, and **DynamoDB**.

This project demonstrates serverless architecture, observability, and DynamoDB access patterns used in real-world cloud systems.

---

## Architecture

![Architecture](docs/architecture.png)

---

## Features

✅ Create short URLs  
✅ HTTP 302 redirects  
✅ Click analytics counter  
✅ DynamoDB TTL for automatic expiration  
✅ API Gateway access logging  
✅ CloudWatch observability  
✅ Fully serverless & auto-scaling

---

## Architecture Overview

**API Layer**

- Amazon API Gateway (REST)
- POST `/shorten`
- GET `/{code}`

**Compute Layer**

- Lambda: `shortenUrl`
- Lambda: `redirectUrl`

**Data Layer**

- DynamoDB table: **ShortUrls**
- Partition key: `shortCode`

**Observability**

- CloudWatch access logs
- Lambda execution logs

---

## How It Works

### Create Short URL

1. Client sends POST `/shorten`
2. Lambda generates short code
3. Mapping stored in DynamoDB
4. Short code returned

### Redirect

1. Client visits short URL
2. Lambda retrieves original URL
3. Click counter increments
4. HTTP 302 redirect returned

---

## API Usage

### Create short URL

```bash
curl -X POST "<INVOKE_URL>/shorten" \
-H "Content-Type: application/json" \
--data-raw '{"url":"https://google.com"}'
```
