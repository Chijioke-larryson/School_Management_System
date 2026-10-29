# Beginner Error Checklist

## `python manage.py runserever` fails

The command is misspelled. Use:

```bash
python manage.py runserver
```

## `TemplateDoesNotExist`

Check that the template is inside the app namespace, for example:

```text
students/templates/students/student_list.html
```

Also confirm the template uses the same path passed to `render()`.

## HTTP 404

Check the route in the app `urls.py`, confirm that app URLconf is included in `school_project/urls.py`, and verify the named URL used by `{% url %}`.

## CSRF verification failed

Every POST form needs:

```django
{% csrf_token %}
```

The form action should also point to the correct named URL.

## `no such table`

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

Confirm the app is listed in `INSTALLED_APPS`.

## Duplicate value error

Admission numbers, staff IDs, class names, subject codes, attendance dates, and results use database uniqueness rules. Choose a new value or edit the existing record.

## Login succeeds but the wrong dashboard appears

Check the user’s `Profile.role`. The accepted values are `admin`, `teacher`, and `student`.

## HTTP 403

The account is authenticated but its role is not allowed for that view. Check the `@role_required(...)` decorator and the user’s profile.

## Blank template value

Compare the context key in the view with the variable in the template. For example, a view passing `students` must use `{% for student in students %}`.

## Test client reports `Invalid HTTP_HOST: testserver`

Use the development host in a focused shell check:

```python
Client(HTTP_HOST="127.0.0.1")
```

## Static CSS is missing

Confirm the template begins with `{% load static %}`, the link uses `{% static 'css/styles.css' %}`, and `STATICFILES_DIRS` includes the project `static/` directory.
