import requests
import json
import logging
import voluptuous as vol
from datetime import timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_CONTRACT_NUMBER = 'contract_number'

DOMAIN = "biznet_info"

DEFAULT_NAME = 'Biznet Info'

SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_CONTRACT_NUMBER): cv.string
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    contract_number = config.get(CONF_CONTRACT_NUMBER)

    add_entities([
        BiznetRemainingLimitSensor(name, contract_number),
        BiznetLimitSensor(name, contract_number),
        BiznetValidUntilSensor(name, contract_number)
    ], True)

class BiznetRemainingLimitSensor(Entity):
    def __init__(self, name, contract_number):
        self._name = f"{name} Remaining Limit"
        self._contract_number = contract_number
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        _LOGGER.info("Retrieve remaining limit data")
        url = f"https://api.biznetnetworks.com/getQuotaInfo?contractNumber={self._contract_number}"
        response = requests.get(url)
        data = response.json()

        if 'contarctNumber' in data:
            main_kuota = data.get('mainKuota', {}).get('mainKuota', {})
            self._state = main_kuota.get('remainingLimit')
            _LOGGER.info(f"Get remaining limit data: {self._state}")
        else:
            _LOGGER.error("Error retrieving remaining limit data from the API")

class BiznetLimitSensor(Entity):
    def __init__(self, name, contract_number):
        self._name = f"{name} Limit"
        self._contract_number = contract_number
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        _LOGGER.info("Retrieve limit data")
        url = f"https://api.biznetnetworks.com/getQuotaInfo?contractNumber={self._contract_number}"
        response = requests.get(url)
        data = response.json()

        if 'contarctNumber' in data:
            main_kuota = data.get('mainKuota', {}).get('mainKuota', {})
            self._state = main_kuota.get('limit')
            _LOGGER.info(f"Get limit data: {self._state}")
        else:
            _LOGGER.error("Error retrieving limit data from the API")

class BiznetValidUntilSensor(Entity):
    def __init__(self, name, contract_number):
        self._name = f"{name} Valid Until"
        self._contract_number = contract_number
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        _LOGGER.info("Retrieve valid until data")
        url = f"https://api.biznetnetworks.com/getQuotaInfo?contractNumber={self._contract_number}"
        response = requests.get(url)
        data = response.json()

        if 'contarctNumber' in data:
            main_kuota = data.get('mainKuota', {}).get('mainKuota', {})
            self._state = main_kuota.get('validUntil')
            _LOGGER.info(f"Get valid until data: {self._state}")
        else:
            _LOGGER.error("Error retrieving valid until data from the API")