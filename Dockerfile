# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the startup script into the container
COPY startup.sh /opt/startup/startup.sh

# Make the startup script executable
RUN chmod +x /opt/startup/startup.sh

# Set the entry point to the startup script
CMD ["/opt/startup/startup.sh"]