# Use the official Python base image since its python project
# if it was js app you would choose Node image
FROM python:3.10-slim


# Set the working directory inside the container where the 
# application code will be placed
WORKDIR /app

# Copy the current directoryFILES into the container in /app
COPY . /app/

# Install packages specified in requirements.txt .
# The RUN instruction executes a command in the Docker image. 
RUN pip install --no-cache-dir -r requirements.txt


# EXPOSE make port 8000 available to the world outside this container
# does not really make it accessible to the world but To make the 
# port accessible to the host machine, you need to publish the port when
# running the container using the -p or --publish option.
EXPOSE 8000


CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]