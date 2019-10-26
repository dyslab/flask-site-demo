### App name: Flask Site Demo &copy;

A learning demostration site for Python Flask framework.

Running Website:

```
$ . venv/bin/activate
$ ./webstart
```

(Note: Use `chmod a+x ./webstart` to ignite the shell file to be executable.)

Then, ckeck out http://127.0.0.1:5000/ in browser.



### Development & Tested OS information:

- OS: Ubuntu 18.10 / 19.04 / 19.10

- Coding tool: Visual Studio Code

- Python version (virtual environment): 3.6.7 or above.



***



### Tips before first running


**1. Install Python virtual environment:**

```
$ python3 -m venv venv
```

Activate virtual environment:

```
$ source venv/bin/activate
```
or 
```
$ . venv/bin/activate
```

Deactivate virtual environment:

```
$ deactivate
```


**2. Install pip (For virtual environment):**

```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # Download installation script.
$ sudo python get-pip.py    # Run script.

```


**3. Install Python Prerequisite Packages:** 

```
$ pip install flask
$ pip install sqlalchemy
$ pip install flask_uploads
$ pip install markdown
$ pip install pyexcel_xlsx
$ pip install bumpversion       // Optional
```


Note: 

- *bumpversion* used for development, The CLI **`$ bumpversion patch`** will upgrade patch version and commit automatically.

- Output package list to a txt file: **`$ pip list -l --format=freeze > installed_packages.txt`**



***



Packages list: See [installed_packages.txt](installed_packages.txt)

Document information:

- *Last Modified on 26 October 2019*

- *Created on 28 February 2019*
