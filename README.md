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

## Run tests with coverage

`coverage run --rcfile=.coveragerc manage.py test`

`coverage report`
