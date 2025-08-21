🏋️‍♂️ Fitness Tracker API

This is a Django REST API for managing a fitness tracker platform, allowing users to register, log in, and interact with training plans and other features. The project is deployed on Heroku.

🚀 Live URL: https://fitness-tracker-api-app-dc05722a0570.herokuapp.com/

📁 Project Structure
fitness_tracker/
├── core/                     # Main app (users, models, views)
├── fitness_tracker/         # Project settings and routing
├── requirements.txt         # Python dependencies
├── Procfile                 # For Heroku deployment
├── manage.py
└── README.md

🔧 Features

✅ JWT-based Authentication (via djangorestframework-simplejwt)

✅ Custom User Model

✅ API Health Check at /

✅ Training Plan model support

✅ Secure deployment with SECRET_KEY and Heroku config vars

✅ Production-ready settings:

DEBUG = False

ALLOWED_HOSTS set for Heroku

WhiteNoise for static file handling

SECURE_SSL_REDIRECT and security headers

⚙️ Installation & Development Setup
git clone https://github.com/your-username/fitness_tracker.git
cd fitness_tracker
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt

🛠️ Run Locally
python manage.py migrate
python manage.py runserver


Visit http://127.0.0.1:8000/

🚀 Deployment on Heroku

Create a Heroku app:

heroku create fitness-tracker-api-app


Set config vars:

Add DJANGO_SECRET_KEY in the Heroku dashboard under Settings → Config Vars

Add a .python-version (optional but recommended):

3.13


Add a Procfile:

web: gunicorn fitness_tracker.wsgi


Push to Heroku:

git add .
git commit -m "Initial Heroku deployment"
git push heroku main

GET /
Response: { "status": "API is running" }


🔐 Security Settings

DEBUG = False

SECRET_KEY loaded from environment

SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS includes Heroku domain

WhiteNoise for static files

X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF, SECURE_BROWSER_XSS_FILTER enabled

📦 Dependencies (selected)

Django==5.2.4

djangorestframework==3.16.0

djangorestframework_simplejwt==5.5.1

gunicorn==23.0.0

whitenoise==6.9.0

