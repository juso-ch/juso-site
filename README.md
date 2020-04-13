# juso-site

## Docker

```
docker-compose build
docker-compose up
```

Installation

```
virtualenv env --python=python3

pip install -r requirements.txt

cp local_settings.py.example juso/local_settings.py

npm install

npx gulp build

python manage.py migrate

# Load a fixture with some example entries
python manage.py loaddata example

python manage.py runserver

```

Add dns entries for juso.local and example.juso.local that point to your localhost.
Visit juso.local:8000, example.juso.local, visit juso.local:8000/admin/ to see the admin interface. Log in as superuser with admin:admin or as regular user with user:user.

## Useful resources

* [Django Doc](https://docs.djangoproject.com/en/3.0/)
* [Django Templating Language](https://docs.djangoproject.com/en/3.0/ref/templates/language/)
* [FeinCMS](https://feincms3.readthedocs.io/en/latest/)
