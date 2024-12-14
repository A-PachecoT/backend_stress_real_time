# StressMinder API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints except `/auth/login` and `/auth/register` require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

Request Body:
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

Response:
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true
}
```

#### Login
```http
POST /auth/login
```

Request Body:
```json
{
  "username": "string",
  "password": "string"
}
```

Response:
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### Sensors

#### Submit Sensor Reading
```http
POST /sensors
```

Request Body:
```json
{
  "temperatura": 36.5,
  "ritmo_cardiaco": 75.0,
  "indice_facial": 0.65
}
```

Response:
```json
{
  "id": 1,
  "temperatura": 36.5,
  "ritmo_cardiaco": 75.0,
  "indice_facial": 0.65,
  "timestamp": "2024-01-20T15:30:00Z"
}
```

#### Get Latest Readings
```http
GET /sensors/latest?minutes=5
```

Query Parameters:
- `minutes` (optional): Number of minutes to look back (default: 5)

Response:
```json
[
  {
    "id": 1,
    "temperatura": 36.5,
    "ritmo_cardiaco": 75.0,
    "indice_facial": 0.65,
    "timestamp": "2024-01-20T15:30:00Z"
  }
]
```

### PSS-10 Questionnaire

#### Submit Question Response
```http
POST /questions
```

Request Body:
```json
{
  "question_number": 1,
  "answer_value": 2
}
```
Note: `answer_value` range is 0-4 (nunca-siempre)

Response:
```json
{
  "id": 1,
  "question_number": 1,
  "answer_value": 2,
  "user_id": 1,
  "timestamp": "2024-01-20T15:30:00Z"
}
```

#### Get PSS-10 Result
```http
GET /questions/pss10
```

Response:
```json
{
  "total_score": 25,
  "stress_level": "Moderado",
  "timestamp": "2024-01-20T15:30:00Z"
}
```

### Stress Analysis

#### Get Stress Analysis Results
```http
GET /results?minutes=30
```

Query Parameters:
- `minutes` (optional): Time window for analysis in minutes (default: 30)

Response:
```json
{
  "timestamp": "2024-01-20T15:30:00Z",
  "total_stress_index": 0.65,
  "pss10_score": 25,
  "stress_level": "Moderado",
  "partial_indices": [0.58, 0.62, 0.70, 0.65]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Calculation Details

### Stress Level Categories
- **Bajo**: 0-33%
- **Moderado**: 34-66%
- **Alto**: 67-100%

### Parameter Weights
- Temperature: 10%
- Heart Rate: 10%
- Facial Expression: 40%
- PSS-10 Score: 40%
