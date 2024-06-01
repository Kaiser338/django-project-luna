# Luna Django Project
## Requirements

### Install Docker and Docker Compose:

Ensure you have Docker and Docker Compose installed on your machine. You can follow the official documentation for installation instructions:

[Docker](https://docs.docker.com/engine/install/)
[Docker Compose](https://docs.docker.com/compose/install/)

## Installation

### Clone the Repository:
```
git clone https://github.com/kaiser338/django-project-luna.git
```

### Create a .env File:
Create a .env file in the root directory of the project with the following contents:
```
# PostgreSQL Configuration
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_username
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django Configuration
DEBUG=1
DJANGO_SECRET_KEY=your_django_secret_key
```

Replace `your_database_name`, `your_database_username`, `your_database_password`, and `your_django_secret_key` with appropriate values for your project

### Build and Start Docker Containers:

```
docker-compose up --build
```


### Run Migrations:
```
docker-compose exec web python django-app/manage.py migrate
```


### Start Docker Image:
```
docker-compose up
```