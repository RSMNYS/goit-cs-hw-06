# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 3001 and 5001 available to the world outside this container
EXPOSE 3001
EXPOSE 5001

# Define environment variable
ENV NAME World

# Define the default command to run when the container starts
CMD ["python", "main.py"]