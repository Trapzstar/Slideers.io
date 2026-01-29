#!/usr/bin/env python
"""Test logging and config systems"""

from logger import get_logger
from config import get_config

# Test logging
logger = get_logger('test')
logger.info('Testing logging system')
logger.debug('Debug message')
logger.warning('Warning message')

# Test config
config = get_config()
print(f'\nConfiguration Test:')
print(f'  Language: {config.get("voice.language")}')
print(f'  Debug mode: {config.get("application.debug")}')
print(f'  Timeout: {config.get("voice.listen_timeout")}')

print('\n✓ Both systems working!')
