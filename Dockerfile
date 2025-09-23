# Use a base image with a specific version of Python
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your application will run on
EXPOSE 5000

# Define the command to run your application when the container starts
CMD ["python", "app.py"]