BarangayCare
A Patient Visit and Medicine Inventory System for a Barangay Health Center

PROJECT DESCRIPTION

BarangayCare is a web-based system developed using Django and PostgreSQL to help manage patient records and health center operations. It provides authorized health center personnel with a centralized platform for managing patient information and recording patient visits.

CURRENT FEATURES

- User registration and login
- Role-based access for Admin and Health Workers
- User profile management
- Staff account creation by Admin
- Patient registration and record management
- Patient search
- Patient visit recording and management
- Visit date validation
- Role-based access to patient and visit records

TECHNOLOGIES USED

- Python
- Django
- PostgreSQL
- Supabase
- HTML
- CSS
- JavaScript
- Git and GitHub

INSTALLATION AND SETUP

1. Clone the repository:

git clone https://github.com/satriozzz/-BarangayCare-Gustilo-GianCarlo-G02.git

2. Navigate to the project folder:

cd -BarangayCare-Gustilo-GianCarlo-G02

3. Create a virtual environment:

py -m venv venv

4. Activate the virtual environment:

venv\Scripts\activate

5. Install dependencies:

py -m pip install -r requirements.txt

6. Create a .env file in the project root and configure the required environment variables:

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-database-url

7. Apply database migrations:

py manage.py migrate

8. Start the development server:

py manage.py runserver

9. Open the following address in your browser:

http://127.0.0.1:8000/

PROJECT REPOSITORY

https://github.com/satriozzz/-BarangayCare-Gustilo-GianCarlo-G02

DEVELOPER

Gian Carlo Gustilo
BS Information Technology
Cebu Institute of Technology–University