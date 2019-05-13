#! /usr/bin/python3

import json
import os

import requests
import argparse

parser = argparse.ArgumentParser('scan various endpoints on spring boot')
parser.add_argument('--proxy', help='proxy to use')
parser.add_argument('--endpoint', help='handle specific endpoint')
parser.add_argument('--force', help='re handle existing files')
parser.add_argument('url', help='full url with path')

args = parser.parse_args()

session =requests.Session()

if args.proxy is not None:
    session.proxies = {'http': args.proxy, 'https': args.proxy}


def test(endpoint):

    filename = 'out/{}.json'.format(endpoint)

    if os.path.isfile(filename) and not args.force:
        print('[*] file {} already exists, skip (use --force to override)'.format(filename))
        return
    
    r = session.get('{}/{}'.format(args.url, endpoint))

    if r.status_code == 200:
        print('[+] get endpoint {}'.format(endpoint))
        try :
            json_response = r.json()
            pretty = json.dumps(json_response, indent=4, sort_keys=True)


            with open(filename, 'wt') as output_file:
                output_file.write(pretty)
                print('[*] writed in {}'.format(filename))
        except Exception as e:
            print(e)
            print(r.text)
    else:
        print('[-] bad response for endpoint {} : {}'.format(endpoint, r.status_code))


if args.endpoint is not None:
    test(args.endpoint)
else:
    with open('endpoints.txt', 'rt') as file:
        for line in file:
            line = line.rstrip('\n')
            test(line)

