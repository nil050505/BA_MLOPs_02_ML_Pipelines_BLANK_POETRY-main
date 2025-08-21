# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster
# Using Python 3.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Don't store pip cache to reduce image size
# -r: Install from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application file into the container at /app
COPY app.py /app/

# Copy the 'src' directory containing config.py and other modules
# This is crucial for resolving imports like 'src.config'
COPY src/ /app/src/

# Copy the 'model_store' directory containing your trained model
# Ensure that 'model_store/churn_prediction_model_v1.joblib' exists in your host machine
# before building the Docker image.
COPY model_store/ /app/model_store/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application using Uvicorn
# 'app:app' refers to the 'app' object inside 'app.py'
# '--host 0.0.0.0' makes the server accessible from outside the container
# '--port 8000' specifies the port it listens on
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]