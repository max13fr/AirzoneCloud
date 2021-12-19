# AirzoneCloud package

## Submodules

## AirzoneCloud.AirzoneCloud module


### class AirzoneCloud.AirzoneCloud.AirzoneCloud(email: str, password: str, user_agent: Optional[str] = None)
Bases: `object`

Allow to connect to AirzoneCloud API


#### \__init__(email: str, password: str, user_agent: Optional[str] = None)
Initialize API connection


#### property all_devices(: list[Device])
Get all devices from all installations


#### property all_groups(: list[Group])
Get all groups from all installations


#### property installations(: list[Installation])
Get installations list


#### refresh_installations()
Refresh installations

## AirzoneCloud.Device module


### class AirzoneCloud.Device.Device(api: AirzoneCloud, group: Group, data: dict)
Bases: `object`

Manage a AirzoneCloud device (thermostat)


#### \__init__(api: AirzoneCloud, group: Group, data: dict)

#### property all_properties(: dict)

#### property current_humidity(: int)
Return device current humidity in percentage (0-100)


#### property current_temperature(: float)
Return device current temperature in °C


#### property group(: <module 'AirzoneCloud.Group' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/Group.py'>)
Get parent group


#### property id(: str)
Return device id


#### property is_connected(: bool)
Return if the device is online (True) or offline (False)


#### property is_master(: bool)
Return True if the device is a master thermostat (allowed to update the mode of all devices)


#### property is_on(: bool)
Return True if the device is on


#### property max_temperature(: float)
Return device maximal temperature for current mode


#### property min_temperature(: float)
Return device minimal temperature for current mode


#### property mode(: str)
Return device current mode name (stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling)


#### property mode_description(: str)
Return device current mode description (pretty name to display)


#### property mode_generic(: str)
Return device current generic mode (stop | auto | cooling | heating | ventilation | dehumidify | emergency)


#### property mode_id(: int)
Return device current id mode (0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12)


#### property modes_availables(: list[str])
Return device availables modes names list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling, …])


#### property modes_availables_generics(: list[str])
Return device availables modes generics list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency, …])


#### property modes_availables_ids(: list[int])
Return device availables modes list ([0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12, …])


#### property name(: str)
Return device name


#### refresh()
Refresh current device states


#### set_mode(mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1)
Set mode of the device


#### set_temperature(temperature: float, auto_refresh: bool = True, delay_refresh: int = 1)
Set target_temperature for current device (degrees celsius)


#### property step_temperature(: float)
Return device step temperature (minimum increase/decrease step)


#### property str_verbose(: str)
More verbose description of current device


#### property system_number(: str)
Return device system_number


#### property target_temperature(: float)
Return device target temperature for current mode


#### turn_off(auto_refresh: bool = True, delay_refresh: int = 1)
Turn device off


#### turn_on(auto_refresh: bool = True, delay_refresh: int = 1)
Turn device on


#### property type(: str)
Return device type (az_zone┃aidoo)


#### property ws_id(: str)
Return device webserver id (mac address)


#### property zone_number(: str)
Return device zone_number

## AirzoneCloud.Group module


### class AirzoneCloud.Group.Group(api: <module 'AirzoneCloud.AirzoneCloud' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/AirzoneCloud.py'>, installation: <module 'AirzoneCloud.Installation' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/Installation.py'>, data: dict)
Bases: `object`

Manage a AirzoneCloud group


#### \__init__(api: <module 'AirzoneCloud.AirzoneCloud' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/AirzoneCloud.py'>, installation: <module 'AirzoneCloud.Installation' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/Installation.py'>, data: dict)

#### property devices(: list[Device])

#### property id(: str)
Return group id


#### property installation(: <module 'AirzoneCloud.Installation' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/Installation.py'>)
Get parent installation


#### property name(: str)
Return group name


#### refresh_devices()
Refresh all devices of this group


#### set_mode(mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1)
Set mode of the all devices in the group


#### set_temperature(temperature: float, auto_refresh: bool = True, delay_refresh: int = 1)
Set target_temperature for current all devices in the group (in degrees celsius)


#### property str_verbose(: str)
More verbose description of current group


#### turn_off(auto_refresh: bool = True, delay_refresh: int = 1)
Turn off all devices in the group


#### turn_on(auto_refresh: bool = True, delay_refresh: int = 1)
Turn on all devices in the group

## AirzoneCloud.Installation module


### class AirzoneCloud.Installation.Installation(api: <module 'AirzoneCloud.AirzoneCloud' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/AirzoneCloud.py'>, data: dict)
Bases: `object`

Manage a AirzoneCloud installation


#### \__init__(api: <module 'AirzoneCloud.AirzoneCloud' from '/home/max13fr/www/AirzoneCloud/AirzoneCloud/AirzoneCloud.py'>, data: dict)

#### property access_type(: str)
Return installation access_type (admin┃advanced┃basic)


#### property all_devices(: list[Device])
Get all devices from all groups in the current installation


#### property groups(: list[Group])
Get all groups in the current installation


#### property id(: str)
Return installation id


#### property location_id(: str)
Return installation location id


#### property name(: str)
Return installation name


#### refresh_devices()
Refresh all devices of this installation


#### refresh_groups()
Refresh all groups of this installation


#### set_mode(mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1)
Set mode of the all devices in the installation


#### set_temperature(temperature: float, auto_refresh: bool = True, delay_refresh: int = 1)
Set target_temperature for current all devices in the installation (in degrees celsius)


#### property str_verbose(: str)
More verbose description of current installation


#### turn_off(auto_refresh: bool = True, delay_refresh: int = 1)
Turn off all devices in the installation


#### turn_on(auto_refresh: bool = True, delay_refresh: int = 1)
Turn on all devices in the installation


#### property ws_ids(: str)
Return array of Webserver MAC addresses belonging to the installation

## AirzoneCloud.constants module

## Module contents
