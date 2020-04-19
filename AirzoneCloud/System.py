import logging
from .contants import MODES_CONVERTER
from .Zone import Zone

_LOGGER = logging.getLogger(__name__)


class System:
    """Manage a AirzoneCloud system"""

    _api = None
    _device = None
    _data = {}
    _zones = []

    def __init__(self, api, device, data):
        self._api = api
        self._device = device
        self._data = data

        # log
        _LOGGER.info(
            "Init system '{}' (id={}, system_number={}, device_id={})".format(
                self.name, self.id, self.system_number, self.device_id
            )
        )
        _LOGGER.debug(data)

        # load zones
        self._load_zones()

    def __str__(self):
        return 'System("{}")'.format(self.name)

    #
    # getters
    #

    @property
    def id(self):
        return self._data.get("id")

    @property
    def name(self):
        return self._data.get("name")

    @property
    def system_number(self):
        return self._data.get("system_number")

    @property
    def device_id(self):
        return self._data.get("device_id")

    #
    # setters
    #

    def set_mode(self, mode_name):
        """ Set mode of the system """
        _LOGGER.info("call set_mode({}) on {}".format(mode_name, self))
        mode_id_found = None
        for mode_id, mode in MODES_CONVERTER.items():
            if mode["name"] == mode_name:
                mode_id_found = mode_id
                break
        if mode_id_found is None:
            raise ValueError('mode name "{}" not found'.format(mode_name))

        # send event
        self._send_event("mode", int(mode_id_found))

        # update mode
        self._data["mode"] = mode_id_found

        # refresh modes on sub-zones (don't refresh because API so slow to update sub-zones, about 5sec...)
        for zone in self.zones:
            zone._data["mode"] = mode_id_found

        return True

    #
    # children zones
    #

    @property
    def zones(self):
        """ Get all zones in this system """
        return self._zones

    #
    # parent device
    #

    @property
    def device(self):
        """ Get parent device """
        return self._device

    #
    # Refresh zone data
    #

    def refresh_zones(self):
        """ Refresh current system data and all zones insides """
        self._load_zones()

    #
    # private
    #

    def _load_zones(self):
        """Load all zones for this system"""
        current_zones = self._zones
        self._zones = []
        try:
            for zone_data in self._api._get_zones(self.id):
                zone = None
                # search zone in current_zones (where are refreshing zones)
                for current_zone in current_zones:
                    if current_zone.id == zone_data.get("id"):
                        zone = current_zone
                        zone._set_data_refreshed(zone_data)
                        break
                # zone not found => instance new zone
                if zone is None:
                    zone = Zone(self._api, self, zone_data)
                self._zones.append(zone)
        except RuntimeError:
            raise Exception(
                "Unable to load zones of system {} ({}) from AirzoneCloud".format(
                    self.name, self.id
                )
            )

        return self._zones

    def _send_event(self, option, value):
        """ Send an event for current system """
        payload = {
            "event": {
                "cgi": "modsistema",
                "device_id": self.device_id,
                "system_number": self.system_number,
                "option": option,
                "value": value,
            }
        }
        return self._api._send_event(payload)


#
# System raw data example
#

# {
#     "id": "...",
#     "device_id": "...",
#     "name": "Home",
#     "eco": "2",
#     "eco_color": "5",
#     "velocity": null,
#     "air_flow": null,
#     "connMC": null,
#     "VMC_mode": "0",
#     "VMC_state": "0",
#     "has_velocity": false,
#     "has_air_flow": false,
#     "mode": "5",
#     "modes": "1111111011",
#     "master_setup": false,
#     "setup_type": "0",
#     "max_limit": "30.0",
#     "min_limit": "18.0",
#     "zones_ids": [
#         "id1...",
#         "id2...",
#         "id3...",
#         "id4...",
#     ],
#     "class": "System",
#     "updated_at": 1587195368,
#     "system_number": "1",
#     "last_update": 1587195368,
#     "firm_ws": "3.173",
#     "scene": null,
#     "auto": null,
#     "temperature_unit": null,
#     "autochange_differential": null,
#     "config_ZBS_visible_environment": null,
#     "system_fw": 3.09,
#     "heat_stages": "1",
#     "cold_stages": null,
#     "auto_index_prog": true,
#     "system_errors": "00000001",
#     "auto_mode_battery_temperature": false,
#     "machine_error_code": "ÿÿÿÿ",
#     "setpoint": null,
#     "tank_temp": null,
#     "powerful": null,
#     "power_acs": null,
#     "acs_min": null,
#     "acs_max": null,
# }
