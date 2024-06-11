FROM python:3.12-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./ /app

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
