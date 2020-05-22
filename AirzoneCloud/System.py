import logging
from .contants import (
    MODES_CONVERTER,
    ECO_CONVERTER,
    VELOCITIES_CONVERTER,
    AIRFLOW_CONVERTER,
)
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
        _LOGGER.info("Init {}".format(self.str_complete))
        _LOGGER.debug(data)

        # load zones
        self._load_zones()

    def __str__(self):
        return "System(name={}, mode={}, eco={}, velocity={}, airflow={})".format(
            self.name, self.mode, self.eco, self.velocity, self.airflow,
        )

    @property
    def str_complete(self):
        return "System(name={}, mode={}, eco={}, velocity={}, airflow={}, id={}, system_number={}, device_id={})".format(
            self.name,
            self.mode,
            self.eco,
            self.velocity,
            self.airflow,
            self.id,
            self.system_number,
            self.device_id,
        )

    #
    # getters
    #

    @property
    def name(self):
        return self._data.get("name")

    @property
    def mode(self):
        if self.mode_raw is None:
            return None
        return MODES_CONVERTER[self.mode_raw]["name"]

    @property
    def mode_description(self):
        if self.mode_raw is None:
            return None
        return MODES_CONVERTER[self.mode_raw]["description"]

    @property
    def mode_raw(self):
        return self._data.get("mode")

    @property
    def eco(self):
        if self.eco_raw is None:
            return None
        return ECO_CONVERTER[self.eco_raw]["name"]

    @property
    def eco_description(self):
        if self.eco_raw is None:
            return None
        return ECO_CONVERTER[self.eco_raw]["description"]

    @property
    def eco_raw(self):
        return self._data.get("eco")

    @property
    def has_velocity(self):
        return self._data.get("has_velocity")

    @property
    def velocity(self):
        if self.velocity_raw is None:
            return None
        return VELOCITIES_CONVERTER[self.velocity_raw]["name"]

    @property
    def velocity_description(self):
        if self.velocity_raw is None:
            return None
        return VELOCITIES_CONVERTER[self.velocity_raw]["description"]

    @property
    def velocity_raw(self):
        return self._data.get("velocity")

    @property
    def has_airflow(self):
        return self._data.get("has_air_flow")

    @property
    def airflow(self):
        if self.airflow_raw is None:
            return None
        return AIRFLOW_CONVERTER[self.airflow_raw]["name"]

    @property
    def airflow_description(self):
        if self.airflow_raw is None:
            return None
        return AIRFLOW_CONVERTER[self.airflow_raw]["description"]

    @property
    def airflow_raw(self):
        return self._data.get("air_flow")

    @property
    def max_temp(self):
        if self._data.get("max_limit") is not None:
            return float(self._data.get("max_limit"))
        return None

    @property
    def min_temp(self):
        if self._data.get("min_limit") is not None:
            return float(self._data.get("min_limit"))
        return None

    @property
    def id(self):
        return self._data.get("id")

    @property
    def device_id(self):
        return self._data.get("device_id")

    @property
    def system_number(self):
        return self._data.get("system_number")

    @property
    def firmware_ws(self):
        return self._data.get("firm_ws")

    @property
    def firmware_system(self):
        return self._data.get("system_fw")

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
    # children
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
    # Refresh
    #

    def ask_airzone_update(self):
        """
        Ask an update to the airzone hardware (airzonecloud don't autopull data like current temperature)
        The update should be available in airzonecloud after 3 to 5 secs in average
        """
        self._ask_airzone_update()

    def refresh(self, refresh_zones=True):
        """ Refresh current system data (call refresh_systems on parent device) """

        # ask airzone to update its data in airzonecloud (there is some delay so current update will be available on next refresh)
        self.ask_airzone_update()

        # refresh systems (including current) from parent device
        self.device.refresh_systems()

        # refresh subzones in needed
        if refresh_zones:
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
                # search zone in current_zones (if where are refreshing zones)
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

    def _ask_airzone_update(self):
        """Ask an update to the airzone hardware (airzonecloud don't autopull data)"""
        payload = {
            "event": {
                "cgi": "infosistema2",
                "device_id": self.device_id,
                "system_number": self.system_number,
                "option": None,
                "value": None,
            }
        }
        return self._api._send_event(payload)

    def _set_data_refreshed(self, data):
        """ Set data refreshed (call by parent device on refresh_systems()) """
        self._data = data
        _LOGGER.info("Data refreshed for {}".format(self.str_complete))


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
