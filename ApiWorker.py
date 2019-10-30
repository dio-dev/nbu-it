import json
import http.client
import pprint
import urllib.parse
import base64

# API Settigs
HOST = 'dio-tech.top'  # e.g.: my.prom.ua, my.tiu.ru, my.satu.kz, my.deal.by, my.prom.md


class HTTPError(Exception):
    pass


class NbuClient(object):

    def __init__(self, password, login):
        self.login = login
        self.password = password
        self.cred = f"{self.login}:{self.password}"

    def make_request(self, method, url, body=None):
        connection = http.client.HTTPConnection(HOST, port=5000)

        headers = {'Authorization': u'Basic %s' % base64.b64encode(self.cred.encode("utf-8")).decode(),
                   'Content-type': 'application/json'}

        print(url)
        if body:
            body = json.dumps(body)
        connection.request(method, url, body=body, headers=headers)
        response = connection.getresponse()
        if response.status != 200:
            raise HTTPError('{}: {}'.format(response.status, response.reason))

        response_data = response.read()
        return json.loads(response_data.decode())

    def get_nearbry_objects(self, place_type, place_name, lat, lng):
        url = f'/dist?type={place_type}&name={urllib.parse.quote(str(place_name))}&lat={lat}&lng={lng}'

        method = 'GET'

        return self.make_request(method, url)

    def get_address_details(self, adress_id):
        url = f'/get_adress_detail?adress_id={adress_id}'

        method = 'GET'

        return self.make_request(method, url)
