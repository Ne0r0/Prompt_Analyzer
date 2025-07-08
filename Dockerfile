# Use an official lightweight Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI default port
EXPOSE 5000

# Define the command to run the FastAPI
CMD ["uvicorn", "analyzer_api:app", "--host", "0.0.0.0", "--port", "5000"]
