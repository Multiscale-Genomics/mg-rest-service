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
import pytest
import tempfile
import json

from context import app

@pytest.fixture
def client(request):
    db_fd, app.APP.config['DATABASE'] = tempfile.mkstemp()
    app.APP.config['TESTING'] = True
    client = app.APP.test_client()
    
    def teardown():
        os.close(db_fd)
        os.unlink(app.APP.config['DATABASE'])
    request.addfinalizer(teardown)

    return client

def test_endpoints(client):
    rv = client.get('/mug/api')
    details = json.loads(rv.data)
    #print(details)
    assert '_links' in details

def test_ping(client):
    rv = client.get('/mug/api/ping')
    details = json.loads(rv.data)
    #print(details)
    assert 'status' in details
