
Coderr Backend

The Coderr backend is a robust REST API built with Django and Django REST Framework (DRF). It supports functionalities such as user authentication, password reset, profile management, and review systems for business users.

Features

- User Authentication:
  - Login and registration with JWT-based authentication.
  - Password reset via email with secure token validation.
- Profile Management:
  - View and edit user profiles (business and customer).
  - Separate endpoints for business and customer profiles.
- Review System:
  - Create, view, update, and delete reviews for business profiles.
- Offer Management:
  - Manage business offers (create, view, update).

Installation

1. Clone the repository:
   git clone git@github.com:LukasNolting/coderr-backend.git
   cd coderr-backend

2. Create a virtual environment:
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Apply migrations:
   python manage.py makemigrations
   python manage.py migrate

5. Start the development server:
   python manage.py runserver

API Endpoints

Authentication
- POST /login/: Authenticate users and return a token.
- POST /registration/: Register new users.

Profile Management
- GET /profile/<pk>/: Retrieve or update a user profile.
- GET /profiles/business/: List all business profiles.
- GET /profiles/customer/: List all customer profiles.

Reviews
- GET /reviews/: List reviews with optional filters.
- POST /reviews/: Create a new review (requires authentication).
- GET /reviews/<id>/: Retrieve, update, or delete a specific review.

Environment Variables

Create a .env file with the following settings:

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

Deployment

1. Set DEBUG=False in .env.
2. Collect static files:
   python manage.py collectstatic
3. Configure a WSGI server (e.g., Gunicorn or uWSGI) to serve the application.
4. Use a reverse proxy (e.g., Nginx) for improved performance.

Contribution

1. Fork the repository.
2. Create a new feature branch:
   git checkout -b feature-name
3. Commit your changes:
   git commit -m "Add feature description"
4. Push to the branch:
   git push origin feature-name
5. Open a pull request.

License

This project is licensed under the MIT License.
