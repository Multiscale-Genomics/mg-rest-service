"""
.. Copyright 2016 EMBL-European Bioinformatics Institute

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
from flask import Flask, make_response, request
from flask_restful import Api, Resource
from flask_apscheduler import APScheduler

from dmp import rest

import logging
logging.basicConfig()

class Config(object):
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


app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


class GetEndPoints(Resource):
    """
    Class to handle the http requests for returning information about the end
    points
    """
    
    def get(self):
        cnf_loc=os.path.dirname(os.path.abspath(__file__)) + '/mongodb.cnf'
        r = rest(cnf_loc)
        services = r.get_up_services()
        
        links = {'_self' : request.url_root + 'api'}
        for service in services:
            links['_' + service['name']] = service['url']
        return {
            '_links': links
        }


class ping(Resource):
    """
    Class to handle the http requests to ping a service
    """
    
    def get(self):
        import release
        res = {
            "status":  "ready",
            "version": release.__version__,
            "author":  release.__author__,
            "license": release.__license__,
            "name":    release.__rest_name__,
            "description": release.__description__
        }
        return res

"""
Define the URIs and their matching methods
"""
api = Api(app)

#   List the available end points for this service
api.add_resource(GetEndPoints, "/api", endpoint='service-root')

#   Service ping
api.add_resource(ping, "/api/ping", endpoint='service-ping')


"""
Initialise the server
"""
if __name__ == "__main__":
    app.run(port=5002, debug=True, use_reloader=False)
