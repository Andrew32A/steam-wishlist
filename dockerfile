# Base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port your Flask app will be running on
EXPOSE 5000

# Run the Flask app with Gunicorn
CMD gunicorn app:app --bind 0.0.0.0:5000