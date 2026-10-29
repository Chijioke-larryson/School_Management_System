<<<<<<< HEAD
# School_Management_System
This is just a simple Django project
=======
# Greenfield School Management System

A small Django school management system built with Django templates, SQLite, plain CSS, and Django authentication.

## Setup

```bash
cd /Users/jioke/Desktop/lesson
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Django
python manage.py migrate
python manage.py check
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Useful Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

Use `python`, not `python manage.py runserever`; the correct command is `runserver`.

## Project Structure

- `school_project/`: project settings and root URLs.
- `accounts/`: authentication, profiles, roles, dashboards, and role checks.
- `academics/`: classes, subjects, and teaching assignments.
- `students/`: student CRUD, search, login creation, and student portal.
- `teachers/`: teacher CRUD, login creation, and assignment management.
- `attendance/`: teacher attendance marking and attendance history.
- `results/`: score entry, grading, student results, and admin reports.
- `templates/`: shared layout and error templates.
- `static/css/`: shared plain stylesheet.

## Roles

- **Admin:** manage school records and view reports.
- **Teacher:** view assigned classes, mark attendance, and enter results for assigned subjects.
- **Student:** view only their own profile, attendance, and results.

The development sample accounts are:

```text
Admin:   phase2admin / Phase2Admin123!
Teacher: phase2teacher / Phase2Teacher123!
Student: phase2student / Phase2Student123!
```

Change these passwords before real use.

## Main URLs

- `/login/`
- `/dashboard/`
- `/academics/classes/`
- `/students/`
- `/teachers/`
- `/attendance/`
- `/results/`
- `/results/reports/classes/`
- `/admin/`

## Testing

Run the full automated suite with:

```bash
python manage.py test
```

The tests cover result totals and grades, score validation, login protection, role access, and student portal ownership.

## Request Flow

A browser sends an HTTP request to a project URL. The project URLconf includes the relevant app URLconf. A function-based view validates the request, reads or changes database records, and returns a template response or a redirect. Successful forms use POST, then redirect, then GET.
>>>>>>> b96e928 (This is my second New Horizon Project)
