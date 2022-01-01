#!/usr/bin/python3

import logging, json
from AirzoneCloud import AirzoneCloud

config = json.load(open("config_test.json"))

logging.basicConfig(level=config.get("log_level", "INFO"))

# Connection
api = AirzoneCloud(config.get("email"), config.get("password"))

print()

# Api token
if config.get("display_api_token", False):
    print("API token = -", api._token, "\n")

# Refresh data
if config.get("refresh_before_display", False):
    print("Refreshing all data:")
    api.refresh_installations()
    for installation in api.installations:
        installation.refresh_groups()
        for group in installation.groups:
            group.refresh_devices()
    print()

# Display
for installation in api.installations:
    print(installation.str_verbose)
    for group in installation.groups:
        print("   {}".format(group.str_verbose))
        if config.get("display_group_properties", False):
            for key, val in group.all_properties.items():
                print("     - {} = {}".format(key, val))

        for device in group.devices:
            print("     " + device.str_verbose)
            if config.get("display_device_properties", False):
                for key, val in device.all_properties.items():
                    print("       - {} = {}".format(key, val))

