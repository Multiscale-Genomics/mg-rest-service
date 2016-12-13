# mg-rest-service
Service to monitor and list live REST services

# Requirements
- Mongo DB 3.2
- Python 2.7.10+
- pyenv
- pyenv virtualenv
- Python Modules:
  - DMP
  - Flask
  - Flask-Restful
  - Flask_APScheduler
  - Waitress

# Installation
Cloneing from GitHub:
```
git clone https://github.com/Multiscale-Genomics/mg-rest-service.git
```
To get this to be picked up by pip if part of a webserver then:
```
pip install --editable .
```
This should install the required packages listed in the `setup.py` script.


Installation via pip:
```
pip install git+https://github.com/Multiscale-Genomics/mg-rest-service.git
```

# Configuration files
Requires a file with the name `mongodb.cnf` with the following parameters to define the MongoDB server:
```
[rest]
host = localhost
port = 27017
user = mongo_user
pass = mongo_user_pwd
db = rest
```

For each REST service that is to be integrated into the MuG REST service should have the relevant URL and name stored within a registry.json file located in the mg-rest-service directory:
```
{"registry" : [{"name" : "DMP", "url" : "http://127.0.0.1:5001/api/dmp/ping"}, {"name" : "", "url" : ""}]}
```

# Setting up a server
```
git clone https://github.com/Multiscale-Genomics/mg-rest-service.git

cd mg-rest-service
pyenv virtualenv 2.7.12 mg-rest-service
pyenv activate mg-rest-service
pip install git+https://github.com/Multiscale-Genomics/mg-dm-api.git
pip install --editable .
pip deactivate
```
Starting the service:
```
nohup ${PATH_2_PYENV}/versions/2.7.12/envs/mg-rest-service/bin/waitress-serve --listen=127.0.0.1:5000 rest.app:app &
```

# Apache Config
This is dependent on the version that you are running.

## Apache 2.2 Config
In Apache 2.2 the `<Location>` tag for the `/api` server need to come last in the list of services so that it is not over written
```
<VirtualHost *:80>
  ServerName www.example.com
  ServerAlias rest-mug.example.com
  ServerAlias rest-mug
  <Proxy *>
    Order deny,allow
    Allow from all
  </Proxy>
  ProxyRequests Off
  ProxyPreserveHost On
  <Location /api/dmp>
    ProxyPass http://127.0.0.1:5001/api/dmp
    ProxyPassReverse http://127.0.0.1:5001/api/dmp
  </Location>
  <Location /api/adjacency>
    ProxyPass http://127.0.0.1:5002/api/adjacency
    ProxyPassReverse http://127.0.0.1:5002/api/adjacency
  </Location>
  <Location /api>
    ProxyPass http://127.0.0.1:5000/api
    ProxyPassReverse http://127.0.0.1:5000/api
  </Location>
  RequestHeader set X-Forwarded-Proto "http"
</VirtualHost>
```


# RESTful API
## List end points
Request:
```
wget http://127.0.0.1:5000/api
```
Returns:
```
{"_links": {"_self": "http://ves-ebi-64.ebi.ac.uk/api", "DMP" : "http://ves-ebi-64.ebi.ac.uk/api/dmp"}}
```

## ping
Request:
```
wget http://127.0.0.1:5000/api
```
Returns:
```
{"status": "ready", "description": "Main process for checking REST APIs are available", "license": "Apache 2.0", "author": "Mark McDowall", "version": "v0.0", "name": "Service"}
```

