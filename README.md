# Democrance

A test insurance site

### Installing

Follow These Steps...

---
#### Get project
You can clone project by running:
```
git clone https://github.com/seyed1991/democrance.git
```

#### make a virtualenv
To create project virtual environment run:
```
virtualenv venv -p python3
```

#### Install Python Packages
To install python packages run:
```
pip install -r requirements.txt
```

#### Migrate Database

To migrate database and create database tables run:
```
python manage.py migrate
```

#### Create Super User
To create system super user run:

```
python manage.py createsuperuser
```
and provide requested data


#### Testing
To run Django Tests run:
```
python manage.py test
```
---
#### Notes:

- `IsOwnerPermission` is implemented, but was not used for easier test
- More tests can be added e.g. `Authenticaion Tests`, `Access Control`, `Filters`
- For more complicated filters `django-filter` can be used
- If `Castomer` has more data a `Castomer` model can be added to save customers profiles
separated
- If we have lots of users, we can add a `full_name` column to users table to have better
performance in name search
- We can have a `Quote Schema` model to have pre-filled Quotes with details, so that users
can search and choose from them. This table can be filled with `Fixtures`.
- `Payment` process is not implemented.
- using `_` in urls and ending them with `/` is not recommended, but was used for task
fulfillment