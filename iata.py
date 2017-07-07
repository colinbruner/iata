#!/usr/bin/env python

import sys
import demjson
import requests

def usage():
    print("Ensure config.ini exists and is filled out.")
    print(sys.argv[0] + "<airport code>")
    sys.exit(1)

def main(site, api_key, api_url):
    # Format string
    api_url = api_url + site + "?user_key=" + api_key

    response = requests.get(api_url)

    # Trim unnecessary response information
    unicode_dict = response.text.split('[')[1][:-3]

    try:
        d = demjson.decode(unicode_dict)
        # Gross formating
        print(
"""#########################################
# Airport Code Information listed below #
#########################################
Code = {code}
City = {city}
Airport Name = {name}
Country = {country}
Time Zone = {timezone}
Latitude = {lat}
Longitude = {lng}""").format(code=d['code'],
                             city=d['city'],
                             name=d['name'],
                             country=d['country'],
                             timezone=d['timezone'],
                             lat=d['lat'],
                             lng=d['lng'])

    except Exception as e:
        print("Oh no, something went wrong!")
        print("Error Message: %s" % e)

if __name__ == "__main__":
    import os

    from argparse import ArgumentParser
    from configparser import RawConfigParser

    parser = ArgumentParser(
        description='This utility looks up airport information by an airport\'s IATA code',
    )
    parser.add_argument(
        'site',
        help='Site to lookup, such as "iad" or "cdg"'
    )

    args = parser.parse_args()

    PROJECT_PATH = os.path.join(os.path.dirname(__file__))
    try:
        config = RawConfigParser()
        config_path=PROJECT_PATH + '/config.ini'

        config.read(config_path)

        # Get config from config.ini
        api_key = config.get('iata', 'API_KEY')
        api_url = config.get('iata', 'API_URL')
    except:
        usage()

    main(args.site, api_key, api_url)
