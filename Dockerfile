# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script and other necessary files to the container
COPY . .

# Expose the port used by the Quart application
EXPOSE 5000

# Run the Python script when the container starts
CMD ["python", "app.py"]
