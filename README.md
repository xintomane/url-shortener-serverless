# AWS Serverless URL Shortener

A serverless URL shortener built using **Amazon API Gateway, AWS Lambda, and DynamoDB**.

This project demonstrates cloud-native architecture, observability, and scalable design using AWS managed services.

---

## 🏗 Architecture

## Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        Client[Client/Browser]
    end

    subgraph "API Layer"
        APIGW[Amazon API Gateway<br/>REST API<br/>POST /shorten<br/>GET /{code}]
        APIGW_Logs[API Gateway<br/>Access Logs]
    end

    subgraph "Compute Layer"
        ShortenLambda[AWS Lambda<br/>shortenUrl<br/>Generate short code<br/>Store mapping]
        RedirectLambda[AWS Lambda<br/>redirectUrl<br/>Retrieve URL<br/>Increment clicks<br/>Return 302 redirect]
        Lambda_Logs[Lambda Function<br/>Execution Logs]
    end

    subgraph "Data Layer"
        DynamoDB[(Amazon DynamoDB<br/>Table: ShortUrls<br/>PK: shortCode<br/>Attributes: longUrl, createdAt, clicks, ttl<br/>TTL Enabled)]
    end

    subgraph "Observability Layer"
        CloudWatch[Amazon CloudWatch<br/>Centralized Logging & Monitoring]
    end

    %% Traffic Flow - Shorten URL
    Client -->|1. POST /shorten<br/>{longUrl}| APIGW
    APIGW -->|2. Invoke| ShortenLambda
    ShortenLambda -->|3. PutItem<br/>{shortCode, longUrl, createdAt, ttl}| DynamoDB
    DynamoDB -->|4. Success| ShortenLambda
    ShortenLambda -->|5. Return<br/>{shortUrl}| APIGW
    APIGW -->|6. 200 OK<br/>{shortUrl}| Client

    %% Traffic Flow - Redirect
    Client -->|7. GET /{code}| APIGW
    APIGW -->|8. Invoke| RedirectLambda
    RedirectLambda -->|9. GetItem & UpdateItem<br/>Increment clicks| DynamoDB
    DynamoDB -->|10. Return longUrl| RedirectLambda
    RedirectLambda -->|11. 302 Redirect<br/>Location: longUrl| APIGW
    APIGW -->|12. 302 Redirect| Client

    %% Logging Flow
    APIGW -.->|Access Logs| APIGW_Logs
    ShortenLambda -.->|Execution Logs| Lambda_Logs
    RedirectLambda -.->|Execution Logs| Lambda_Logs
    APIGW_Logs -.->|Stream| CloudWatch
    Lambda_Logs -.->|Stream| CloudWatch

    %% Styling
    classDef apiLayer fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#232F3E
    classDef computeLayer fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#232F3E
    classDef dataLayer fill:#3B48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef observability fill:#759C3E,stroke:#232F3E,stroke-width:2px,color:#232F3E
    classDef client fill:#232F3E,stroke:#FF9900,stroke-width:2px,color:#fff

    class APIGW,APIGW_Logs apiLayer
    class ShortenLambda,RedirectLambda,Lambda_Logs computeLayer
    class DynamoDB dataLayer
    class CloudWatch observability
    class Client client
```

## Component Details

### API Layer

- **Amazon API Gateway (REST API)**
  - Public entry point for all requests
  - Two endpoints:
    - `POST /shorten` - Create short URL
    - `GET /{code}` - Redirect to original URL
  - Access logging enabled

### Compute Layer

- **shortenUrl Lambda Function**
  - Generates unique short codes
  - Stores URL mappings in DynamoDB
  - Sets TTL for automatic expiration
  - Returns short URL to client

- **redirectUrl Lambda Function**
  - Retrieves original URL from DynamoDB
  - Increments click counter
  - Returns HTTP 302 redirect response

### Data Layer

- **DynamoDB Table: ShortUrls**
  - **Partition Key**: `shortCode` (String)
  - **Attributes**:
    - `longUrl` (String) - Original URL
    - `createdAt` (Number) - Unix timestamp
    - `clicks` (Number) - Click counter
    - `ttl` (Number) - Time-to-live for automatic expiration
  - **TTL Enabled**: Automatic deletion of expired links

### Observability Layer

- **Amazon CloudWatch**
  - Centralized logging and monitoring
  - API Gateway access logs
  - Lambda execution logs
  - Metrics and alarms (optional)

## Traffic Flow

### Create Short URL (Steps 1-6)

1. Client sends POST request to `/shorten` with `longUrl`
2. API Gateway invokes `shortenUrl` Lambda
3. Lambda generates short code and stores mapping in DynamoDB
4. DynamoDB confirms successful write
5. Lambda returns short URL
6. API Gateway returns 200 OK with short URL

### Redirect to Original URL (Steps 7-12)

7. Client accesses short URL via GET `/{code}`
8. API Gateway invokes `redirectUrl` Lambda
9. Lambda retrieves item and increments click counter
10. DynamoDB returns original URL
11. Lambda returns 302 redirect with Location header
12. API Gateway forwards redirect to client

## AWS Best Practices Implemented

✓ **Serverless Architecture** - No server management, auto-scaling
✓ **Pay-per-use** - Only charged for actual requests
✓ **High Availability** - Multi-AZ deployment by default
✓ **Security** - IAM roles for Lambda execution
✓ **Observability** - Comprehensive logging with CloudWatch
✓ **Data Lifecycle** - Automatic expiration with DynamoDB TTL
✓ **Performance** - Single-digit millisecond DynamoDB latency

## Additional Considerations

- **Security**: Add API Gateway authentication (API keys, Cognito, or IAM)
- **Rate Limiting**: Configure API Gateway throttling
- **Custom Domains**: Use Route 53 + CloudFront for branded short URLs
- **Monitoring**: Set up CloudWatch alarms for errors and latency
- **Backup**: Enable DynamoDB point-in-time recovery

### Request Flow

**Create Short URL**

1. Client sends POST `/shorten`
2. API Gateway invokes `shortenUrl` Lambda
3. Lambda stores mapping in DynamoDB
4. API returns generated short code

**Redirect**

1. Client requests `/{code}`
2. API Gateway invokes `redirectUrl` Lambda
3. Lambda retrieves URL & increments click counter
4. Returns HTTP **302 redirect**

---

## 🚀 Features

✅ Serverless architecture  
✅ URL shortening & redirection  
✅ Click analytics (atomic counter)  
✅ DynamoDB TTL for automatic expiration  
✅ API Gateway access logging  
✅ CloudWatch observability  
✅ High availability & auto scaling

---

## 🧰 Tech Stack

- Amazon API Gateway (REST)
- AWS Lambda (Python)
- Amazon DynamoDB
- Amazon CloudWatch Logs
- IAM Roles & Policies

---

## 🔌 API Endpoints

### Create short URL

**POST** `/shorten`

**Request**

```json
{ "url": "https://google.com" }
```
