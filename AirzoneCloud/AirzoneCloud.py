#!/usr/bin/python3

import logging
import requests
import urllib
import urllib.parse
import json

from .contants import (
    BASE_URL,
    API_LOGIN,
    API_DEVICE_RELATIONS,
    API_SYSTEMS,
    API_ZONES,
    API_EVENTS,
    BASIC_REQUEST_HEADERS,
    XHR_REQUEST_HEADERS,
)
from .Device import Device

_LOGGER = logging.getLogger(__name__)


class AirzoneCloud:
    """Allow to connect to AirzoneCloud API"""

    _token = None
    _devices = []

    def __init__(self, username, password):
        """Initialize API connection"""
        self._session = requests.Session()
        self._username = username
        self._password = password
        # login
        self._login(username, password)
        # load devices
        self._load_devices()

    #
    # getters
    #

    @property
    def devices(self):
        """Get devices list (same order as in app)"""
        return self._devices

    @property
    def all_zones(self):
        """Get all zones from all devices (same order as in app)"""
        result = []
        for device in self.devices:
            for system in device.systems:
                for zone in system.zones:
                    result.append(zone)
        return result

    #
    # private
    #

    def _login(self, username, password):
        """Login to AirzoneCloud and return token"""

        try:
            url = "{}{}".format(BASE_URL, API_LOGIN)
            login_payload = {"email": username, "password": password}
            response = self._session.post(
                url, headers=BASIC_REQUEST_HEADERS, json=login_payload
            ).json()
            print(response)
            self._token = response.get("user").get("authentication_token")
        except (RuntimeError, AttributeError):
            raise Exception("Unable to login to AirzoneCloud") from None

        _LOGGER.info("Login success as {}".format(self._username))

        return self._token

    def _load_devices(self):
        """Load all devices"""
        self._devices = []
        try:
            for device_relation in self._get_device_relations():
                device = device_relation.get("device")
                self.devices.append(Device(self, device))
        except RuntimeError:
            raise Exception("Unable to load devices from AirzoneCloud")

        return self._devices

    def _get_device_relations(self):
        """Get devices"""
        _LOGGER.debug("get_device_relations()")
        return self._get(API_DEVICE_RELATIONS).get("device_relations")

    def _get_systems(self, device_id):
        """Get systems"""
        _LOGGER.debug("get_systems(device_id={})".format(device_id))
        return self._get(API_SYSTEMS, {"device_id": device_id}).get("systems")

    def _get_zones(self, system_id):
        """Get Zones."""
        _LOGGER.debug("get_zones(system_id={})".format(system_id))
        return self._get(API_ZONES, {"system_id": system_id}).get("zones")

    def _send_event(self, payload):
        _LOGGER.info("Send event with payload: {}".format(json.dumps(payload)))
        try:
            result = self._post(API_EVENTS, payload)
            return result  # XXX manage error ?
        except RuntimeError:
            _LOGGER.error("Unable to send event to AirzoneCloud")
            return None

    def _get(self, api_endpoint, params={}):
        """Do a http GET request on an api endpoint"""
        params["format"] = "json"
        params["user_email"] = self._username
        params["user_token"] = self._token
        url = "{}{}/?{}".format(BASE_URL, api_endpoint, urllib.parse.urlencode(params))
        return self._session.get(url, headers=BASIC_REQUEST_HEADERS).json()

    def _post(self, api_endpoint, payload={}):
        """Do a http POST request on an api endpoint"""
        uri_params = {
            "user_email": self._username,
            "user_token": self._token,
        }
        url = "{}{}/?{}".format(
            BASE_URL, api_endpoint, urllib.parse.urlencode(uri_params)
        )
        return self._session.post(url, headers=XHR_REQUEST_HEADERS, json=payload).json()
