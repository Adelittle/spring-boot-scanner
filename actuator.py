#! /usr/bin/python3

import json
import requests
import argparse

parser = argparse.ArgumentParser('scan various endpoints on spring boot')
parser.add_argument('url', help='full url with path')

args = parser.parse_args()

with open('endpoints.txt', 'rt') as file:
    endpoints = file.readlines()


def test(endpoint_):
    r = requests.get('{}/{}'.format(args.url, endpoint_))
    json_response = r.json()

    if r.status_code == 200:
        pretty = json.dumps(json_response, indent=4, sort_keys=True)

        with open('out/{}.json'.format(endpoint_), 'wt') as output_file:
            output_file.write(pretty)


for endpoint in endpoints:
    test(endpoint)
