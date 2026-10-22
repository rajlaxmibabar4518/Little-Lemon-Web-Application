LITTLE LEMON - Back-End Developer Capstone (Django REST Framework + MySQL)
==========================================================================

API PATHS TO TEST (base URL: http://127.0.0.1:8000)
---------------------------------------------------
/                          (static HTML home page)
/about/  /menu/  /book/    (static HTML pages)
/api/registration/         POST   create a user and receive a token
/api/token/                POST   log in with username + password, receive a token
/api/me/                   GET    protected - needs header  Authorization: Token <token>
/api/menu/                 GET (public), POST (token)
/api/menu/1/               GET (public), PUT/PATCH/DELETE (token)
/api/bookings/             GET, POST (token required)
/api/bookings/1/           GET, PUT, PATCH, DELETE (token required)
/admin/                    Django admin

SETUP
-----
1. Create the MySQL database:
     mysql -u root -p -e "CREATE DATABASE littlelemon CHARACTER SET utf8mb4;"
2. Create and activate a virtual environment, then install packages:
     python -m venv venv
     venv\Scripts\activate        (Windows)   |   source venv/bin/activate   (macOS/Linux)
     pip install -r requirements.txt
3. Set DB credentials (defaults: user root, password root, host 127.0.0.1, port 3306):
     Windows PowerShell:  $env:DB_PASSWORD="your_password"
     macOS/Linux:         export DB_PASSWORD=your_password
   (Or edit the DATABASES block in littlelemon/settings.py.)
4. Run migrations, create admin, start server:
     python manage.py migrate
     python manage.py createsuperuser
     python manage.py runserver
5. Run unit tests:
     python manage.py test

TESTING WITH INSOMNIA
---------------------
1. POST /api/registration/  JSON: {"username":"peer","email":"peer@example.com","password":"StrongPass!234"}
   -> response contains "token".  (Or POST /api/token/ with username + password.)
2. For protected requests add header:  Authorization: Token <your token>
3. POST /api/menu/      JSON: {"title":"Greek Salad","price":"12.50","inventory":20}
4. POST /api/bookings/  JSON: {"first_name":"Sam","reservation_date":"2026-12-01","reservation_slot":19}
5. GET /api/menu/ and GET /api/bookings/ to verify.
An importable Insomnia collection is included: insomnia_collection.json
