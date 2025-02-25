# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (if applicable)
# Replace 8051 with the port your app uses
EXPOSE 8051

# Define the command to run your Streamlit application
CMD ["streamlit", "run", "streamlit_app.py"]