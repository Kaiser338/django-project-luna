FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /django-app

#dependencies install
COPY requirements.txt /django-app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /django-app/

# Run app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
