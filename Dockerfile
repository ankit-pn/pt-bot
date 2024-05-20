# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages
RUN pip install --no-cache-dir psutil requests

# Run monitor_processes.py when the container launches
CMD ["python", "monitor_processes.py"]
