# Backend installation notes

## Requirements

* [python 3.8.5](https://www.python.org/downloads/) and pip
* [MySQL](https://www.mysql.com/downloads/) and connector/python

## Installing python packages
`pip install -r requirements.txt`

## Setting up the database
* `mysql -u root -p < setup.sql`
* `python manage.py migrate`

## Runnig up the server
1. `export ENV=DEV`
1. `python manage.py runserver`
1. [127.0.0.1:8000](127.0.0.1:8000)

or

[https://hacktues.pythonanywhere.com](https://hacktues.pythonanywhere.com)

# content of `choices.bytes`:
```python
{
    "FORMS": [
        ('8�', '8 �'), ('8�', '8 �'), ('8�', '8 �'), ('8�', '8 �'),
        ('9�', '9 �'), ('9�', '9 �'), ('9�', '9 �'), ('9�', '9 �'),
        ('10�', '10 �'), ('10�', '10 �'), ('10�', '10 �'), ('10�', '10 �'),
        ('11�', '11 �'), ('11�', '11 �'), ('11�', '11 �'), ('11�', '11 �'),
        ('12�', '12 �'), ('12�', '12 �'), ('12�', '12 �'), ('12�', '12 �'),
    ],
    "FOOD_PREFERENCES": [
        ('0', 'None'),
        ('Vgtn', 'Vegeterian'),
        ('Vgn', 'Vegan'),
    ],
    "SIZES": [
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
    ]
}
```
