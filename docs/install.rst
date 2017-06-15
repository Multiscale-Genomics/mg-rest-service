Requirements and Installation
=============================

Requirements
------------

Software
^^^^^^^^
- Mongo DB 3.2
- Python 2.7.10+
- pyenv
- pyenv virtualenv
- pip


Python Modules
^^^^^^^^^^^^^^
- DMP
- Flask
- Flask-Restful
- Flask_APScheduler
- Waitress


Installation
------------
Basics
^^^^^^
Directly from GitHub:

.. code-block:: none
   :linenos:

   git clone https://github.com/Multiscale-Genomics/mg-rest-service.git
   cd mg-rest-service/
   pip install -e .

Using pip:

.. code-block:: none
   :linenos:

   pip install git+https://github.com/Multiscale-Genomics/mg-rest-service.git


Setting up a server
^^^^^^^^^^^^^^^^^^^
.. code-block:: none
   :linenos:
   
   git clone https://github.com/Multiscale-Genomics/mg-rest-dm.git

   cd mg-rest-service
   pyenv virtualenv 2.7.12 mg-rest-service
   pyenv activate mg-rest-service
   pip install git+https://github.com/Multiscale-Genomics/mg-dm-api.git
   pip install -e .
   pyenv deactivate

Requires a file with the name `mongodb.cnf` with the following parameters to
define the MongoDB server:

.. code-block:: none
   :linenos:

   [rest]
   host = localhost
   port = 27017
   user = mongo_user
   pass = mongo_user_pwd
   db = rest


Adding Services
^^^^^^^^^^^^^^^
For each REST service that is to be integrated into the MuG REST service should have the relevant URL and name stored within a registry.json file located in the mg-rest-service directory:

.. code-block:: none
   :linenos:

   {"registry" : [
      {"name" : "DMP", "url" : "http://127.0.0.1:5001/api/dmp/ping"},
      {"name" : "", "url" : ""}
   ]}

Starting the service
^^^^^^^^^^^^^^^^^^^^

.. code-block:: none
   :linenos:

   nohup ${PATH_2_PYENV}/versions/2.7.12/envs/mg-rest-service/bin/waitress-serve --listen=127.0.0.1:5000 rest.app:app &


Apache Config
^^^^^^^^^^^^^
This is dependent on the version that you are running.

In Apache 2.2 the `<Location>` tag for the `/api` server need to come last in the list of services so that it is not over written

.. code-block:: none
   :linenos:

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
