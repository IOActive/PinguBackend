# ENVIRONMENT = 'local'
ENVIRONMENT = 'development'
# ENVIRONMENT = 'production'

SETTINGS_MODULE = 'PinguBackend.settings.development'

if ENVIRONMENT == 'docker_dev':
    SETTINGS_MODULE = 'PinguBackend.settings.docker_dev'
if ENVIRONMENT == 'docker_prod':
    SETTINGS_MODULE = 'PinguBackend.settings.docker_prod'
if ENVIRONMENT == 'development':
    SETTINGS_MODULE = 'PinguBackend.settings.development'
if ENVIRONMENT == 'production':
    SETTINGS_MODULE = 'PinguBackend.settings.production'
