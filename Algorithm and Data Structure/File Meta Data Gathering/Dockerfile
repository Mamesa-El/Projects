# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World
ENV GITHUB_REPO_URL=https://raw.githubusercontent.com/jimmyislive/sample-files/master/

# Run file_metadata.py when the container launches
CMD ["python", "metadata.py"]
