import logging
import time
from typing import Union
from . import AirzoneCloud, Group
from .constants import MODES_CONVERTER

_LOGGER = logging.getLogger(__name__)


class Device:
    """ Manage a AirzoneCloud device (thermostat) """

    _api: "AirzoneCloud" = None
    _group: "Group" = None
    _data: dict = {}
    _state: dict = {}

    def __init__(self, api: "AirzoneCloud", group: "Group", data: dict) -> None:
        self._api = api
        self._group = group
        self._data = data

        # load state
        self.refresh()

        # log
        _LOGGER.info("Init {}".format(self.str_verbose))
        _LOGGER.debug(data)

    def __str__(self) -> str:
        return "Device(name={}, is_connected={}, is_on={}, mode={}, current_temp={}, target_temp={})".format(
            self.name,
            self.is_connected,
            self.is_on,
            self.mode,
            self.current_temperature,
            self.target_temperature,
        )

    @property
    def str_verbose(self) -> str:
        """ More verbose description of current device """
        return "Device(name={}, is_connected={}, is_on={}, mode={}, current_temp={}, target_temp={}, id={}, ws_id={})".format(
            self.name,
            self.is_connected,
            self.is_on,
            self.mode,
            self.current_temperature,
            self.target_temperature,
            self.id,
            self.ws_id,
        )

    @property
    def all_properties(self) -> dict:
        result = {}
        for prop in [
            "id",
            "name",
            "type",
            "ws_id",
            "system_number",
            "zone_number",
            "is_connected",
            "is_on",
            "mode_id",
            "mode",
            "mode_generic",
            "mode_description",
            "modes_availables",
            "modes_availables_generics",
            "current_humidity",
            "current_temperature",
            "target_temperature",
            "min_temperature",
            "max_temperature",
            "step_temperature",
        ]:
            result[prop] = getattr(self, prop)
        return result

    #
    # getters
    #

    @property
    def id(self) -> str:
        """ Return device id """
        return self._data.get("device_id")

    @property
    def name(self) -> str:
        """ Return device name """
        return self._data.get("name")

    @property
    def type(self) -> str:
        """ Return device type (az_zone┃aidoo) """
        return self._data.get("type")

    @property
    def ws_id(self) -> str:
        """ Return device webserver id (mac address) """
        return self._data.get("ws_id")

    @property
    def system_number(self) -> str:
        """ Return device system_number """
        return self._data.get("meta", {}).get("system_number")

    @property
    def zone_number(self) -> str:
        """ Return device zone_number """
        return self._data.get("meta", {}).get("zone_number")

    @property
    def is_connected(self) -> bool:
        """ Return if the device is online (True) or offline (False) """
        return self._state.get("isConnected", False)

    @property
    def is_on(self) -> bool:
        return self._state.get("power", False)

    @property
    def mode_id(self) -> int:
        """ Return device current id mode (0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12) """
        return self._state.get("mode", 0)

    @property
    def mode(self) -> str:
        """ Return device current mode name (stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling)"""
        return MODES_CONVERTER.get(str(self.mode_id), {}).get("name")

    @property
    def mode_generic(self) -> str:
        """ Return device current generic mode (stop | auto | cooling | heating | ventilation | dehumidify | emergency) """
        return MODES_CONVERTER.get(str(self.mode_id), {}).get("generic")

    @property
    def mode_description(self) -> str:
        """ Return device current mode description (pretty name to display)"""
        return MODES_CONVERTER.get(str(self.mode_id), {}).get("description")

    @property
    def modes_availables_ids(self) -> "list[int]":
        """ Return device availables modes list ([0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12, ...]) """
        return self._state.get("mode_available", [0])

    @property
    def modes_availables(self) -> "list[str]":
        """ Return device availables modes names list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling, ...])"""
        return [
            MODES_CONVERTER.get(str(mode_id), {}).get("name")
            for mode_id in self.modes_availables_ids
        ]

    @property
    def modes_availables_generics(self) -> "list[str]":
        """ Return device availables modes generics list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency, ...])"""
        return list(
            set(
                [
                    MODES_CONVERTER.get(str(mode_id), {}).get("generic")
                    for mode_id in self.modes_availables_ids
                ]
            )
        )

    @property
    def current_temperature(self) -> float:
        """ Return device current temperature in °C """
        return float(self._state.get("local_temp", {}).get("celsius", 0))

    @property
    def current_humidity(self) -> int:
        """ Return device current humidity in percentage (0-100) """
        return int(self._state.get("humidity", 0))

    @property
    def target_temperature(self) -> float:
        """ Return device target temperature for current mode """
        key = MODES_CONVERTER.get(str(self.mode_id), {}).get("setpoint_key")
        return float(self._state.get(key, {}).get("celsius", 0))

    @property
    def min_temperature(self) -> float:
        """ Return device minimal temperature for current mode """
        key = MODES_CONVERTER.get(str(self.mode_id), {}).get("range_key_prefix") + "min"
        return float(self._state.get(key, {}).get("celsius", 0))

    @property
    def max_temperature(self) -> float:
        """ Return device maximal temperature for current mode """
        key = MODES_CONVERTER.get(str(self.mode_id), {}).get("range_key_prefix") + "max"
        return float(self._state.get(key, {}).get("celsius", 0))

    @property
    def step_temperature(self) -> float:
        """ Return device step temperature (minimum increase/decrease step) """
        return float(self._state.get("step", {}).get("celsius", 0.5))

    #
    # setters
    #

    def turn_on(self, auto_refresh: bool = True, delay_refresh: int = 1) -> "Device":
        """ Turn device on """
        _LOGGER.info("call turn_on() on {}".format(self.str_verbose))

        self._set("power", True)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh()

        return self

    def turn_off(self, auto_refresh: bool = True, delay_refresh: int = 1) -> "Device":
        """ Turn device off """
        _LOGGER.info("call turn_off() on {}".format(self.str_verbose))

        self._set("power", False)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh()

        return self

    def set_temperature(
        self, temperature: float, auto_refresh: bool = True, delay_refresh: int = 1
    ) -> "Device":
        """ Set target_temperature for current device in celcius """
        _LOGGER.info(
            "call set_temperature({}) on {}".format(temperature, self.str_verbose)
        )
        if self.min_temperature is not None and temperature < self.min_temperature:
            temperature = self.min_temperature
        if self.max_temperature is not None and temperature > self.max_temperature:
            temperature = self.max_temperature

        self._set("setpoint", temperature)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh()

        return self

    def set_mode(
        self, mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1
    ):
        """ Set mode of the device """
        _LOGGER.info("call set_mode({}) on {}".format(mode_name, self.str_verbose))

        # search mode id
        mode_id_found = None
        for mode_id, mode in MODES_CONVERTER.items():
            if mode["name"] == mode_name:
                mode_id_found = int(mode_id)
                break
        if mode_id_found is None:
            raise ValueError(
                'mode name "{}" not found for {}'.format(mode_name, self.str_verbose)
            )

        if mode_id_found not in self.modes_availables_ids:
            if len(self.modes_availables_ids) == 0:
                raise ValueError(
                    'mode name "{}" (id: {}) not availables for {} : only master thermostat device can set the mode'.format(
                        mode_name,
                        mode_id_found,
                        self.str_verbose,
                        self.modes_availables,
                    )
                )

            raise ValueError(
                'mode name "{}" (id: {}) not availables for {}. Allowed values: {}'.format(
                    mode_name, mode_id_found, self.str_verbose, self.modes_availables
                )
            )

        self._set("mode", mode_id_found)

        if auto_refresh:
            time.sleep(delay_refresh)  # wait data refresh by airzone
            self.refresh()

        return self

    #
    # parent group
    #

    @property
    def group(self) -> Group:
        """ Get parent group """
        return self._group

    #
    # Refresh
    #

    def refresh(self) -> "Device":
        """ Refresh current device data (call refresh_devices on parent AirzoneCloud) """
        _LOGGER.debug("call refresh() on {}".format(self.str_verbose))
        self._state = self._api._api_get_device_state(
            self.id, self.group.installation.id
        )
        _LOGGER.debug(self._state)
        return self

    #
    # private
    #

    def _set(self, param: str, value: Union[str, int, float, bool]) -> "Device":
        """ Refresh current device data (call refresh_devices on parent AirzoneCloud) """
        _LOGGER.debug("call _set({}, {}) on {}".format(param, value, self.str_verbose))
        self._api._api_patch_device(
            self.id, self.group.installation.id, param, value, {"units": 0}
        )
        return self

    def _set_data_refreshed(self, data: dict) -> "Device":
        """ Set data refreshed (called by parent AirzoneCloud on refresh_devices()) """
        self._data = data
        _LOGGER.info("Data refreshed for {}".format(self.str_verbose))
        return self


#
# device raw data example
#

# {
#     "device_id": "60f5cb9...",
#     "meta": {
#         "system_number": 1,
#         "zone_number": 6
#     },
#     "type": "az_zone",
#     "ws_id": "AA:BB:CC:DD:EE:FF",
#     "name": "Salon"
# }

#
# device raw state example
#

# {
#   "active": null,
#   "aq_active": null,
#   "aq_mode_conf": null,
#   "aq_mode_values": [],
#   "aq_quality": null,
#   "aqpm1_0": null,
#   "aqpm2_5": null,
#   "aqpm10": null,
#   "auto_mode": null,
#   "connection_date": "2021-11-17T08:44:04.000Z",
#   "disconnection_date": "2021-11-16T06:24:11.499Z",
#   "eco_conf": "off",
#   "eco_values": [
#     "off",
#     "manual",
#     "a",
#     "a_p",
#     "a_pp"
#   ],
#   "humidity": 48,
#   "isConnected": true,
#   "local_temp": {
#     "celsius": 20.7,
#     "fah": 69
#   },
#   "mode": 3,
#   "mode_available": [
#     2,
#     3,
#     4,
#     5,
#     0
#   ],
#   "name": "Salon",
#   "power": true,
#   "range_sp_cool_air_max": {
#     "fah": 86,
#     "celsius": 30
#   },
#   "range_sp_cool_air_min": {
#     "celsius": 18,
#     "fah": 64
#   },
#   "range_sp_dry_air_max": {
#     "fah": 86,
#     "celsius": 30
#   },
#   "range_sp_dry_air_min": {
#     "celsius": 18,
#     "fah": 64
#   },
#   "range_sp_emerheat_air_max": {
#     "celsius": 30,
#     "fah": 86
#   },
#   "range_sp_emerheat_air_min": {
#     "fah": 59,
#     "celsius": 15
#   },
#   "range_sp_hot_air_max": {
#     "celsius": 30,
#     "fah": 86
#   },
#   "range_sp_hot_air_min": {
#     "fah": 59,
#     "celsius": 15
#   },
#   "range_sp_stop_air_max": {
#     "fah": 86,
#     "celsius": 30
#   },
#   "range_sp_stop_air_min": {
#     "fah": 59,
#     "celsius": 15
#   },
#   "range_sp_vent_air_max": {
#     "fah": 86,
#     "celsius": 30
#   },
#   "range_sp_vent_air_min": {
#     "fah": 59,
#     "celsius": 15
#   },
#   "setpoint_air_heat": {
#     "celsius": 20,
#     "fah": 68
#   },
#   "setpoint_air_stop": {
#     "celsius": 20,
#     "fah": 68
#   },
#   "sleep": 0,
#   "sleep_values": [
#     0,
#     30,
#     60,
#     90
#   ],
#   "speed_conf": null,
#   "speed_type": null,
#   "speed_values": [],
#   "step": {
#     "fah": 1,
#     "celsius": 0.5
#   },
#   "usermode_conf": null,
#   "warnings": [],
#   "zone_sched_available": false
# }
