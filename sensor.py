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

DEFAULT_NAME = 'Biznet Info'

SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_CONTRACT_NUMBER): cv.string
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    contract_number = config.get(CONF_CONTRACT_NUMBER)

    add_entities([BiznetQuotaSensor(name, contract_number)], True)

class BiznetQuotaSensor(Entity):
    def __init__(self, name, contract_number):
        self._name = name
        self._contract_number = contract_number
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self._attributes

    @Throttle(SCAN_INTERVAL)
    def update(self):
        url = f"https://api.biznetnetworks.com/getQuotaInfo?contractNumber={self._contract_number}"
        response = requests.get(url)
        data = response.json()

        if 'mainKuota' in data:
            self._state = data['mainKuota']
            self._attributes = data
        else:
            _LOGGER.error("Error retrieving data from the API")

