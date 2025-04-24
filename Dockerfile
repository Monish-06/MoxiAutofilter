# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install the required dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port (optional)
EXPOSE 5000

# Run the bot
CMD ["python", "main.py"]
