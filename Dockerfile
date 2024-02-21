FROM python:3.10
LABEL authors="PyCrafters"

# Set the environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /wic_app

# Set the working directory inside the container
WORKDIR $APP_HOME

# Copying your application to the container
COPY src $APP_HOME/src
COPY LICENSE $APP_HOME
COPY README.md $APP_HOME
COPY requirements.txt $APP_HOME

# Installing dependencies
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install tensorflow

# Run the application
ENTRYPOINT ["python", "src/web_image_classifier/manage.py", "runserver", "0.0.0.0:80"]