To add a section on creating a superuser in Django, I'll include it under the "Setup" section. Here's the updated documentation:

---

# Property Project

## Overview

This project is a Django application for managing property information. It includes features to migrate data from a Scrapy project into a Django model, manage property listings, and handle property images.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Migration Command](#migration-command)
- [Create a Superuser](#create-a-superuser)

## Requirements

- Python 3.x
- Django 5.x
- psycopg2
- requests
- PostgreSQL

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bishworup002/property_project.git
   cd property_project
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a Superuser**

   After applying migrations, create a superuser to access the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to set up a username, email, and password.

## Configuration

1. **Set Up Database**

   Ensure that PostgreSQL is installed and running. Create a database named `hotel` and configure the credentials in `config.py`:

   ```python
   # config.py

   # Scrapy project's database configuration
   SCRAPY_DB = {
       "dbname": "trip",  # Replace with your Scrapy DB name
       "user": "postgres",
       "password": "p@stgress",
       "host": "localhost",
       "port": "5433",
   }

   # Django project's database configuration
   DJANGO_DB = {
       "ENGINE": "django.db.backends.postgresql",
       "NAME": "hotel",
       "USER": "postgres",
       "PASSWORD": "p@stgress",
       "HOST": "localhost",
       "PORT": "5433",
   }

   # Security settings
   SECRET_KEY = "django-insecure-_^if9w822)#2!5citetave_9lct@ig#87n*y2rtti6=0l(=2wf"
   DEBUG = True
   ALLOWED_HOSTS = []
   ```

2. **Apply Migrations**

   Run the following command to create the necessary database tables:

   ```bash
   python manage.py migrate
   ```

## Migration Command

To migrate data from the Scrapy project's database into the Django models, use the custom management command:

```bash
python manage.py migrate_data
```

## Running the Project

1. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```  
   The application will be accessible at `http://localhost:8000/admin/` or `http://localhost:8000/`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

--- 

This update adds a step to create a Django superuser after the migrations are applied.