

# Property Project With Ollama

## Overview

This Django CLI application enhances property information by rewriting titles and generating summaries and descriptions using the Ollama model. It integrates with PostgreSQL to store updated data in the existing property table and a newly created summary table. The application leverages Django ORM for efficient data management and processing.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Generate and Update Database Command](#generate-and-update-database-command)
- [License](#license)

## Requirements

- Python 3.x
- Django 5.x
- psycopg2
- requests
- PostgreSQL
- Ollama

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bishworup002/Django_With_Ollama.git
   cd Django_With_Ollama
   ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

    Or

    ```bash
    python3 -m venv venv
    source venv/bin/activate  
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```
 4. **Install and Start Ollama**
   
   Follow the instructions at Ollama's official website to install Ollama on your system.

5. **Pull the Required Model**

   Pull the required model (e.g., gemma2:2b):

   ```bash
   ollama pull gemma2:2b
   ```   

## Configuration

1. **Create `config.py`**

    ```bash
    touch config.py
    ```

2. **Set Up Database**

    Ensure that PostgreSQL is installed and running. Create a database and configure the credentials in `config.py`:

    ```python
    # config.py

    # Django project's database configuration
    DJANGO_DB = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "hotel",  # Replace with your DB name
        "USER": "postgres",  # Replace with your username
        "PASSWORD": "password",  # Replace with your password
        "HOST": "localhost",
        "PORT": "5433",
    }

    # Security settings
    SECRET_KEY = "your_secret_key"  # Replace with your SECRET_KEY
    DEBUG = True
    ALLOWED_HOSTS = []
    ```

3. **Database Creation**
   Before running the project, create the Django database. Ensure that the database name in `config.py` under `django_database_config` matches the created database. Execute this SQL command:

   ```sql
   CREATE DATABASE database_name;
   ```


4. **Database Setup**
   You have two options for setting up the database tables:
   
   * **Manual Creation:** Execute the necessary SQL commands to create the tables manually.
   * **Automatic Creation via Migrations:** Use Django's migration system (recommended). This ensures the database schema matches your project's models:
    

5. **Apply Migrations**

    Run the following commands to create the necessary database tables:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

# Django Database Creation Guide

Before running the project, you need to create the database and tables for your Django models. Here's a step-by-step guide to manually create the database and tables:

## Database Creation

First, create the database using the following SQL command:

```sql
CREATE DATABASE your_database_name;
```

Replace `your_database_name` with the name specified in your Django settings.

## Table Creation

Now, let's create the tables for each model:

### Amenity Table

```sql
CREATE TABLE amenity (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
```

### Location Table

```sql
CREATE TABLE location (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    CONSTRAINT type_choices CHECK (type IN ('country', 'state', 'city'))
);
```

### Property Table

```sql
CREATE TABLE property (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(1000) DEFAULT '',
    create_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### PropertyImage Table

```sql
CREATE TABLE property_image (
    id SERIAL PRIMARY KEY,
    image VARCHAR(100) NOT NULL,
    property_id INTEGER NOT NULL,
    FOREIGN KEY (property_id) REFERENCES property (id) ON DELETE CASCADE
);
```

### PropertySummary Table

```sql
CREATE TABLE property_summary (
    id SERIAL PRIMARY KEY,
    summary TEXT NOT NULL,
    property_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (property_id) REFERENCES property (id) ON DELETE CASCADE
);
```

### Many-to-Many Relationship Tables

For the many-to-many relationships between Property and Location, and Property and Amenity:

```sql
CREATE TABLE property_locations (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    FOREIGN KEY (property_id) REFERENCES property (id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location (id) ON DELETE CASCADE
);

CREATE TABLE property_amenities (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL,
    amenity_id INTEGER NOT NULL,
    FOREIGN KEY (property_id) REFERENCES property (id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenity (id) ON DELETE CASCADE
);
```



## Create a Superuser**

    After applying migrations, create a superuser to access the Django admin panel:

    ```bash
    python manage.py createsuperuser
    ```

## Generate and Update Database Command

To update the database with data generated from the Django project, use the custom management command. **This process may take a few minutes, please wait.**

```bash
python manage.py generate_descriptions
```

## Running the Project

1. **Start the Development Server**

    ```bash
    python manage.py runserver
    ```


2. Access the application at <h3> `http://127.0.0.1:8000` </h3>

3. Access the admin panel at <h3> `http://127.0.0.1:8000/admin` </h3>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---