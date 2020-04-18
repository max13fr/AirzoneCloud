import logging
from .Zone import Zone

_LOGGER = logging.getLogger(__name__)


class System:
    """Manage a AirzoneCloud system"""

    def __init__(self, api, data):
        self._api = api
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
    # children
    #

    @property
    def zones(self):
        return self._zones

    #
    # private
    #

    def _load_zones(self):
        """Load all zones for this system"""
        self._zones = []
        try:
            for zone in self._api._get_zones(self.id):
                self._zones.append(Zone(self._api, zone))
        except RuntimeError:
            raise Exception(
                "Unable to load zones of system {} (%) from AirzoneCloud".format(
                    self.name, self.id
                )
            )

        return self._zones


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
