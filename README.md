# GeoWhisper Backend

A location-aware AI walking and exploration backend service.

## Features
- Real-time location updates
- Movement detection
- AI-generated insights about surroundings
- Clean Architecture / FastAPI / Async

## Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### Running Locally

1. **Start Infrastructure**
   ```bash
   docker-compose up -d
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run App**
   ```bash
   uvicorn app.main:app --reload
   ```

## Development
- `main`: Stable production branch
- `develop`: Active development