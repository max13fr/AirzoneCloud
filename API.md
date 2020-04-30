# AirzoneCloud package

## Submodules

## AirzoneCloud.AirzoneCloud module


### class AirzoneCloud.AirzoneCloud.AirzoneCloud(username, password, user_agent=None, base_url=None)
Bases: `object`

Allow to connect to AirzoneCloud API


#### \__init__(username, password, user_agent=None, base_url=None)
Initialize API connection


#### property all_zones()
Get all zones from all devices (same order as in app)


#### property devices()
Get devices list (same order as in app)


#### refresh_devices()
Refresh devices

## AirzoneCloud.Device module


### class AirzoneCloud.Device.Device(api, data)
Bases: `object`

Manage a AirzoneCloud device


#### \__init__(api, data)
Initialize self.  See help(type(self)) for accurate signature.


#### property firmware_ws()
Return webserver device


#### property has_airflow()

#### property has_eco()

#### property has_farenheit()

#### property has_velocity()

#### property id()
Return device id


#### property location()
Return device location


#### property mac()
Return device mac


#### property name()
Return device name


#### property pin()
Return device pin code


#### refresh(refresh_systems=True)
Refresh current device data (call refresh_devices on parent AirzoneCloud)


#### refresh_systems()
Refresh all systems of this device


#### property status()
Return device status


#### property str_complete()

#### property sync_datetime()
Return True if device datetime is sync with AirzoneCloud


#### property systems()

#### property target_temperature()
Return device target temperature

## AirzoneCloud.System module


### class AirzoneCloud.System.System(api, device, data)
Bases: `object`

Manage a AirzoneCloud system


#### \__init__(api, device, data)
Initialize self.  See help(type(self)) for accurate signature.


#### property airflow()

#### property airflow_description()

#### property airflow_raw()

#### property device()
Get parent device


#### property device_id()

#### property eco()

#### property eco_description()

#### property eco_raw()

#### property firmware_system()

#### property firmware_ws()

#### property has_airflow()

#### property has_velocity()

#### property id()

#### property max_temp()

#### property min_temp()

#### property mode()

#### property mode_description()

#### property mode_raw()

#### property name()

#### refresh(refresh_zones=True)
Refresh current system data (call refresh_systems on parent device)


#### refresh_zones()
Refresh all zones of this system


#### set_mode(mode_name)
Set mode of the system


#### property str_complete()

#### property system_number()

#### property velocity()

#### property velocity_description()

#### property velocity_raw()

#### property zones()
Get all zones in this system

## AirzoneCloud.Zone module


### class AirzoneCloud.Zone.Zone(api, system, data)
Bases: `object`

Manage a Airzonecloud zone


#### \__init__(api, system, data)
Initialize self.  See help(type(self)) for accurate signature.


#### property current_humidity()

#### property current_temperature()

#### property device_id()

#### property id()

#### property is_on()

#### property max_temp()

#### property min_temp()

#### property mode()

#### property mode_description()

#### property mode_raw()

#### property name()

#### refresh()
Refresh current zone data (call refresh_zones on parent system)


#### set_temperature(temperature)
Set target_temperature for this zone


#### property str_complete()

#### property system()
Get parent system


#### property system_number()

#### property target_temperature()

#### turn_off()
Turn zone off


#### turn_on()
Turn zone on


#### property zone_number()
## AirzoneCloud.contants module

## Module contents
