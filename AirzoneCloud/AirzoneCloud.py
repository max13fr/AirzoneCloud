#!/usr/bin/python3

import json
import logging
import pprint
import requests
import urllib
import urllib.parse

from .contants import (
    API_LOGIN,
    API_SITES,
    API_ZONES,
    API_ZONE,
    API_EVENTS,
)
from .Site import Site

_LOGGER = logging.getLogger(__name__)


class AirzoneCloud:
    """Allow to connect to AirzoneCloud API"""

    _session = None
    _username = None
    _password = None
    _base_url = "https://m.airzonecloud.com"
    _user_agent = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X; wv) AppleWebKit/537.26 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Safari/537.36"
    _token = None
    _sites = {}

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
        # load sites
        self._load_sites()

    #
    # getters
    #

    @property
    def sites(self):
        """Get sites list (same order as in app)"""
        return list(self._sites.values())

    @property
    def all_systems(self):
        """Get all systems from all sites (same order as in app)"""
        result = []
        for site in self.sites:
            for system in site.systems:
                result.append(system)
        return result

    @property
    def all_zones(self):
        """Get all zones from all sites (same order as in app)"""
        result = []
        for site in self.sites:
            for system in site.systems:
                for zone in system.zones:
                    result.append(zone)
        return result

    #
    # Refresh
    #

    def refresh_sites(self):
        """Refresh sites"""
        self._load_sites()

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

    def _load_sites(self):
        """Load all sites for this account"""
        current_sites = self._sites
        self._sites = {}
        try:
            for site_data in self._get_sites():
                #pprint.pprint(site_data)
                site_id = site_data.get("installation_id")
                site = current_sites.get(site_id)
                # site not found => instance new site
                if site is None:
                    site = Site(self, site_id)
                else:
                    site.refersh();
                self._sites[site.id] = site
        except RuntimeError:
            raise Exception("Unable to load sites from AirzoneCloud")
        return self._sites

    def _get_sites(self):
        """Http GET to load sites"""
        _LOGGER.debug("get_sites()")
        return self._get(API_SITES).get("installations")

    def _get_site(self, site_id):
        """Http GET to load site"""
        _LOGGER.debug("get_site({})".format(site_id))
        return self._get("{}/{}".format(API_SITES, site_id))

    def _get_zone(self, zone_id):
        """Http GET to load Zone"""
        _LOGGER.debug("get_zone({})".format(zone_id))
        return self._get("{}/{}".format(API_ZONES, "60f817cc7b7b998ed14b58f9"))

    def _get_zone_config(self, site_id, zone_id):
        """Http GET to load Zone"""
        _LOGGER.debug("get_zone_config({}, {})".format(site_id, zone_id))
        return self._get("{}/{}/config".format(API_ZONE, zone_id), params = { "installation_id": site_id, "type": "user"})

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
        #pprint.pprint(url)

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
        #pprint.pprint(call.json())
        return call.json()
