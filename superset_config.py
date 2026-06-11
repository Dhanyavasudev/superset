SECRET_KEY = "Dhanya@123456789_SUPERSET_ASSIGNMENT_SECRET_KEY"

from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
)

from superset.custom_security_manager import MultiAuthSecurityManager

CUSTOM_SECURITY_MANAGER = MultiAuthSecurityManager

AUTH_TYPES = [
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
] 