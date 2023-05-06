# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Run app.py when the container launches on localhost:4500
EXPOSE 4500
CMD ["python3", "app.py", "--host=0.0.0.0"]

# docker build -t processor-lab .
# docker run -d --name p-lab -p 4500:4500 processor-lab
