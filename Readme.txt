LITTLE LEMON - Back-End Developer Capstone (Django REST Framework + MySQL + Djoser)
===================================================================================
Project: littlelemon      App: restaurant

API PATHS TO TEST (base URL: http://127.0.0.1:8000)
---------------------------------------------------
/                              static HTML home page (index.html)
/about/  /menu/  /book/        static HTML pages
/auth/users/                   POST  register a user (djoser)  {"username","email","password"}
/auth/token/login/             POST  log in (djoser) -> returns "auth_token"
/auth/token/logout/            POST  log out (djoser, needs token)
/api-token-auth/               POST  log in (obtain_auth_token) -> returns "token"
/api/me/                       GET   protected, header:  Authorization: Token <token>
/api/menu/                     GET (public), POST (token)
/api/menu/1/                   GET (public), PUT/PATCH/DELETE (token)
/api/bookings/                 GET, POST (token required)
/api/bookings/1/               GET, PUT, PATCH, DELETE (token required)
/admin/                        Django admin

SETUP
-----
1. Create the MySQL database:
     mysql -u root -p -e "CREATE DATABASE littlelemon CHARACTER SET utf8mb4;"
2. Virtual environment and packages:
     python -m venv venv
     venv\Scripts\activate        (Windows)   |   source venv/bin/activate   (macOS/Linux)
     pip install -r requirements.txt
3. Set DB credentials (defaults: user root, password root, host 127.0.0.1, port 3306):
     PowerShell:   $env:DB_PASSWORD="your_password"
     macOS/Linux:  export DB_PASSWORD=your_password
   (or edit the DATABASES section in littlelemon/settings.py)
4. python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
5. Unit tests (restaurant/tests/test_models.py and test_views.py):
     python manage.py test

TESTING WITH INSOMNIA / BROWSABLE API
-------------------------------------
1. POST /auth/users/  {"username":"peer","email":"peer@example.com","password":"StrongPass!234"}
2. POST /auth/token/login/  {"username":"peer","password":"StrongPass!234"}  -> copy "auth_token"
3. Add header  Authorization: Token <auth_token>  for protected requests
4. POST /api/menu/      {"title":"Greek Salad","price":"12.50","inventory":20}
5. POST /api/bookings/  {"first_name":"Sam","reservation_date":"2026-12-01","reservation_slot":19}
6. GET /api/menu/ and GET /api/bookings/ also work in a browser (browsable API).
Importable collection: insomnia_collection.json
