# Django HRM System

This is a simple HRM (Human Resource Management) System built with Django and the Django Admin Panel.

## Features

- Manage companies and locations
- Manage employee information such as name, address, tax number, etc.
- Upload and manage documents for each employee
- Ability to download documents as a ZIP file
- Ability to download employee data as an Excel table

## Prerequisites

- Python 3.8
- Docker

## Installation and Running

### With Git and Python

1. Clone the repository:

    ```bash
    git clone https://github.com/Keykubat60/HR-Management.git
    ```

2. Navigate into the directory:

    ```bash
    cd .\HR-Management\
    ```
   
3. deploy Projekt:

    ```bash
    docker-compose up -d       
    ``` 
   
4. Navigate into the directory:

    ```bash
    docker compose run --rm web python manage.py makemigrations
    ```
   
5. migrate DB:

    ```bash
    docker compose run --rm web python manage.py migrate
    ```
  
6. create user:

    ```bash
    docker compose run --rm web python manage.py createsuperuser
    ``` 



7. create static files:

    ```bash
    docker-compose run --rm web python manage.py collectstatic --noinput
    ```


Now the application should be running, and you can access it in your browser at `http://127.0.0.1:8000/`.
