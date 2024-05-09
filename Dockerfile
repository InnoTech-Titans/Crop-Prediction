FROM python:3.9

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt




# Mounts the application code to the image
COPY . code

WORKDIR /code


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
