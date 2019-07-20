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

- OS: Ubuntu 18.10 / 19.04

- Coding tool: Visual Studio Code

- Python version (virtual environment): 3.6.7 / 3.7.3



***

### Tips before first running

Tips 1: Install Python virtual environment:

```
$ python3 -m venv venv
```

Activate virtual environment:

```
$ source venv/bin/activate` or `$ . venv/bin/activate
```

Deactivate virtual environment:

```
$ deactivate
```


Tips 2: Install pip (For virtual environment):

```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # Download installation script.
$ sudo python get-pip.py    # Run script.

```


Tips 3: Install Python Prerequisite Packages: 

```
$ pip install flask
$ pip install sqlalchemy
$ pip install flask_uploads
$ pip install markdown
$ pip install pyexcel_xlsx
```