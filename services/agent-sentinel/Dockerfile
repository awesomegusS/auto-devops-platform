# We use a slim Python image to keep it fast
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file we generated earlier
COPY requirements.txt .

# Install the dependencies (docker, openai, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src

# Run the agent
CMD ["python", "src/main.py"]