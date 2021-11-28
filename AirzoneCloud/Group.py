import logging

from . import AirzoneCloud, Installation
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

    # XXX
    def refresh(self, refresh_devices: bool = True):
        """ Refresh current group data (call refresh_groups on parent AirzoneCloud) """
        self._api.refresh_groups()
        if refresh_devices:
            self.refresh_devices()

    # XXX
    def refresh_devices(self):
        """ Refresh all devices of this group """
        self._load_devices()

    #
    # private
    #

    def _load_devices(self) -> "list[Device]":
        """Load all devices for this group"""
        previous_devices = self._devices
        self._devices = []
        for device_data in self._data.get("devices", []):
            # skip fake system device
            if device_data.get("type") == "az_system":
                continue
            device = None
            # search device in previous_devices (if where are refreshing devices)
            for previous_device in previous_devices:
                if previous_device.id == device_data.get("device_id"):
                    device = previous_device
                    device._set_data_refreshed(device_data)
                    break
            # device not found => instance new device
            if device is None:
                device = Device(self._api, self, device_data)
            self._devices.append(device)
        return self._devices

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
