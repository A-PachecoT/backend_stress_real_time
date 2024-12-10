# Stress Monitoring System

A Python-based system for monitoring and analyzing stress levels using multiple physiological and behavioral parameters.

## Components

### Data Collection
- `insert_sensor_data.py`: Handles sensor data collection and database insertion
  - Collects temperature and heart rate readings
  - Supports manual and automated data collection
  - Includes random data generation for testing

### Data Processing
- `scripts/1.preguntas.py`: PSS-10 (Perceived Stress Scale) questionnaire processing
- `scripts/2.procesamiento.py`: Core stress index calculation
- `scripts/3.normalizar.py`: Parameter normalization and partial index calculation

### Database Management
- `db_explorer.py`: Database exploration and management tool
  - Provides detailed database structure visualization
  - Supports sample data viewing
  - Shows foreign key relationships

## Stress Index Calculation

The system calculates stress levels using multiple parameters:
1. Physiological data (heart rate, temperature)
2. PSS-10 questionnaire responses
3. Angular velocity measurements
4. Facial expression analysis

Parameters are normalized and weighted to produce:
- IP (Partial Index): Individual measurement score
- ITE (Total Stress Index): Aggregate stress score

## Configuration

Database connection parameters:
- Host: stress-prueba1.cna4icyokmxm.us-east-2.rds.amazonaws.com
- Database: sensores_db

## Usage

1. Data Collection: Run insert_sensor_data.py and follow the interactive menu to:
   - Insert single sensor readings
   - Generate multiple random readings
   - Start continuous monitoring with custom intervals

2. Database Exploration: Execute db_explorer.py to:
   - View available databases
   - Explore table structures
   - Examine data relationships

3. Stress Analysis: Use the processing scripts to:
   - Process PSS-10 questionnaire responses
   - Calculate normalized stress indices
   - Generate stress level reports