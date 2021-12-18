#!/usr/bin/python3

import logging
from typing import Any, Union
import requests
import urllib
import urllib.parse

from .Installation import Installation
from .Group import Group
from .Device import Device
from .constants import API_URL

_LOGGER = logging.getLogger(__name__)


class AirzoneCloud:
    """Allow to connect to AirzoneCloud API"""

    _email: str = None
    _password: str = None
    _user_agent: str = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X; wv) AppleWebKit/537.26 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Safari/537.36"
    _session: requests.Session = None
    _token: str = None
    _installations: "list[Installation]" = []

    def __init__(self, email: str, password: str, user_agent: str = None) -> None:
        """Initialize API connection"""
        self._email = email
        self._password = password
        if user_agent is not None and isinstance(user_agent, str):
            self._user_agent = user_agent

        # init new Session
        self._session = requests.Session()

        # login
        self._login()

        # load installations
        self._load_installations()

    #
    # getters
    #

    @property
    def installations(self) -> "list[Installation]":
        """ Get installations list """
        return self._installations

    @property
    def all_groups(self) -> "list[Group]":
        """ Get all groups from all installations """
        result = []
        for installation in self.installations:
            for group in installation.groups:
                result.append(group)
        return result

    @property
    def all_devices(self) -> "list[Device]":
        """ Get all devices from all installations """
        result = []
        for group in self.installations:
            for device in group.all_devices:
                result.append(device)
        return result

    #
    # Refresh
    #

    def refresh_installations(self) -> "AirzoneCloud":
        """Refresh installations"""
        self._load_installations()
        return self

    #
    # private
    #

    def _login(self) -> str:
        """Login to  AirzoneCloud and return token"""

        try:
            url = "{}/auth/login".format(API_URL)
            login_payload = {"email": self._email, "password": self._password}
            headers = {"User-Agent": self._user_agent}
            response = self._session.post(url, headers=headers, json=login_payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(
                "Unable to login to AirzoneCloud with the email {} and the given password".format(
                    self._email
                )
            ) from None

        self._token = response.json().get("token")
        if not self._token:
            raise Exception(
                "Unable to login to AirzoneCloud, cannot get token from response : {}".format(
                    response
                )
            )

        _LOGGER.info("Login success as {}".format(self._email))

        return self._token

    def _load_installations(self) -> "list[Installation]":
        """Load all installations for this account"""
        previous_installations = self._installations
        self._installations = []
        try:
            for installation_data in self._api_get_installations_list():
                installation = None
                # search installation in previous_installations (if where are refreshing installations)
                for previous_installation in previous_installations:
                    if previous_installation.id == installation_data.get(
                        "installation_id"
                    ):
                        installation = previous_installation
                        installation._set_data_refreshed(installation_data)
                        break
                # installation not found => instance new installation
                if installation is None:
                    installation = Installation(self, installation_data)
                self._installations.append(installation)
        except RuntimeError:
            raise Exception("Unable to load installations from AirzoneCloud")
        return self._installations

    #
    # API calls
    #

    def _api_get_installations_list(self) -> list:
        """ Http GET to load installations relations"""
        _LOGGER.debug("_api_get_installations_list()")
        # TODO manage pagination (10 installations max currently)
        return self._api_get("/installations").get("installations", [])

    def _api_get_installation_groups_list(self, installation_id: str) -> list:
        """ Http GET to load groups in a specific installation """
        _LOGGER.debug(
            "_api_get_installation_groups_list(installation_id={})".format(
                installation_id
            )
        )
        return self._api_get("/installations/{}".format(installation_id)).get(
            "groups", []
        )

    def _api_get_device_state(self, device_id: str, installation_id: str) -> dict:
        """ Http GET to load state of a specific device """
        _LOGGER.debug(
            "_api_get_device_state(device_id={}, installation_id={})".format(
                device_id, installation_id
            )
        )
        return self._api_get(
            "/devices/{}/status".format(device_id),
            {"installation_id": installation_id},
        )

    def _api_get_device_config(
        self, device_id: str, installation_id: str, type: str = "all"
    ) -> dict:
        """ Http GET to load config of a specific device """
        _LOGGER.debug(
            "_api_get_device_config(device_id={}, installation_id={}, type={})".format(
                device_id, installation_id, type
            )
        )
        return self._api_get(
            "/devices/{}/config".format(device_id),
            {"installation_id": installation_id, "type": type},
        )

    def _api_patch_device(
        self,
        device_id: str,
        installation_id: str,
        param: str,
        value: Union[str, int, float, bool],
        opts: dict = {},
    ) -> Any:
        """ Http PATCH to change a device parameter (state or config) """
        _LOGGER.debug(
            "_api_patch_device(device_id={}, installation_id={}, param={}, value={}, opts={})".format(
                device_id, installation_id, param, value, opts
            )
        )
        return self._api_patch(
            "/devices/{}".format(device_id),
            {
                "installation_id": installation_id,
                "param": param,
                "value": value,
                "opts": opts,
            },
        )

    def _api_get(self, api_endpoint: str, params: dict = {}) -> Any:
        """Do a http GET request on an api endpoint"""

        params["format"] = "json"

        return self._api_request(method="GET", api_endpoint=api_endpoint, params=params)

    def _api_post(self, api_endpoint: str, payload: dict = {}) -> Any:
        """Do a http POST request on an api endpoint"""

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        }

        return self._api_request(
            method="POST", api_endpoint=api_endpoint, headers=headers, json=payload
        )

    def _api_put(self, api_endpoint: str, payload: dict = {}) -> Any:
        """Do a http PUT request on an api endpoint"""

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        }

        return self._api_request(
            method="PUT", api_endpoint=api_endpoint, headers=headers, json=payload
        )

    def _api_patch(self, api_endpoint: str, payload: dict = {}) -> Any:
        """Do a http PATCH request on an api endpoint"""

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        }

        return self._api_request(
            method="PATCH", api_endpoint=api_endpoint, headers=headers, json=payload
        )

    def _api_request(
        self,
        method: str,
        api_endpoint: str,
        params: dict = {},
        headers: dict = {},
        json: dict = None,
        autoreconnect: bool = True,
    ) -> Any:
        """Do a http generic request on an api endpoint"""

        # set headers
        headers["Authorization"] = "Bearer {}".format(self._token)
        headers["User-Agent"] = self._user_agent

        # generate url
        url = "{}{}/?{}".format(API_URL, api_endpoint, urllib.parse.urlencode(params))

        # make call
        call = self._session.request(method=method, url=url, headers=headers, json=json)

        if call.status_code == 401 and autoreconnect:  # unauthorized error
            # log
            _LOGGER.info(
                "Get unauthorized error (token expired ?), trying to reconnect..."
            )

            # try to reconnect
            self._login()

            # retry get without autoreconnect (to avoid infinite loop)
            return self._api_request(
                method=method,
                api_endpoint=api_endpoint,
                params=params,
                headers=headers,
                json=json,
                autoreconnect=False,
            )

        # raise other error if needed
        try:
            call.raise_for_status()
        except requests.exceptions.HTTPError as err:
            _LOGGER.error(call.text)
            raise err

        # decode json only if response is not empty
        if len(call.text):
            return call.json()

        return None

