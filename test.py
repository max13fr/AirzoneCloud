#!/usr/bin/env python3

import json
import pprint

import AirzoneCloud

config = json.load(open("config.json"))
api = AirzoneCloud.AirzoneCloud(config["email"], config["password"])
