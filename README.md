# BarangayCare
**A Patient Visit Management System for a Barangay Health Center**

## PROJECT DESCRIPTION

BarangayCare is a web-based system developed using Django and PostgreSQL to help manage patient records and patient visits in a barangay health center. It provides authorized health center personnel with a centralized platform for managing patient information and recording patient visits.

## CURRENT FEATURES

- Admin and Health Worker login and logout
- Role-based access for Admin and Health Workers
- User profile viewing and editing
- Staff account creation by Admin
- Patient registration and record management
- Patient search
- Patient visit recording and management
- Visit date validation
- Role-based access to patient and visit records
- Protection against unauthorized record access

## TECHNOLOGIES USED

- Python
- Django
- PostgreSQL
- Supabase
- HTML
- CSS
- JavaScript
- Git and GitHub

## INSTALLATION AND SETUP

### 1. Clone the repository

```cmd
git clone https://github.com/satriozzz/-BarangayCare-Gustilo-GianCarlo-G02.git
```

### 2. Navigate to the project folder

```cmd
cd -BarangayCare-Gustilo-GianCarlo-G02
```

### 3. Create a virtual environment

```cmd
py -m venv venv
```

### 4. Activate the virtual environment

```cmd
venv\Scripts\activate
```

### 5. Install dependencies

```cmd
py -m pip install -r requirements.txt
```

### 6. Configure environment variables

Copy `.env.example` and rename the copy to `.env`.

```cmd
copy .env.example .env
```

Open `.env` and configure the following variables using your own values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-supabase-postgresql-connection-string
```

**Important:** BarangayCare requires a PostgreSQL database. SQLite is not supported.

### 7. Apply database migrations

```cmd
py manage.py migrate
```

### 8. Start the development server

```cmd
py manage.py runserver
```

### 9. Open the application

Visit:

http://127.0.0.1:8000/

## RUNNING TESTS

To run the project's automated tests:

```cmd
py manage.py test
```

If the Supabase test database cleanup issue occurs, the following command can be used to preserve the test database:

```cmd
py manage.py test --keepdb
```

## PROJECT DOCUMENTATION

PD2 and PD3 completion reports are located in the `docs/` directory.

## PROJECT REPOSITORY

https://github.com/satriozzz/-BarangayCare-Gustilo-GianCarlo-G02

## DEVELOPER

Gian Carlo Gustilo  
BS Information Technology  
Cebu Institute of Technology–University