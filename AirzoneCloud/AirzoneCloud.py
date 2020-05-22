#!/usr/bin/python3

import logging
import requests
import urllib
import urllib.parse
import json

from .contants import (
    API_LOGIN,
    API_DEVICE_RELATIONS,
    API_SYSTEMS,
    API_ZONES,
    API_EVENTS,
)
from .Device import Device

_LOGGER = logging.getLogger(__name__)


class AirzoneCloud:
    """Allow to connect to AirzoneCloud API"""

    _session = None
    _username = None
    _password = None
    _base_url = "https://www.airzonecloud.com"
    _user_agent = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X; wv) AppleWebKit/537.26 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Safari/537.36"
    _token = None
    _devices = []

    def __init__(
        self, username, password, user_agent=None, base_url=None,
    ):
        """Initialize API connection"""
        self._session = requests.Session()
        self._username = username
        self._password = password
        if user_agent is not None and isinstance(user_agent, str):
            self._user_agent = user_agent
        if base_url is not None and isinstance(base_url, str):
            self._base_url = base_url
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
    def all_systems(self):
        """Get all systems from all devices (same order as in app)"""
        result = []
        for device in self.devices:
            for system in device.systems:
                result.append(system)
        return result

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
    # Refresh
    #

    def refresh_devices(self):
        """Refresh devices"""
        self._load_devices()

    #
    # private
    #

    def _login(self, username, password):
        """Login to AirzoneCloud and return token"""

        try:
            url = "{}{}".format(self._base_url, API_LOGIN)
            login_payload = {"email": username, "password": password}
            headers = {"User-Agent": self._user_agent}
            response = self._session.post(
                url, headers=headers, json=login_payload
            ).json()
            self._token = response.get("user").get("authentication_token")
        except (RuntimeError, AttributeError):
            raise Exception("Unable to login to AirzoneCloud") from None

        _LOGGER.info("Login success as {}".format(self._username))

        return self._token

    def _load_devices(self):
        """Load all devices for this account"""
        current_devices = self._devices
        self._devices = []
        try:
            for device_relation in self._get_device_relations():
                device_data = device = device_relation.get("device")
                device = None
                # search device in current_devices (if where are refreshing devices)
                for current_device in current_devices:
                    if current_device.id == device_data.get("id"):
                        device = current_device
                        device._set_data_refreshed(device_data)
                        break
                # device not found => instance new device
                if device is None:
                    device = Device(self, device_data)
                self._devices.append(device)
        except RuntimeError:
            raise Exception("Unable to load devices from AirzoneCloud")
        return self._devices

    def _get_device_relations(self):
        """Http GET to load devices"""
        _LOGGER.debug("get_device_relations()")
        return self._get(API_DEVICE_RELATIONS).get("device_relations")

    def _get_systems(self, device_id):
        """Http GET to load systems"""
        _LOGGER.debug("get_systems(device_id={})".format(device_id))
        return self._get(API_SYSTEMS, {"device_id": device_id}).get("systems")

    def _get_zones(self, system_id):
        """Http GET to load Zones"""
        _LOGGER.debug("get_zones(system_id={})".format(system_id))
        return self._get(API_ZONES, {"system_id": system_id}).get("zones")

    def _send_event(self, payload):
        """Http POST to send an event"""
        _LOGGER.debug("Send event with payload: {}".format(json.dumps(payload)))
        try:
            result = self._post(API_EVENTS, payload)
            _LOGGER.debug("Result event: {}".format(json.dumps(result)))
            return result
        except RuntimeError:
            _LOGGER.error("Unable to send event to AirzoneCloud")
            return None

    def _get(self, api_endpoint, params={}):
        """Do a http GET request on an api endpoint"""
        params["format"] = "json"
        params["user_email"] = self._username
        params["user_token"] = self._token
        url = "{}{}/?{}".format(
            self._base_url, api_endpoint, urllib.parse.urlencode(params)
        )
        headers = {"User-Agent": self._user_agent}
        return self._session.get(url, headers=headers).json()

    def _post(self, api_endpoint, payload={}):
        """Do a http POST request on an api endpoint"""
        uri_params = {
            "user_email": self._username,
            "user_token": self._token,
        }
        url = "{}{}/?{}".format(
            self._base_url, api_endpoint, urllib.parse.urlencode(uri_params)
        )
        headers = {
            "User-Agent": self._user_agent,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
        }
        return self._session.post(url, headers=headers, json=payload).json()
