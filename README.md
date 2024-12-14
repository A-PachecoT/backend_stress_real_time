# StressMinder API

A real-time stress monitoring and analysis system built with FastAPI that processes multiple physiological and behavioral parameters to assess stress levels.

## Overview

StressMinder API provides a comprehensive stress analysis by combining:
- Physiological sensors (temperature, heart rate)
- Facial expression analysis
- PSS-10 (Perceived Stress Scale) questionnaire responses

## Key Features

- **Real-time Monitoring**: Continuous collection and analysis of sensor data
- **Multi-parameter Analysis**: Combined analysis of physical and psychological indicators
- **Standardized Assessment**: Integration with PSS-10 questionnaire
- **Stress Level Classification**: Automated stress level categorization (Low, Moderate, High)

## Architecture

The system calculates stress levels using:
1. **Partial Indices (IP)**: Individual normalized measurements
2. **Total Stress Index (ITE)**: Weighted combination of all parameters

### Calculation Weights
- Temperature: 10%
- Heart Rate: 10%
- Facial Expression: 40%
- PSS-10 Score: 40%

## API Endpoints

- `/api/v1/sensors`: Sensor data collection
- `/api/v1/questions`: PSS-10 questionnaire handling
- `/api/v1/results`: Stress analysis results
- `/api/v1/auth`: User authentication

## Getting Started

For development setup and contribution guidelines, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

### Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Start the application:
```bash
make dev
```

## Documentation

- API Documentation: `http://localhost:8000/docs`
- ReDoc Interface: `http://localhost:8000/redoc`

## License

This project is licensed under the MIT License.