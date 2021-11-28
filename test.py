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

            # if device.name == "Salon":
            #     # device.turn_on(auto_refresh=False).set_temperature(20)
            #     device.set_mode("heating")
            #     print(device.str_verbose)
            #     exit(0)

# XXX TODO
# - refreshes AirzoneCloud
# - refreshes Installation
# - refreshes Group
# - set mode from Group
# - reprendre le repo .git
# - virer TODROP.py
# - fichier test.py
# - ajouter config_test.json au .gitignore
# - documentation

#         device.set_mode("cool")
#         device.set_temperature(25)
#         device.turn_off()
#         device.refresh()
#         print(device)


# device = api.all_devices[0]
# print(device)
# device.turn_off()

# set mode to heat
# device.set_mode("cool")
# print(device)

#
# regenerate API doc https://stackoverflow.com/a/59128670
#

# cd Sphinx-docs
# make markdown
# cp _build/markdown/AirzoneCloud.md ../API.md

#
# push new build on pypi
#

# python setup.py sdist
# twine upload dist/AirzoneCloud-0.4.0.tar.gz
