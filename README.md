## flask-site-demo: A website demo powered by Python Flask framework.

[![Powered by Flask v2](./assets/powered-by-Flask-v1.svg)](https://flask.palletsprojects.com/) [![Github license](./assets/license-MIT.svg)](https://github.com/dyslab/flask-site-demo/blob/master/LICENSE) [![Demo version](./assets/demo-version.svg)](https://github.com/dyslab/flask-site-demo)

### OS and tools information

- OS: Ubuntu v18. ~ v19 / Deepin v20 ~ v23 / Windows 11

- Python version (virtual environment): v3.6.7 or above.

- Framework: Flask v1.1.1 ~ v3.1.2

- SQL toolkit: SQLAlchemy v1.3.11

- IDE tool: Visual Studio Code

***

### Tips before first try

1. Install Python virtual environment (venv mode)

```bash
python3 -m venv venv
```

2. Activate venv mode

```bash
source venv/bin/activate
# or 
. venv/bin/activate
# or (on Windows)
venv\Scripts\activate
```

3. Deactivate venv mode

```bash
deactivate
```

4. Update or install latest pip (in venv mode)

```bash
pip install pip -U
# or curl it by yourself
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # Download installation script.
sudo python get-pip.py    # Run script.
```

5. Install required packages 

```bash
pip install -r requirements.txt
```

6. Start web server

```bash
# Acticate Python virtual mode
source venv/bin/activate

# Run web server on any platform (development mode)
flask --app 'fsdemo' run
# NOTE: The argument '--app' is a new feature in Flask v3

# Or run the below script on Linux
# Classical approach to running web service in Flask v1
./webstart  
# Note: type command line `chmod a+x ./webstart` to make the script executable if it does'n work

# Then, ckeck out link: http://127.0.0.1:5000/ on browser.
```

### Additional notes 

- All reqired packages list see [requirements.txt](requirements.txt)

- Export all required packages list with restrict version to requirements.txt by the command line below.

```bash
pip freeze > requirements.txt
```

---

- *Last Modified on 27 October 2025*

- *Created on 28 February 2019*
