Coderr Backend<br><br>

The Coderr backend is a robust REST API built with Django and Django REST Framework (DRF). It supports functionalities such as user authentication, password reset, profile management, and review systems for business users.<br><br>

Features<br>
- <b>User Authentication:</b><br>
  - Login and registration with JWT-based authentication.<br>
  - Password reset via email with secure token validation.<br>
- <b>Profile Management:</b><br>
  - View and edit user profiles (business and customer).<br>
  - Separate endpoints for business and customer profiles.<br>
- <b>Review System:</b><br>
  - Create, view, update, and delete reviews for business profiles.<br>
- <b>Offer Management:</b><br>
  - Manage business offers (create, view, update).<br><br>

---

Installation<br><br>

Prerequisites<br>
- Python 3.10+<br>
- pip<br>
- WSL 20.04 (for Windows users)<br>
- PostgreSQL<br><br>

Steps<br>
1. <b>Clone the repository:</b><br>
   <code>git clone git@github.com:LukasNolting/coderr-backend.git</code><br>
   <code>cd coderr-backend</code><br><br>

2. <b>Create a virtual environment:</b><br>
   <code>python -m venv env</code><br>
   <code>source env/bin/activate</code>  # Linux/Mac<br>
   <code>env\\Scripts\\activate</code>  # Windows<br><br>

3. <b>Install dependencies:</b><br>
   <code>pip install -r requirements.txt</code><br><br>

4. <b>Set up PostgreSQL database:</b><br>
   - Launch WSL or your terminal and start PostgreSQL:<br>
     <code>sudo service postgresql start</code><br>
   - Access the PostgreSQL CLI:<br>
     <code>sudo -u postgres psql</code><br>
   - Create a new database:<br>
     <code>CREATE DATABASE coderr;</code><br>
   - Create a new user:<br>
     <code>CREATE USER coderr_user WITH PASSWORD 'your_password';</code><br>
   - Grant privileges:<br>
     <code>GRANT ALL PRIVILEGES ON DATABASE coderr TO coderr_user;</code><br>
   - Exit the PostgreSQL CLI:<br>
     <code>\\q</code><br><br>

5. <b>Configure .env file:</b><br>
   - Copy <code>dot_env_template</code> to <code>.env</code>.<br>
   - Update the database section:<br>
     <code>
       DATABASE_NAME='coderr'<br>
       DATABASE_USER='coderr_user'<br>
       DATABASE_PASSWORD='your_password'<br>
       DATABASE_HOST='localhost'<br>
       DATABASE_PORT=5432<br>
     </code><br><br>

6. <b>Apply migrations:</b><br>
   <code>python manage.py makemigrations</code><br>
   <code>python manage.py migrate</code><br><br>

7. <b>Gunicorn Setup</b><br><br>

In addition to installing the required dependencies from <code>requirements.txt</code>, you need to install Gunicorn separately for deployment:<br><br>

7.1. Install Gunicorn via pip:<br>
   <code>pip install gunicorn</code><br><br>

7.2. Test running the server with Gunicorn:<br>
   <code>gunicorn --bind 0.0.0.0:8000 coderr_backend.wsgi:application</code><br><br>

7.3. Configure Gunicorn as a system service for production (optional):<br>
   - Create a Gunicorn service file, e.g., <code>/etc/systemd/system/coderr_gunicorn.service</code>, with the following content:<br>
   <pre>
   [Unit]
   Description=Gunicorn instance for Coderr Backend
   After=network.target

   [Service]
   User=your_user
   Group=your_group
   WorkingDirectory=/path/to/coderr-backend
   ExecStart=/path/to/env/bin/gunicorn --workers 3 --bind unix:/path/to/coderr-backend/coderr.sock coderr_backend.wsgi:application

   [Install]
   WantedBy=multi-user.target
   </pre><br>

7.4. Start and enable the Gunicorn service:<br>
   <code>sudo systemctl start coderr_gunicorn</code><br>
   <code>sudo systemctl enable coderr_gunicorn</code><br><br>

This ensures Gunicorn is set up properly for production environments.
"""

8. <b>Start the development server:</b><br>
   <code>python manage.py runserver</code><br><br>

---

<b>Guest Access</b><br><br>

Two guest access accounts have been pre-configured for testing purposes:<br><br>

<pre>
const GUEST_LOGINS = {
  customer: {
    username: "andrey",
    password: "asdasd",
  },
  business: {
    username: "kevin",
    password: "asdasd",
  },
};
</pre><br>

You can use these accounts to log in and test the application with pre-defined roles: Customer and Business.
"""

API Endpoints<br><br>

<b>Authentication</b><br>
- <code>POST /login/</code>: Authenticate users and return a token.<br>
- <code>POST /registration/</code>: Register new users.<br><br>

<b>Profile Management</b><br>
- <code>GET /profile/&lt;pk&gt;/</code>: Retrieve or update a user profile.<br>
- <code>GET /profiles/business/</code>: List all business profiles.<br>
- <code>GET /profiles/customer/</code>: List all customer profiles.<br><br>

<b>Reviews</b><br>
- <code>GET /reviews/</code>: List reviews with optional filters.<br>
- <code>POST /reviews/</code>: Create a new review (requires authentication).<br>
- <code>GET /reviews/&lt;id&gt;/</code>: Retrieve, update, or delete a specific review.<br><br>

Environment Variables<br><br>

Create a .env file or use the template <code>dot_env_template</code> with the following settings:<br>
<pre>
REDIRECT_LOGIN='http://127.0.0.1:54051/login.html'
REDIRECT_LANDING='http://127.0.0.1:54051'
BACKEND_URL='localhost:8000'
PROD_FRONTEND_URL=''

SECRET_KEY=''
ALLOWED_HOSTS=["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS=["http://127.0.0.1","http://localhost:4200","http://localhost:8000"]
CORS_ALLOWED_ORIGINS=["http://127.0.0.1","http://localhost:4200","http://localhost:8000"]

DATABASE_NAME='coderr'
DATABASE_USER='postgres'
DATABASE_PASSWORD=''
DATABASE_HOST=''
DATABASE_PORT=5432

EMAIL_HOST=''
EMAIL_PORT=587
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
DEFAULT_FROM_EMAIL=''
DOMAIN_NAME='localhost'
</pre><br>

---

Deployment<br><br>

1. Set <code>DEBUG=False</code> in .env.<br>
2. Collect static files:<br>
   <code>python manage.py collectstatic</code><br>
3. Configure a WSGI server (e.g., Gunicorn or uWSGI) to serve the application.<br>
4. Use a reverse proxy (e.g., Nginx) for improved performance.<br><br>

---

Contribution<br><br>

1. Fork the repository.<br>
2. Create a new feature branch:<br>
   <code>git checkout -b feature-name</code><br>
3. Commit your changes:<br>
   <code>git commit -m "Add feature description"</code><br>
4. Push to the branch:<br>
   <code>git push origin feature-name</code><br>
5. Open a pull request.<br><br>

---

License<br><br>

This project is licensed under the MIT License.<br>
"""


