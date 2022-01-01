# Table of Contents

* [AirzoneCloud](#AirzoneCloud)
  * [AirzoneCloud](#AirzoneCloud.AirzoneCloud)
    * [\_\_init\_\_](#AirzoneCloud.AirzoneCloud.__init__)
    * [installations](#AirzoneCloud.AirzoneCloud.installations)
    * [all\_groups](#AirzoneCloud.AirzoneCloud.all_groups)
    * [all\_devices](#AirzoneCloud.AirzoneCloud.all_devices)
    * [refresh\_installations](#AirzoneCloud.AirzoneCloud.refresh_installations)
* [Installation](#Installation)
  * [Installation](#Installation.Installation)
    * [str\_verbose](#Installation.Installation.str_verbose)
    * [id](#Installation.Installation.id)
    * [name](#Installation.Installation.name)
    * [access\_type](#Installation.Installation.access_type)
    * [location\_id](#Installation.Installation.location_id)
    * [ws\_ids](#Installation.Installation.ws_ids)
    * [turn\_on](#Installation.Installation.turn_on)
    * [turn\_off](#Installation.Installation.turn_off)
    * [set\_temperature](#Installation.Installation.set_temperature)
    * [set\_mode](#Installation.Installation.set_mode)
    * [groups](#Installation.Installation.groups)
    * [all\_devices](#Installation.Installation.all_devices)
    * [refresh\_groups](#Installation.Installation.refresh_groups)
    * [refresh\_devices](#Installation.Installation.refresh_devices)
* [Group](#Group)
  * [Group](#Group.Group)
    * [str\_verbose](#Group.Group.str_verbose)
    * [all\_properties](#Group.Group.all_properties)
    * [id](#Group.Group.id)
    * [name](#Group.Group.name)
    * [is\_on](#Group.Group.is_on)
    * [mode\_id](#Group.Group.mode_id)
    * [mode](#Group.Group.mode)
    * [mode\_generic](#Group.Group.mode_generic)
    * [mode\_description](#Group.Group.mode_description)
    * [modes\_availables\_ids](#Group.Group.modes_availables_ids)
    * [modes\_availables](#Group.Group.modes_availables)
    * [modes\_availables\_generics](#Group.Group.modes_availables_generics)
    * [turn\_on](#Group.Group.turn_on)
    * [turn\_off](#Group.Group.turn_off)
    * [set\_temperature](#Group.Group.set_temperature)
    * [set\_mode](#Group.Group.set_mode)
    * [installation](#Group.Group.installation)
    * [devices](#Group.Group.devices)
    * [master\_device](#Group.Group.master_device)
    * [refresh\_devices](#Group.Group.refresh_devices)
* [Device](#Device)
  * [Device](#Device.Device)
    * [str\_verbose](#Device.Device.str_verbose)
    * [all\_properties](#Device.Device.all_properties)
    * [id](#Device.Device.id)
    * [name](#Device.Device.name)
    * [type](#Device.Device.type)
    * [ws\_id](#Device.Device.ws_id)
    * [system\_number](#Device.Device.system_number)
    * [zone\_number](#Device.Device.zone_number)
    * [is\_connected](#Device.Device.is_connected)
    * [is\_on](#Device.Device.is_on)
    * [is\_master](#Device.Device.is_master)
    * [mode\_id](#Device.Device.mode_id)
    * [mode](#Device.Device.mode)
    * [mode\_generic](#Device.Device.mode_generic)
    * [mode\_description](#Device.Device.mode_description)
    * [modes\_availables\_ids](#Device.Device.modes_availables_ids)
    * [modes\_availables](#Device.Device.modes_availables)
    * [modes\_availables\_generics](#Device.Device.modes_availables_generics)
    * [current\_temperature](#Device.Device.current_temperature)
    * [current\_humidity](#Device.Device.current_humidity)
    * [target\_temperature](#Device.Device.target_temperature)
    * [min\_temperature](#Device.Device.min_temperature)
    * [max\_temperature](#Device.Device.max_temperature)
    * [step\_temperature](#Device.Device.step_temperature)
    * [turn\_on](#Device.Device.turn_on)
    * [turn\_off](#Device.Device.turn_off)
    * [set\_temperature](#Device.Device.set_temperature)
    * [set\_mode](#Device.Device.set_mode)
    * [group](#Device.Device.group)
    * [refresh](#Device.Device.refresh)

<a id="AirzoneCloud"></a>

# AirzoneCloud

<a id="AirzoneCloud.AirzoneCloud"></a>

## AirzoneCloud Objects

```python
class AirzoneCloud()
```

Allow to connect to AirzoneCloud API

<a id="AirzoneCloud.AirzoneCloud.__init__"></a>

#### \_\_init\_\_

```python
def __init__(email: str, password: str, user_agent: str = None) -> None
```

Initialize API connection

<a id="AirzoneCloud.AirzoneCloud.installations"></a>

#### installations

```python
@property
def installations() -> "list[Installation]"
```

Get installations list

<a id="AirzoneCloud.AirzoneCloud.all_groups"></a>

#### all\_groups

```python
@property
def all_groups() -> "list[Group]"
```

Get all groups from all installations

<a id="AirzoneCloud.AirzoneCloud.all_devices"></a>

#### all\_devices

```python
@property
def all_devices() -> "list[Device]"
```

Get all devices from all installations

<a id="AirzoneCloud.AirzoneCloud.refresh_installations"></a>

#### refresh\_installations

```python
def refresh_installations() -> "AirzoneCloud"
```

Refresh installations

<a id="Installation"></a>

# Installation

<a id="Installation.Installation"></a>

## Installation Objects

```python
class Installation()
```

Manage a AirzoneCloud installation

<a id="Installation.Installation.str_verbose"></a>

#### str\_verbose

```python
@property
def str_verbose() -> str
```

More verbose description of current installation

<a id="Installation.Installation.id"></a>

#### id

```python
@property
def id() -> str
```

Return installation id

<a id="Installation.Installation.name"></a>

#### name

```python
@property
def name() -> str
```

Return installation name

<a id="Installation.Installation.access_type"></a>

#### access\_type

```python
@property
def access_type() -> str
```

Return installation access_type (admin┃advanced┃basic)

<a id="Installation.Installation.location_id"></a>

#### location\_id

```python
@property
def location_id() -> str
```

Return installation location id

<a id="Installation.Installation.ws_ids"></a>

#### ws\_ids

```python
@property
def ws_ids() -> str
```

Return array of Webserver MAC addresses belonging to the installation

<a id="Installation.Installation.turn_on"></a>

#### turn\_on

```python
def turn_on(auto_refresh: bool = True, delay_refresh: int = 1) -> "Installation"
```

Turn on all devices in the installation

<a id="Installation.Installation.turn_off"></a>

#### turn\_off

```python
def turn_off(auto_refresh: bool = True, delay_refresh: int = 1) -> "Installation"
```

Turn off all devices in the installation

<a id="Installation.Installation.set_temperature"></a>

#### set\_temperature

```python
def set_temperature(temperature: float, auto_refresh: bool = True, delay_refresh: int = 1) -> "Installation"
```

Set target_temperature for current all devices in the installation (in degrees celsius)

<a id="Installation.Installation.set_mode"></a>

#### set\_mode

```python
def set_mode(mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1) -> "Installation"
```

Set mode of the all devices in the installation

<a id="Installation.Installation.groups"></a>

#### groups

```python
@property
def groups() -> "list[Group]"
```

Get all groups in the current installation

<a id="Installation.Installation.all_devices"></a>

#### all\_devices

```python
@property
def all_devices() -> "list[Device]"
```

Get all devices from all groups in the current installation

<a id="Installation.Installation.refresh_groups"></a>

#### refresh\_groups

```python
def refresh_groups() -> "Installation"
```

Refresh all groups of this installation

<a id="Installation.Installation.refresh_devices"></a>

#### refresh\_devices

```python
def refresh_devices() -> "Installation"
```

Refresh all devices of this installation

<a id="Group"></a>

# Group

<a id="Group.Group"></a>

## Group Objects

```python
class Group()
```

Manage a AirzoneCloud group

<a id="Group.Group.str_verbose"></a>

#### str\_verbose

```python
@property
def str_verbose() -> str
```

More verbose description of current group

<a id="Group.Group.all_properties"></a>

#### all\_properties

```python
@property
def all_properties() -> dict
```

Return all group properties values

<a id="Group.Group.id"></a>

#### id

```python
@property
def id() -> str
```

Return group id

<a id="Group.Group.name"></a>

#### name

```python
@property
def name() -> str
```

Return group name

<a id="Group.Group.is_on"></a>

#### is\_on

```python
@property
def is_on() -> bool
```

Return True if at least one device is on in the group

<a id="Group.Group.mode_id"></a>

#### mode\_id

```python
@property
def mode_id() -> int
```

Return group current id mode (0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12)

<a id="Group.Group.mode"></a>

#### mode

```python
@property
def mode() -> str
```

Return group current mode name (stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling)

<a id="Group.Group.mode_generic"></a>

#### mode\_generic

```python
@property
def mode_generic() -> str
```

Return group current generic mode (stop | auto | cooling | heating | ventilation | dehumidify | emergency)

<a id="Group.Group.mode_description"></a>

#### mode\_description

```python
@property
def mode_description() -> str
```

Return group current mode description (pretty name to display)

<a id="Group.Group.modes_availables_ids"></a>

#### modes\_availables\_ids

```python
@property
def modes_availables_ids() -> "list[int]"
```

Return group availables modes list ([0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12, ...])

<a id="Group.Group.modes_availables"></a>

#### modes\_availables

```python
@property
def modes_availables() -> "list[str]"
```

Return group availables modes names list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling, ...])

<a id="Group.Group.modes_availables_generics"></a>

#### modes\_availables\_generics

```python
@property
def modes_availables_generics() -> "list[str]"
```

Return group availables modes generics list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency, ...])

<a id="Group.Group.turn_on"></a>

#### turn\_on

```python
def turn_on(auto_refresh: bool = True, delay_refresh: int = 1) -> "Group"
```

Turn on all devices in the group

<a id="Group.Group.turn_off"></a>

#### turn\_off

```python
def turn_off(auto_refresh: bool = True, delay_refresh: int = 1) -> "Group"
```

Turn off all devices in the group

<a id="Group.Group.set_temperature"></a>

#### set\_temperature

```python
def set_temperature(temperature: float, auto_refresh: bool = True, delay_refresh: int = 1) -> "Group"
```

Set target_temperature for current all devices in the group (in degrees celsius)

<a id="Group.Group.set_mode"></a>

#### set\_mode

```python
def set_mode(mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1) -> "Group"
```

Set mode of the all devices in the group

<a id="Group.Group.installation"></a>

#### installation

```python
@property
def installation() -> Installation
```

Get parent installation

<a id="Group.Group.devices"></a>

#### devices

```python
@property
def devices() -> "list[Device]"
```

Return all devices in this group

<a id="Group.Group.master_device"></a>

#### master\_device

```python
@property
def master_device() -> "Device"
```

Return master device in this group (only device allowed to change mode)

<a id="Group.Group.refresh_devices"></a>

#### refresh\_devices

```python
def refresh_devices() -> "Group"
```

Refresh all devices of this group

<a id="Device"></a>

# Device

<a id="Device.Device"></a>

## Device Objects

```python
class Device()
```

Manage a AirzoneCloud device (thermostat)

<a id="Device.Device.str_verbose"></a>

#### str\_verbose

```python
@property
def str_verbose() -> str
```

More verbose description of current device

<a id="Device.Device.all_properties"></a>

#### all\_properties

```python
@property
def all_properties() -> dict
```

Return all group properties values

<a id="Device.Device.id"></a>

#### id

```python
@property
def id() -> str
```

Return device id

<a id="Device.Device.name"></a>

#### name

```python
@property
def name() -> str
```

Return device name

<a id="Device.Device.type"></a>

#### type

```python
@property
def type() -> str
```

Return device type (az_zone┃aidoo)

<a id="Device.Device.ws_id"></a>

#### ws\_id

```python
@property
def ws_id() -> str
```

Return device webserver id (mac address)

<a id="Device.Device.system_number"></a>

#### system\_number

```python
@property
def system_number() -> str
```

Return device system_number

<a id="Device.Device.zone_number"></a>

#### zone\_number

```python
@property
def zone_number() -> str
```

Return device zone_number

<a id="Device.Device.is_connected"></a>

#### is\_connected

```python
@property
def is_connected() -> bool
```

Return if the device is online (True) or offline (False)

<a id="Device.Device.is_on"></a>

#### is\_on

```python
@property
def is_on() -> bool
```

Return True if the device is on

<a id="Device.Device.is_master"></a>

#### is\_master

```python
@property
def is_master() -> bool
```

Return True if the device is a master thermostat (allowed to update the mode of all devices)

<a id="Device.Device.mode_id"></a>

#### mode\_id

```python
@property
def mode_id() -> int
```

Return device current id mode (0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12)

<a id="Device.Device.mode"></a>

#### mode

```python
@property
def mode() -> str
```

Return device current mode name (stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling)

<a id="Device.Device.mode_generic"></a>

#### mode\_generic

```python
@property
def mode_generic() -> str
```

Return device current generic mode (stop | auto | cooling | heating | ventilation | dehumidify | emergency)

<a id="Device.Device.mode_description"></a>

#### mode\_description

```python
@property
def mode_description() -> str
```

Return device current mode description (pretty name to display)

<a id="Device.Device.modes_availables_ids"></a>

#### modes\_availables\_ids

```python
@property
def modes_availables_ids() -> "list[int]"
```

Return device availables modes list ([0┃1┃2┃3┃4┃5┃6┃7┃8┃9┃10┃11┃12, ...])

<a id="Device.Device.modes_availables"></a>

#### modes\_availables

```python
@property
def modes_availables() -> "list[str]"
```

Return device availables modes names list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency-heating | air-heating | radiant-heating | combined-heating | air-cooling | radiant-cooling | combined-cooling, ...])

<a id="Device.Device.modes_availables_generics"></a>

#### modes\_availables\_generics

```python
@property
def modes_availables_generics() -> "list[str]"
```

Return device availables modes generics list ([stop | auto | cooling | heating | ventilation | dehumidify | emergency, ...])

<a id="Device.Device.current_temperature"></a>

#### current\_temperature

```python
@property
def current_temperature() -> float
```

Return device current temperature in °C

<a id="Device.Device.current_humidity"></a>

#### current\_humidity

```python
@property
def current_humidity() -> int
```

Return device current humidity in percentage (0-100)

<a id="Device.Device.target_temperature"></a>

#### target\_temperature

```python
@property
def target_temperature() -> float
```

Return device target temperature for current mode

<a id="Device.Device.min_temperature"></a>

#### min\_temperature

```python
@property
def min_temperature() -> float
```

Return device minimal temperature for current mode

<a id="Device.Device.max_temperature"></a>

#### max\_temperature

```python
@property
def max_temperature() -> float
```

Return device maximal temperature for current mode

<a id="Device.Device.step_temperature"></a>

#### step\_temperature

```python
@property
def step_temperature() -> float
```

Return device step temperature (minimum increase/decrease step)

<a id="Device.Device.turn_on"></a>

#### turn\_on

```python
def turn_on(auto_refresh: bool = True, delay_refresh: int = 1) -> "Device"
```

Turn device on

<a id="Device.Device.turn_off"></a>

#### turn\_off

```python
def turn_off(auto_refresh: bool = True, delay_refresh: int = 1) -> "Device"
```

Turn device off

<a id="Device.Device.set_temperature"></a>

#### set\_temperature

```python
def set_temperature(temperature: float, auto_refresh: bool = True, delay_refresh: int = 1) -> "Device"
```

Set target_temperature for current device (degrees celsius)

<a id="Device.Device.set_mode"></a>

#### set\_mode

```python
def set_mode(mode_name: str, auto_refresh: bool = True, delay_refresh: int = 1) -> "Device"
```

Set mode of the device

<a id="Device.Device.group"></a>

#### group

```python
@property
def group() -> Group
```

Get parent group

<a id="Device.Device.refresh"></a>

#### refresh

```python
def refresh() -> "Device"
```

Refresh current device states

