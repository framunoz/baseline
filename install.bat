py -m pip install --upgrade pip
py -m pip install --user virtualenv
py -m venv venv
.\venv\Scripts\activate
py setup.py sdist
cd dist
pip install despliegue-0.1.0.tar.gz
py main.py