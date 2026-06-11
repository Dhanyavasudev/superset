# Apache Superset v5.0.0 Multi Authentication Support

## Objective

The objective of this assignment was to enable Apache Superset to support multiple authentication methods simultaneously:

* AUTH_DB
* AUTH_LDAP
* AUTH_OAUTH

By default, Superset supports only one authentication provider through the `AUTH_TYPE` configuration.



## Approach and Plan

To support multiple authentication providers, I introduced a custom security manager and a custom login view.

Instead of using a single `AUTH_TYPE`, I added a new configuration called `AUTH_TYPES` that allows multiple authentication methods to be configured together.

Example:

```python
AUTH_TYPES = [
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
]
```

The solution was designed to extend the existing authentication flow while keeping the default Superset behavior compatible.


## Solution Architecture

```text
User Login
    |
    v
MultiAuthView
    |
    +------------------+
    |                  |
    v                  v
AUTH_DB          AUTH_LDAP
(Database)         (LDAP)
    |
    +------------------+
               |
               v
        Authenticated User
               |
               v
           Superset

OAuth Providers
(Google / Azure / Others)
remain available through
Superset OAuth configuration
```




## Changes Made and Why

### 1. Custom Security Manager

Created:

```text
superset/custom_security_manager.py
```

Why:

* To support multiple authentication providers.
* To introduce the new `AUTH_TYPES` configuration.
* To keep custom logic separate from the default Superset implementation.

### 2. Custom Login View

Added a custom login view.

Why:

* To support authentication against multiple providers.
* To attempt database authentication first.
* To fall back to LDAP authentication when database authentication fails.

### 3. Configuration Changes

Updated `superset_config.py` with:

```python
CUSTOM_SECURITY_MANAGER = MultiAuthSecurityManager

AUTH_TYPES = [
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
]
```

Why:

* To register the custom security manager.
* To allow multiple authentication methods in a single deployment.



## Authentication Flow

1. User enters username and password.
2. Database authentication is attempted.
3. If database authentication fails, LDAP authentication is attempted.
4. If authentication succeeds, the user is logged in.
5. OAuth authentication remains available through Superset OAuth configuration.



## Trade-offs and Considerations

* Authentication providers are checked sequentially.
* Additional authentication checks may slightly increase login time.
* Existing Superset authentication configurations remain compatible.
* OAuth integration can be extended further with a dedicated provider selection UI.


## Summary

This solution extends Apache Superset authentication by introducing support for multiple authentication providers while maintaining compatibility with the existing authentication framework. The implementation uses a custom security manager, a custom login view, and a new `AUTH_TYPES` configuration to support multiple authentication methods within the same deployment.
