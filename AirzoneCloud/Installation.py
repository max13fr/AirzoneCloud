import logging
import pprint

from .System import System

_LOGGER = logging.getLogger(__name__)


class Installation:
    """Manage a AirzoneCloud installation"""

    def __init__(self, api, installation_id):
        self._api = api
        self._installation_id = installation_id

        # load all systems
        self.refresh()

        # log
        _LOGGER.info("Init {}".format(self.str_complete))
        _LOGGER.debug(data)

    def __str__(self):
        return "Installation(name={}, status={})".format(self.name, self.status)

    @property
    def str_complete(self):
        return "Installation(name={}, status={}, id={}, mac={})".format(
            self.name, self.status, self.id, self.mac,
        )

    #
    # getters
    #

    @property
    def id(self):
        """ Return installation id """
        return self._data.get("id")

    @property
    def name(self):
        """ Return installation name """
        return self._data.get("name")

    @property
    def status(self):
        """ Return installation status """
        return self._data.get("status")

    @property
    def location(self):
        """ Return installation location """
        return self._data.get("complete_name")

    @property
    def mac(self):
        """ Return installation mac """
        return self._data.get("mac")

    @property
    def pin(self):
        """ Return installation pin code """
        return self._data.get("pin")

    @property
    def target_temperature(self):
        """ Return installation target temperature """
        return self._data.get("consign")

    @property
    def firmware_ws(self):
        """ Return webserver installation """
        return self._data.get("firm_ws")

    @property
    def has_eco(self):
        return self._data.get("has_eco")

    @property
    def has_velocity(self):
        return self._data.get("has_velocity")

    @property
    def has_airflow(self):
        return self._data.get("has_air_flow")

    @property
    def has_farenheit(self):
        return self._data.get("has_harenheit")

    @property
    def sync_datetime(self):
        """ Return True if installation datetime is sync with AirzoneCloud """
        return self._data.get("sync_datetime")

    #
    # children
    #

    @property
    def systems(self):
        return self._systems

    #
    # Refresh
    #

    def refresh(self, refresh_systems=True):
        """ Refresh current installation data (call refresh_installations on parent AirzoneCloud) """
        self._data = self._api._get_installation(self._installation_id)
        #pprint.pprint(self._data)
        if refresh_systems:
            self.refresh_systems()

    def refresh_systems(self):
        """ Refresh all systems of this installation """
        self._load_systems()

    #
    # private
    #

    def _load_systems(self):
        """Load all systems for this installation"""
        current_systems = self._systems
        self._systems = []
        try:
            for system_data in self._api._get_systems(self.id):
                system = None
                # search system in current_systems (if where are refreshing systems)
                for current_system in current_systems:
                    if current_system.id == system_data.get("id"):
                        system = current_system
                        system._set_data_refreshed(system_data)
                        break
                # system not found => instance new system
                if system is None:
                    system = System(self._api, self, system_data)
                self._systems.append(system)
        except RuntimeError:
            raise Exception(
                "Unable to load systems of installation {} ({}) from AirzoneCloud".format(
                    self.name, self.id
                )
            )
        return self._systems

    def _set_data_refreshed(self, data):
        """ Set data refreshed (call by parent AirzoneCloud on refresh_installations()) """
        self._data = data
        _LOGGER.info("Data refreshed for {}".format(self.str_complete))


#
# installation raw data example
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
