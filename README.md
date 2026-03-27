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

## Self-hosted RHEL9 runner

The repository now includes a dedicated workflow for a self-hosted runner labeled `rhel9-dev`:

`.github/workflows/rhel9-dev-deploy.yml`

That workflow is now chained behind the standard CI workflow:

1. The localhost-style CI workflow in `.github/workflows/ci.yml` runs first on GitHub-hosted runners.
2. Only if that CI workflow succeeds for a `push`, the deployment workflow reaches the `rhel9-dev` environment approval gate.
3. After you approve `rhel9-dev`, the self-hosted workflow runs its RHEL9 validation and Gunicorn smoke test.

Inside the RHEL9 deployment workflow, it then does two things:

1. Runs migrations, collects static files, and executes the full Django test suite with coverage on the `rhel9-dev` runner.
2. Repeats the checks on the same runner, starts Gunicorn, and smoke-tests both the home page and the static CSS endpoint.

Every job in `.github/workflows/rhel9-dev-deploy.yml` is attached to the `rhel9-dev` environment, so your environment protection rules apply across the entire deployment-validation pipeline.

The workflows are currently configured for Python `3.12` and `3.13`.

The workflow assumes:

1. Your self-hosted runner has the label `rhel9-dev`.
2. You created a GitHub Environment named `rhel9-dev`.
3. The runner can execute `bash`, `curl`, and Python virtual environments.

This is a deployment validation workflow, not a permanent process manager. If you want the app to stay running on RHEL9 after the workflow finishes, the next step is to run Gunicorn under `systemd`, `supervisord`, or a container service.

## Run tests with coverage

`coverage run --rcfile=.coveragerc manage.py test`

`coverage report`
