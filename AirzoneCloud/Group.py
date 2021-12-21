import logging
import time
from typing import Union
from . import AirzoneCloud, Installation
from .constants import MODES_CONVERTER
from .Device import Device

_LOGGER = logging.getLogger(__name__)


class Group:
    """Manage a AirzoneCloud group"""

    _api: AirzoneCloud = None
    _installation: Installation = None
    _data: dict = {}
    _devices: "list[Device]" = []

    def __init__(
        self, api: AirzoneCloud, installation: Installation, data: dict
    ) -> None:
        self._api = api
        self._installation = installation
        self._data = data

        # log
        _LOGGER.info("Init {}".format(self.str_verbose))
        _LOGGER.debug(data)

        # load all devices
        self._load_devices()

    def __str__(self) -> str:
        return "Group(name={}, installation={})".format(
            self.name, self._installation.name
        )

    @property
    def str_verbose(self) -> str:
        """ More verbose description of current group """
        return "Group(name={}, installation={}, id={})".format(
            self.name, self._installation.name, self.id
        )

    #
    # getters
    #

    @property
    def id(self) -> str:
        """ Return group id """
        return self._data.get("group_id")

    @property
    def name(self) -> str:
        """ Return group name """
        return self._data.get("name")

    #
    # setters
    #

    def turn_on(self, auto_refresh: bool = True, delay_refresh: int = 1) -> "Group":
        """ Turn on all devices in the group """
        _LOGGER.info("call turn_on() on {}".format(self.str_verbose))

        for device in self.devices:
            device.turn_on(auto_refresh=False)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh_devices()

        return self

    def turn_off(self, auto_refresh: bool = True, delay_refresh: int = 1) -> "Group":
        """ Turn off all devices in the group """
        _LOGGER.info("call turn_off() on {}".format(self.str_verbose))

        for device in self.devices:
            device.turn_off(auto_refresh=False)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh_devices()

        return self

    def set_temperature(
        self, temperature: float, auto_refresh: bool = True, delay_refresh: int = 1
    ) -> "Group":
        """ Set target_temperature for current all devices in the group (in degrees celsius) """
        _LOGGER.info(
            "call set_temperature({}) on {}".format(temperature, self.str_verbose)
        )

        for device in self.devices:
            if device.is_master:
                device.set_temperature(temperature=temperature, auto_refresh=False)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh_devices()

        return self

    def set_mode(
        self, mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1
    ) -> "Group":
        """ Set mode of the all devices in the group """
        _LOGGER.info("call set_mode({}) on {}".format(mode_name, self.str_verbose))

        for device in self.devices:
            if device.is_master:
                device.set_mode(mode_name=mode_name, auto_refresh=False)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh_devices()

        return self

    #
    # parent installation
    #

    @property
    def installation(self) -> Installation:
        """ Get parent installation """
        return self._installation

    #
    # children
    #

    @property
    def devices(self) -> "list[Device]":
        return self._devices

    #
    # Refresh
    #

    def refresh_devices(self) -> "Group":
        """ Refresh all devices of this group """
        for device in self.devices:
            device.refresh()
        return self

    #
    # private
    #

    def _load_devices(self) -> "list[Device]":
        """Load all devices for this group"""
        previous_devices = self._devices
        self._devices = []
        for device_data in self._data.get("devices", []):
            # skip fake system device
            if device_data.get("type") != "az_zone":
                continue
            device = None
            # search device in previous_devices (if where are refreshing devices)
            for previous_device in previous_devices:
                if previous_device.id == device_data.get("device_id"):
                    device = previous_device
                    # update data
                    device._set_data_refreshed(device_data)
                    break
            # device not found => instance new device
            if device is None:
                device = Device(self._api, self, device_data)
            self._devices.append(device)
        return self._devices

    def _set(self, param: str, value: Union[str, int, float, bool]) -> "Group":
        """ Execute a command to the current device (power, mode, setpoint, ...) """
        _LOGGER.debug("call _set({}, {}) on {}".format(param, value, self.str_verbose))
        self._api._api_put_group(
            self.id, self.group.installation.id, param, value, {"units": 0}
        )
        return self

    def _set_data_refreshed(self, data: dict) -> "Group":
        """ Set data refreshed (called by parent Installation on refresh_groups()) """
        self._data = data
        _LOGGER.info("Data refreshed for {}".format(self.str_verbose))
        return self


#
# group raw data example
#

# {
#     "group_id": "60f5cb99ff517e33f0365733",
#     "name": "Système 1",
#     "devices": [
#         {
#             "device_id": "60f5cb...",
#             "meta": {"system_number": 1},
#             "type": "az_system",
#             "ws_id": "AA:BB:CC:DD:EE:FF",
#         },
#         {
#             "device_id": "60f5cb...",
#             "meta": {"system_number": 1, "zone_number": 6},
#             "type": "az_zone",
#             "ws_id": "AA:BB:CC:DD:EE:FF",
#             "name": "Salon",
#         },
#         {
#             "device_id": "60f5cb991...",
#             "meta": {"system_number": 1, "zone_number": 4},
#             "type": "az_zone",
#             "ws_id": "AA:BB:CC:DD:EE:FF",
#             "name": "Ch parents",
#         },
#         {
#             "device_id": "60f5cb9...",
#             "meta": {"system_number": 1, "zone_number": 5},
#             "type": "az_zone",
#             "ws_id": "AA:BB:CC:DD:EE:FF",
#             "name": "Ch bebe",
#         },
#     ],
# }
