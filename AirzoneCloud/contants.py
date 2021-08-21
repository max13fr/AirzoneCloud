API = "/api/v1"
API_LOGIN = "{}/auth/login".format(API)
API_SITES = "{}/installations".format(API)
API_SYSTEMS = "/systems"
API_ZONES = "{}/devices".format(API)
API_ZONE = "{}/devices".format(API)
API_EVENTS = "/events"

# 2020-04-18: extracted from https://airzonecloud.com/assets/application-506494af86e686bf472b872d02048b42.js

MODES_CONVERTER = {
    "0": {"name": "stop", "description": "Stop"},
    "1": {"name": "cool-air", "description": "Air cooling"},
    "2": {"name": "heat-radiant", "description": "Radiant heating"},
    "3": {"name": "ventilate", "description": "Ventilate"},
    "4": {"name": "heat-air", "description": "Air heating"},
    "5": {"name": "heat-both", "description": "Combined heating"},
    "6": {"name": "dehumidify", "description": "Dry"},
    "7": {"name": "not_exit", "description": ""},
    "8": {"name": "cool-radiant", "description": "Radiant cooling"},
    "9": {"name": "cool-both", "description": "Combined cooling"},
}

SCHEDULE_MODES_CONVERTER = {
    "0": {"name": "", "description": ""},
    "1": {"name": "stop", "description": "Stop"},
    "2": {"name": "ventilate", "description": "Ventilate"},
    "3": {"name": "cool-air", "description": "Air cooling"},
    "4": {"name": "heat-air", "description": "Air heating"},
    "5": {"name": "heat-radiant", "description": "Radiant heating"},
    "6": {"name": "heat-both", "description": "Combined heating"},
    "7": {"name": "dehumidify", "description": "Dry"},
    "8": {"name": "cool-radiant", "description": "Radiant cooling"},
    "9": {"name": "cool-both", "description": "Combined cooling"},
}

VELOCITIES_CONVERTER = {
    "0": {"name": "auto", "description": "Auto"},
    "1": {"name": "velocity-1", "description": "Low speed"},
    "2": {"name": "velocity-2", "description": "Medium speed"},
    "3": {"name": "velocity-3", "description": "High speed"},
}

AIRFLOW_CONVERTER = {
    "0": {"name": "airflow-0", "description": "Silence"},
    "1": {"name": "airflow-1", "description": "Standard"},
    "2": {"name": "airflow-2", "description": "Power"},
}

ECO_CONVERTER = {
    "0": {"name": "eco-off", "description": "Eco off"},
    "1": {"name": "eco-m", "description": "Eco manual"},
    "2": {"name": "eco-a", "description": "Eco A"},
    "3": {"name": "eco-aa", "description": "Eco A+"},
    "4": {"name": "eco-aaa", "description": "Eco A++"},
}

SCENES_CONVERTER = {
    "0": {
        "name": "stop",
        "description": "The air-conditioning system will remain switched off regardless of the demand status of any zone, all the motorized dampers will remain opened",
    },
    "1": {
        "name": "confort",
        "description": "Default and standard user mode. The desired set point temperature can be selected using the predefined temperature ranges",
    },
    "2": {
        "name": "unocupied",
        "description": "To be used when there is no presence detected for short periods of time. A more efficient set point temperature will be set. If the thermostat is activated, the zone will start running in comfort mode",
    },
    "3": {
        "name": "night",
        "description": "The system automatically changes the set point temperature 0.5\xba C/1\xba F every 30 minutes in up to 4 increments of 2\xba C/4\xba F in 2 hours. When cooling, the system increases the set point temperature; when heating, the system decreases the set point temperature",
    },
    "4": {
        "name": "eco",
        "description": "The range of available set point temperatures change for more efficient operation",
    },
    "5": {
        "name": "vacation",
        "description": "This mode feature saves energy while the user is away for extended periods of time",
    },
}
