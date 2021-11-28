#!/usr/bin/python3

import logging, json
from AirzoneCloud import AirzoneCloud

config = json.load(open("config_test.json"))

logging.basicConfig(level=config.get("log_level", "INFO"))
api = AirzoneCloud(config.get("email"), config.get("password"))

if config.get("display_api_token", False):
    print("API token = ", api._token, "\n")

print()

for installation in api.installations:
    print(installation.str_verbose)
    for group in installation.groups:
        print("   " + group.str_verbose)
        for device in group.devices:
            print("     " + device.str_verbose)
            if config.get("display_device_properties", False):
                for key, val in device.all_properties.items():
                    print("       - {} = {}".format(key, val))
