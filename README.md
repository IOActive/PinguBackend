# Basic configuration

You will need to create a .env to store your secrets. Eg,:

```
SECRET_KEY="XXXXXX"
```

# Install requeriments

# Run server
```
python manage.py makemigrations
python manage.py migrate --settings=PinguBackend.settings.development
python manage.py runserver 0.0.0.0:8080 --settings=PinguBackend.settings.development
```
