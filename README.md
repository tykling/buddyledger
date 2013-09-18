Buddyledger
===========
A django system to keep track of the sometimes complicated debt relationships between groups of friends.


Development status
------------------
Buddyledger is in development and is not production ready. The current version runs on https://buddyledger.baconsvin.org with the code in this repository.


Using Buddyledger
-----------------
Buddyledger is often used on an event-by-event basis, where you create a ledger for a specific event (like a vacation). All expenses for that event are entered on the ledger, and after the event is over the ledger is closed and debts are settled by making backpayments.

Buddyledger can also be used as a more "permanent ledger" to keep track of longer running group expenses, where the ledger is never closed, and expenses are added as you go. This way you can simply check Buddyledger before going out for dinner, and use the current debt balance between two (or more) people to decide whose pays this time.

Installation
------------
First, make sure you have Django and NetworkX installed.

Change directory to `<repository_root>/buddyledger/src` (the one containing `manage.py`).

Create `buddyledger/settings.py` relative to current directory (example content):
```
ROOT_URLCONF="buddyledger.urls"
INSTALLED_APPS=(
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'buddyledger'
)

TEMPLATE_DIRS=("templates")

DEBUG = True
DEFAULT_FROM_EMAIL = 'webmaster@example.com'
SECRET_KEY="lol"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'buddydb'
     }
}
```

Now execute (example for Windows):

    c:\Python33\python manage.py syncdb
    c:\Python33\python manage.py getcurrency
    c:\Python33\python manage.py runserver

The web application is available at http://localhost:8000/ .
