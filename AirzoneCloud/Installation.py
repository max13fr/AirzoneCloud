import logging

from . import AirzoneCloud
from .Group import Group
from .Device import Device

_LOGGER = logging.getLogger(__name__)


class Installation:
    """Manage a AirzoneCloud installation"""

    _api: AirzoneCloud = None
    _data: dict = {}
    _groups: "list[Group]" = []

    def __init__(self, api: AirzoneCloud, data: dict) -> None:
        self._api = api
        self._data = data

        # log
        _LOGGER.info("Init {}".format(self.str_verbose))
        _LOGGER.debug(data)

        # load all groups
        self._load_groups()

    def __str__(self) -> str:
        return "Installation(name={})".format(self.name)

    @property
    def str_verbose(self) -> str:
        """ More verbose description of current installation """
        return "Installation(name={}, access_type={}, ws_ids=[{}], id={})".format(
            self.name, self.access_type, ", ".join(self.ws_ids), self.id
        )

    #
    # getters
    #

    @property
    def id(self) -> str:
        """ Return installation id """
        return self._data.get("installation_id")

    @property
    def name(self) -> str:
        """ Return installation name """
        return self._data.get("name")

    @property
    def access_type(self) -> str:
        """ Return installation access_type (admin┃advanced┃basic) """
        return self._data.get("access_type")

    @property
    def location_id(self) -> str:
        """ Return installation location id """
        return self._data.get("location_id")

    @property
    def ws_ids(self) -> str:
        """ Return array of Webserver MAC addresses belonging to the installation """
        return self._data.get("ws_ids", [])

    #
    # children
    #

    @property
    def groups(self) -> "list[Group]":
        """ Get all groups in the current installation """
        return self._groups

    @property
    def all_devices(self) -> "list[Device]":
        """ Get all devices from all groups in the current installation """
        result = []
        for group in self.groups:
            for device in group.devices:
                result.append(device)
        return result

    #
    # Refresh
    #

    # XXX
    def refresh(self, refresh_groups: bool = True):
        """ Refresh current installation data (call refresh_installations on parent AirzoneCloud) """
        self._api.refresh_installations()
        if refresh_groups:
            self.refresh_groups()

    # XXX
    def refresh_groups(self):
        """ Refresh all groups of this installation """
        self._load_groups()

    #
    # private
    #

    def _load_groups(self) -> "list[Group]":
        """Load all groups for this installation"""
        previous_groups = self._groups
        self._groups = []
        try:
            for group_data in self._api._api_get_installation_groups_list(self.id):
                group = None
                # search group in previous_groups (if where are refreshing groups)
                for previous_group in previous_groups:
                    if previous_group.id == group_data.get("group_id"):
                        group = previous_group
                        group._set_data_refreshed(group_data)
                        break
                # group not found => instance new group
                if group is None:
                    group = Group(self._api, self, group_data)
                self._groups.append(group)
        except RuntimeError:
            raise Exception(
                "Unable to load groups for Installation " + self.str_verbose
            )
        return self._groups

    def _set_data_refreshed(self, data: dict) -> "Installation":
        """ Set data refreshed (called by parent AirzoneCloud on refresh_installations()) """
        self._data = data
        _LOGGER.info("Data refreshed for {}".format(self.str_verbose))
        return self


#
# installation raw data example
#

# {
#     "_id": "60f5cb...",
#     "installation_id": "60f5...",
#     "location_id": "60f54...",
#     "location_text": {
#         "city": {
#             "de": "Bouches-du-Rhône",
#             "en": "Bouches-du-Rhône",
#             "es": "Bouches-du-Rhône",
#             "fr": "Bouches-du-Rhône",
#             "it": "Bouches-du-Rhône",
#             "pt": "Bouches-du-Rhône"
#         },
#         "country": {
#             "de": "Frankreich",
#             "en": "France",
#             "es": "Francia",
#             "fr": "France",
#             "it": "Francia",
#             "pt": "França"
#         }
#     },
#     "name": "Maison",
#     "ws_ids": [
#         "AA:BB:CC:DD:EE:FF"
#     ],
#     "access_type": "admin",
#     "color": 2
# }
