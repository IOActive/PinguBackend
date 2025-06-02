# PinguCrew Backend Setup

This document provides instructions for setting up the PinguCrew backend for local development and Docker-based deployment.

## Prerequisites

Ensure the following tools are installed on your system:

- Python 3.8+
- pip
- Docker and Docker Compose
- Git

## Local Development Setup

Follow these steps to set up the backend for local development:

1. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Configuration**

   - Update the configuration files in the `config/` directory as needed.
   - Example: Update `config/system/config.yaml` with your desired `SECRET_KEY`.

5. **Run Bootstrap Script**

   Use the provided bootstrap script to initialize the database, message queues, and other components:

   ```bash
   bash src/bootstrap/bootstrap.sh
   ```

6. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```
---

## Docker Deployment Setup

Follow these steps to deploy the backend using Docker:


1. **Build and Start Docker Containers**

   ```bash
   docker-compose up --build
   ```
2. **Verify Services**

   - Access the backend at `http://localhost:8086`.
   - Verify other services (e.g., RabbitMQ, Minio) using their respective ports.
---

## Notes

- Update sensitive credentials in the configuration files (`config/`) before deployment.
- For production, ensure to use secure values for environment variables like `SECRET_KEY`, `POSTGRES_PASSWORD`, and `MINIO_ROOT_PASSWORD`.
