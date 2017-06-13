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

from urllib2 import Request, urlopen, URLError
import json
import os

from dmp import rest

def ping(key, registry_key):
    """
    Ping the defined end points to determine if they are valid services. The
    results are then logged and used by the DMP and other service when listing
    what end points are available. This allows for services to drop out and not
    have nodes pointing to those services until they come back.

    Parameters
    ----------
    key : str
        key for the registry dict
    registry_key : dict
        'a' is the registry key
    """
    cnf_loc = os.path.dirname(os.path.abspath(__file__)) + '/mongodb.cnf'
    dmp_api = rest(cnf_loc)

    for service in registry_key[str(key)]:
        req = Request(service["url"])
        status = "down"
        log = ""
        data = {}
        try:
            response = urlopen(req)
            log = response.code
            data = json.loads(response.read())
            response.close()
        except URLError, err:
            log = err

        if log == 200:
            status = "up"

        if dmp_api.is_service(service["name"]) is True:
            service_found = dmp_api.get_service(service["name"])
            dmp_api.set_service_status(service["name"], status)
            if service_found["url"] + "/ping" != service["url"]:
                dmp_api.update_service_url(service["name"], service["url"])
        else:
            description = data["description"] if data.has_key("description") else ""
            dmp_api.add_service(service["name"], service["url"], description, status)
