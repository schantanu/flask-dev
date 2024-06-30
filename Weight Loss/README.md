# Flaskapp

### To generate Requirements file
Navigate to project folder and run the following
```shell
pipreqs
```

### Install Virtual Environment and Initiate
```shell
python3 -m venv venv
. venv/bin/activate
```

### Install Packages
```shell
. venv/bin/activate
python3 -m pip install -r requirements.txt
```

### To Initiate SQLite DB
```shell
. venv/bin/activate
python3
```
```python
from application import db
db.create_all()
db.commit()
exit()
```

### To Run App
```shell
. venv/bin/activate
python3 run.py
```


# To Run App
```
. venv/bin/activate
flask setup_db
flask setup_admin anaconda
flask run
```