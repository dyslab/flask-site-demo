## flask-site-demo: A website demo powered by Python Flask framework.

[![Powered by Flask v2](./assets/powered-by-Flask-v2.svg)](https://flask.palletsprojects.com/) [![Github license](./assets/license-MIT.svg)](https://github.com/dyslab/flask-site-demo/blob/master/LICENSE) [![Demo version](./assets/demo-version.svg)](https://github.com/dyslab/flask-site-demo)

### OS and tools information

- OS: Ubuntu v18.10 / v19.04 / v19.10, Deepin v20.9

- Python version (virtual environment): v3.6.7 or above.

- Framework: Flask v2.3 / Werkzeug v0.16

- SQL toolkit: SQLAlchemy v1.3

- Coding tool: Visual Studio Code

***

### Tips before first try

Install Python virtual environment (venv mode)

```bash
python3 -m venv venv
```

Activate venv mode

```bash
source venv/bin/activate
# or 
. venv/bin/activate
```

Deactivate venv mode

```bash
deactivate
```

Update or install pip (in venv mode)

```bash
pip install pip -U
# or curl it by yourself
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # Download installation script.
sudo python get-pip.py    # Run script.
```

Install required packages 

```bash
pip install -r requirements.txt
```

Start web server

```bash
source venv/bin/activate
./webstart  # Note: type `chmod a+x ./webstart` to ignite the shell file to be executable if it does'n work

# Then, ckeck out link: http://127.0.0.1:5000/ on browser.
```

### Additional notes 

- All reqired packages list see [requirements.txt](requirements.txt)

- Export all required packages list with restrict version to requirements.txt by the command line below.

```bash
pip freeze > requirements.txt
```

---

*· Last Modified on 27 November 2019*

*· Created on 28 February 2019*
