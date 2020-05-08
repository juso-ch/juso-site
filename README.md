# juso-site

## Docker

```
docker-compose build
docker-compose up
```

### Deployment
Copy `.env.dev` to `.env.prod` and change the passwords.

Build images and run them
```
docker-compose -f docker-compose.prod.yml up --build -d
```

Run database migrations
```
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

Collect static files
```
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```
On first run only, create a superuser and a default site.
```
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
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
