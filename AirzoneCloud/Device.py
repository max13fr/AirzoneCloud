import logging
from .System import System

_LOGGER = logging.getLogger(__name__)


class Device:
    """Manage a AirzoneCloud device"""

    def __init__(self, api, data):
        self._api = api

        # remove weather (huge array with all translates)
        if "data" in data and "data" in data["data"]:
            data["data"]["data"].pop("weather", True)
        self._data = data

        # log
        _LOGGER.info("Init device '{}' (id={})".format(self.name, self.id))
        _LOGGER.debug(data)

        # load all systems
        self._load_systems()

    def __str__(self):
        return 'Device("{}")'.format(self.name)

    #
    # getters
    #

    @property
    def id(self):
        """ Return device id """
        return self._data.get("id")

    @property
    def name(self):
        """ Return device name """
        return self._data.get("name")

    @property
    def location(self):
        """ Return device location """
        return self._data.get("complete_name")

    #
    # children
    #

    @property
    def systems(self):
        return self._systems

    #
    # private
    #

    def _load_systems(self):
        """Load all systems for this device"""
        self._systems = []
        try:
            for system in self._api._get_systems(self.id):
                self._systems.append(System(self._api, system))
        except RuntimeError:
            raise Exception(
                "Unable to load systems of device {} (%) from AirzoneCloud".format(
                    self.name, self.id
                )
            )

        return self._systems


#
# device raw data example
#

# {
#     "id": "...",
#     "mac": "AA:BB:CC:DD:EE:FF",
#     "pin": "1234",
#     "name": "Home",
#     "icon": 5,
#     "consign": "19.0",
#     "sync_datetime": True,
#     "remote_control": False,
#     "firm_ws": "3.173",
#     "status": "activated",
#     "connection_date": "2020-04-18T08:58:15.000+00:00",
#     "has_eco": True,
#     "has_velocity": False,
#     "spot_name": "Marseille",
#     "complete_name": "Marseille,Bouches-du-Rhône,Provence-Alpes-Côte d'Azur,France",
#     "country_code": "FR",
#     "electricity_prices": {},
#     "location": {"latitude": 43.00000000000000, "longitude": 5.00000000000000},
#     "data": {
#         "data": {
#             "time_zone": [
#                 {
#                     "localtime": "2020-04-18 05:34",
#                     "utcOffset": "2.0",
#                     "zone": "Europe/Paris",
#                 }
#             ]
#         }
#     },
#     "modes": "00001111111011",
#     "has_air_flow": False,
#     "has_scene": False,
#     "has_farenheit": False,
# }
