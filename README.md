# vacation-memories

A simple Django starter for a dark-mode vacation memories site that can grow into a photo and video gallery over time.

## Quick start

1. Create a virtual environment:
   `python -m venv .venv`
2. Activate it:
   Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Apply migrations:
   `python manage.py migrate`
5. Run the development server:
   `python manage.py runserver`

## Run with Gunicorn

Use Gunicorn for a production-style server process on Linux, macOS, or inside a container:

`gunicorn -c gunicorn.conf.py config.wsgi:application`

On Windows, use `python manage.py runserver` for local development. Gunicorn depends on Unix-only modules and will not run natively on Windows.

## Ubuntu deployment notes

When you switch from `runserver` to Gunicorn, Django stops serving static files for you. If you skip `collectstatic`, the page loads without the CSS and the UI looks unstyled.

Run these commands on Ubuntu from the project root:

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `export DJANGO_DEBUG=False`
5. `export DJANGO_ALLOWED_HOSTS=your-domain-or-server-ip`
6. `python manage.py migrate`
7. `python manage.py collectstatic --noinput`
8. `gunicorn -c gunicorn.conf.py config.wsgi:application`

If you prefer not to use the config file, this equivalent command also works:

`gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3`

## Run tests with coverage

`coverage run --rcfile=.coveragerc manage.py test`

`coverage report`
