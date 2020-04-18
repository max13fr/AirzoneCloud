import logging
from .contants import MODES_CONVERTER

_LOGGER = logging.getLogger(__name__)


class Zone:
    """Manage a Airzonecloud zone"""

    def __init__(self, api, data):
        self._api = api
        self._data = data

        _LOGGER.info(
            "Init zone '{}' (id={}, system_number={}, zone_number={}, current_temperature={} target_temperature={})".format(
                self.name,
                self.id,
                self.system_number,
                self.zone_number,
                self.current_temperature,
                self.target_temperature,
            )
        )

        _LOGGER.debug(data)

    def __str__(self):
        return 'Zone("{}")'.format(self.name)

    #
    # getters
    #

    @property
    def name(self):
        return self._data.get("name")

    @property
    def current_temperature(self):
        if self._data.get("temp") is not None:
            return float(self._data.get("temp"))
        return None

    @property
    def current_humidity(self):
        if self._data.get("humidity") is not None:
            return float(self._data.get("humidity"))
        return None

    @property
    def target_temperature(self):
        if self._data.get("consign") is not None:
            return float(self._data.get("consign"))
        return None

    @property
    def max_temp(self):
        if self._data.get("upper_conf_limit") is not None:
            return float(self._data.get("upper_conf_limit"))
        return None

    @property
    def min_temp(self):
        if self._data.get("lower_conf_limit") is not None:
            return float(self._data.get("lower_conf_limit"))
        return None

    @property
    def is_on(self):
        return bool(int(self._data.get("state", 0)))

    @property
    def mode(self):
        return self._data.get("mode")

    @property
    def mode_name(self):
        return MODES_CONVERTER[self.mode]["name"]

    @property
    def mode_description(self):
        return MODES_CONVERTER[self.mode]["description"]

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
    def zone_number(self):
        return self._data.get("zone_number")

    #
    # setters
    #

    def turn_on(self):
        self._data["state"] = "1"
        self._send_event("state", 1)
        return True

    def turn_off(self):
        self._data["state"] = "0"
        self._send_event("state", 0)
        return True

    #
    # private
    #

    def _send_event(self, option, value):
        payload = {
            "event": {
                "cgi": "modzona",
                "device_id": self.device_id,
                "system_number": self.system_number,
                "zone_number": self.zone_number,
                "option": option,
                "value": value,
            }
        }
        return self._api._send_event(payload)


#
# Zone raw data example
#

# {
#     "id": "...",
#     "system_id": "...",
#     "device_id": "...",
#     "modes": "1111111011",
#     "warning": "0",
#     "name": "Living room",
#     "system_number": "1",
#     "zone_number": "6",
#     "state": "1",
#     "consign": "21.5",
#     "temp": "21.4",
#     "mode": "5",
#     "velocity": None,
#     "show_velocity": None,
#     "sleep": "0",
#     "lower_conf_limit": "18.0",
#     "upper_conf_limit": "30.0",
#     "master": "1",
#     "velMax": None,
#     "eco": "2",
#     "prog_enabled": "1",
#     "speed_prog_mode": "0",
#     "show_ventilation": "1",
#     "updated_at": 1587190474,
#     "setup_type": "0",
#     "class": "Zone",
#     "last_update": 1587190474,
#     "next_schedule_number": 4,
#     "led": None,
#     "offset": None,
#     "cold_offset": None,
#     "heat_offset": None,
#     "scene": None,
#     "air_flow": None,
#     "humidity": "42",
#     "coldConsign": "",
#     "heatConsign": "",
#     "auto": None,
#     "temperature_unit": None,
#     "vla": None,
#     "config": {
#         "id": "...",
#         "cold_values": "1",
#         "heat_values": "1",
#         "cold_angle": None,
#         "heat_angle": None,
#         "swing_horizontal": None,
#         "swing_vertical": None,
#         "antifreeze": "0",
#         "vla": None,
#         "zone_number": "6",
#         "slave": None,
#         "master": None,
#         "basic_mode": "0",
#         "ambient_temp": "24.6",
#         "heat_type": None,
#         "cold_type": None,
#         "heat_type_config": "1",
#         "cold_type_config": "1",
#         "ventilation": None,
#         "q_weight": None,
#         "window": None,
#         "presence": None,
#         "spray_dew": None,
#         "local_vent": None,
#         "tact_fw": "3. 7",
#         "firm_lm": None,
#         "manufacturer": None,
#         "led": None,
#         "velMax": None,
#         "confort_cold_consign": None,
#         "confort_heat_consign": None,
#         "eco_cold_consign": None,
#         "eco_heat_consign": None,
#         "unocupied_cold_consign": None,
#         "unocupied_heat_consign": None,
#         "vacation_cold_consign": None,
#         "vacation_heat_consign": None,
#         "firm_ws": "3.173",
#         "offset": None,
#         "errors": "0",
#         "zone_id": "...",
#         "automatic_weight": None,
#         "autochange_differential": None,
#         "offset_environment_cold": None,
#         "offset_environment_heat": None,
#         "eco_function": None,
#         "heat_constant_ventilation": None,
#         "cold_constant_ventilation": None,
#         "v_min_module_010": None,
#         "v_max_module_010": None,
#         "cold_battery_temperature": None,
#         "heat_battery_temperature": None,
#         "VAF_coldstage": None,
#         "VAF_heatstage": None,
#         "VAF_radiantstage": None,
#     },
# }
