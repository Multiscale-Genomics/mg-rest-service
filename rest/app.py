"""
.. Copyright 2017 EMBL-European Bioinformatics Institute

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
import logging
from flask import Flask, request #, make_response
from flask_restful import Api, Resource
from flask_apscheduler import APScheduler

from dmp import rest

logging.basicConfig()

class Config(object):
    """
    Class to handle the spinning off of a separate thread for pinging other
    servers to test if they are alive.
    """
    import json

    with open(os.path.dirname(os.path.abspath(__file__)) + '/registry.json') as data_file:
        data = json.load(data_file)

    JOBS = [
        {
            'id': 'ping',
            'func': 'rest.jobs:ping',
            'args' : ("registry", data),
            'trigger': 'interval',
            'seconds': 60
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True


APP = Flask(__name__)
APP.config.from_object(Config())

SCHEDULER = APScheduler()
SCHEDULER.init_app(APP)
SCHEDULER.start()


class EndPoints(Resource):
    """
    Class to handle the http requests for returning information about the end
    points
    """

    def get(self):
        """
        GET list all end points
        
        List of all of the end points for the current service.

        Example
        -------
        .. code-block:: none
           :linenos:

           curl -X GET http://localhost:5001/mug/api

        """
        cnf_loc = os.path.dirname(os.path.abspath(__file__)) + '/mongodb.cnf'
        if os.path.isfile(cnf_loc) == True:
            dmp_api = rest(cnf_loc)
        else:
            dmp_api = rest(cnf_loc, test=True)
        services = dmp_api.get_up_services()

        links = {'_self' : request.base_url}
        for service in services:
            links['_' + service['name']] = service['url']
        return {
            '_links': links
        }


class Ping(Resource):
    """
    Class to handle the http requests to ping a service
    """

    def get(self):
        """
        GET Status

        List the current status of the service along with the relevant
        information about the version.

        Example
        -------
        .. code-block:: none
           :linenos:

           curl -X GET http://localhost:5001/mug/api/ping


        """
        from . import release
        res = {
            "status":  "ready",
            "version": release.__version__,
            "author":  release.__author__,
            "license": release.__license__,
            "name":    release.__rest_name__,
            "description": release.__description__,
            "_links" : {
                '_self' : request.url_root + 'mug/api/ping',
                '_parent' : request.url_root + 'mug/api'
            }
        }
        return res

# Define the URIs and their matching methods
REST_API = Api(APP)

#   List the available end points for this service
REST_API.add_resource(EndPoints, "/mug/api", endpoint='service-root')

#   Service ping
REST_API.add_resource(Ping, "/mug/api/ping", endpoint='service-ping')


# Initialise the server
if __name__ == "__main__":
    APP.run(port=5000, debug=True, use_reloader=False)
