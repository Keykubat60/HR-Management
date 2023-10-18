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

3. Start the Docker containers:

    ```bash
    docker-compose up
    ```

Now the application should be running, and you can access it in your browser at `http://127.0.0.1:8000/`.
