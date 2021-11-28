# AirzoneCloudDaikin package

## Submodules

## AirzoneCloudDaikin.AirzoneCloudDaikin module


### class AirzoneCloudDaikin.AirzoneCloudDaikin.AirzoneCloudDaikin(username, password, user_agent=None, base_url=None)
Bases: `object`

Allow to connect to AirzoneCloudDaikin API


#### \__init__(username, password, user_agent=None, base_url=None)
Initialize API connection


#### property all_devices()
Get all devices from all installations (same order as in app)


#### property installations()
Get installations list (same order as in app)


#### refresh_installations()
Refresh installations

## AirzoneCloudDaikin.Device module


### class AirzoneCloudDaikin.Device.Device(api, installation, data)
Bases: `object`

Manage a AirzoneCloudDaikin device


#### \__init__(api, installation, data)
Initialize self.  See help(type(self)) for accurate signature.


#### ask_airzone_update()
Ask an update to the airzone hardware (airzone cloud don’t autopull data like current temperature)
The update should be available in airzone cloud after 3 to 10 secs in average


#### property brand()
Return webserver brand


#### property current_temperature()
Return device current temperature


#### property firmware()
Return webserver firmware


#### property heat_cold_mode()
Return device current heat/cold mode


#### property id()
Return device id


#### property installation()
Get parent installation


#### property is_on()

#### property mac()
Return device mac


#### property max_temperature()
Return device maximal temperature


#### property max_temperature_cold()
Return device max temperature limit in cold mode


#### property max_temperature_heat()
Return device max temperature limit in heat mode


#### property min_temperature()
Return device minimal temperature


#### property min_temperature_cold()
Return device min temperature limit in cold mode


#### property min_temperature_heat()
Return device min temperature limit in heat mode


#### property mode()
Return device current mode name


#### property mode_description()
Return device current mode description


#### property mode_raw()
Return device current raw mode (from API)


#### property name()
Return device name


#### property pin()
Return device pin code


#### refresh()
Refresh current device data (call refresh_devices on parent AirzoneCloudDaikin)


#### set_mode(mode_name)
Set mode of the device


#### set_temperature(temperature)
Set target_temperature for current heat/cold mode on this device


#### property status()
Return device status


#### property str_complete()

#### property target_temperature()
Return device target temperature


#### property target_temperature_cold()
Return device target temperature in cold mode


#### property target_temperature_heat()
Return device target temperature in heat mode


#### turn_off()
Turn device off


#### turn_on()
Turn device on

## AirzoneCloudDaikin.Installation module


### class AirzoneCloudDaikin.Installation.Installation(api, data)
Bases: `object`

Manage a Daikin AirzoneCloud installation


#### \__init__(api, data)
Initialize self.  See help(type(self)) for accurate signature.


#### property devices()

#### property gps_location()
Return installation gps location : { latitude: …, longitude: … }


#### property id()
Return installation id


#### property location()
Return installation location


#### property name()
Return installation name


#### refresh(refresh_devices=True)
Refresh current installation data (call refresh_installations on parent AirzoneCloudDaikin)


#### refresh_devices()
Refresh all devices of this installation


#### property scenary()
Return installation scenary


#### property str_complete()

#### property time_zone()
Return the timezone


#### property type()
Return installation type

## AirzoneCloudDaikin.contants module

## Module contents
