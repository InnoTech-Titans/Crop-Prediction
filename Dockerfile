FROM python:3.9

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a new user named 'appuser'
RUN useradd -m -s /bin/bash appuser

# Set the working directory and ownership
WORKDIR /code
RUN chown -R appuser:appuser /code

# Switch to the newly created user
USER appuser

# Mounts the application code to the image
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
