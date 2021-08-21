#!/usr/bin/python3

import json
import logging
import pprint
import requests
import urllib
import urllib.parse

from .contants import (
    API_LOGIN,
    API_INSTALLATIONS,
    API_SYSTEMS,
    API_ZONES,
    API_EVENTS,
)
from .Installation import Installation

_LOGGER = logging.getLogger(__name__)


class AirzoneCloud:
    """Allow to connect to AirzoneCloud API"""

    _session = None
    _username = None
    _password = None
    _base_url = "https://m.airzonecloud.com"
    _user_agent = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X; wv) AppleWebKit/537.26 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Safari/537.36"
    _token = None
    _installations = {}

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
        self._login()
        # load installations
        self._load_installations()

    #
    # getters
    #

    @property
    def installations(self):
        """Get installations list (same order as in app)"""
        return list(self._installations.values())

    @property
    def all_systems(self):
        """Get all systems from all installations (same order as in app)"""
        result = []
        for installation in self.installations:
            for system in installation.systems:
                result.append(system)
        return result

    @property
    def all_zones(self):
        """Get all zones from all installations (same order as in app)"""
        result = []
        for installation in self.installations:
            for system in installation.systems:
                for zone in system.zones:
                    result.append(zone)
        return result

    #
    # Refresh
    #

    def refresh_installations(self):
        """Refresh installations"""
        self._load_installations()

    #
    # private
    #

    def _login(self):
        """Login to AirzoneCloud and return token"""

        try:
            url = "{}{}".format(self._base_url, API_LOGIN)
            login_payload = {"email": self._username, "password": self._password}
            headers = {"User-Agent": self._user_agent}
            response = self._session.post(
                url, headers=headers, json=login_payload
            ).json()
            self._token = response.get("token")
        except (RuntimeError, AttributeError):
            raise Exception("Unable to login to AirzoneCloud") from None

        _LOGGER.info("Login success as {}".format(self._username))

        return self._token

    def _load_installations(self):
        """Load all installations for this account"""
        current_installations = self._installations
        self._installations = {}
        try:
            for installation_data in self._get_installations():
                #pprint.pprint(installation_data)
                installation_id = installation_data.get("installation_id")
                installation = current_installations.get(installation_id)
                # installation not found => instance new installation
                if installation is None:
                    installation = Installation(self, installation_id)
                else:
                    installation.refersh();
                self._installations.append(installation)
        except RuntimeError:
            raise Exception("Unable to load installations from AirzoneCloud")
        return self._installations

    def _get_installations(self):
        """Http GET to load installations"""
        _LOGGER.debug("get_installations()")
        return self._get(API_INSTALLATIONS).get("installations")

    def _get_installation(self, installation_id):
        """Http GET to load installations"""
        _LOGGER.debug("get_installation()")
        return self._get("{}/{}".format(API_INSTALLATIONS, installation_id))

    def _get_systems(self, installation_id):
        """Http GET to load systems"""
        _LOGGER.debug("get_systems(installation_id={})".format(installation_id))
        return self._get(API_SYSTEMS, {"installation_id": installation_id}).get("systems")

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

        return self._request(method="GET", api_endpoint=api_endpoint, params=params)

    def _post(self, api_endpoint, payload={}):
        """Do a http POST request on an api endpoint"""
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
        }

        return self._request(
            method="POST", api_endpoint=api_endpoint, headers=headers, json=payload
        )

    def _request(
        self, method, api_endpoint, params={}, headers={}, json=None, autoreconnect=True
    ):
        # generate url with auth
        headers["authorization"] = "Bearer {}".format(self._token)
        url = "{}{}/?{}".format(
            self._base_url, api_endpoint, urllib.parse.urlencode(params)
        )

        # set user agent
        headers["User-Agent"] = self._user_agent

        # make call
        call = self._session.request(method=method, url=url, headers=headers)

        if call.status_code == 401 and autoreconnect:  # unauthorized error
            # log
            _LOGGER.info(
                "Get unauthorized error (token expired ?), trying to reconnect..."
            )

            # try to reconnect
            self._login()

            # retry get without autoreconnect (to avoid infinite loop)
            return self._request(
                method=method,
                api_endpoint=api_endpoint,
                params=params,
                headers=headers,
                json=json,
                autoreconnect=False,
            )

        # raise other error if needed
        call.raise_for_status()
        #pprint.pprint(url)
        #pprint.pprint(call.json())
        return call.json()
