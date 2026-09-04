# Use the official slim Python 3.12 base image for a smaller production container
FROM python:3.12-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy only the requirements file first so dependencies can be installed separately
COPY requirements.txt ./

# Install Python dependencies from requirements.txt without caching wheels
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Start the FastAPI app with Uvicorn, listening on all network interfaces at port 8000
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]