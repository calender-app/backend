# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL='postgresql://riajul:password@postgres:5432/caleappp'
ENV API_TOKEN='sdf23sdfsafasfdasqweqweasdsadasd'

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y postgresql-client

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN python -m venv venv
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the image
COPY . /app/

# Expose your application's port (if needed)
EXPOSE 8000

# Add Alembic migration command
CMD ["alembic", "upgrade", "head"]