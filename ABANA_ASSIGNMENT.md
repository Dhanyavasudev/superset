# Apache Superset v5.0.0 Multi Authentication Support

## Objective

The objective of this assignment was to extend Apache Superset v5.0.0 to support multiple authentication methods simultaneously:

* AUTH_DB
* AUTH_LDAP
* AUTH_OAUTH

By default, Apache Superset supports only a single authentication backend through the `AUTH_TYPE` configuration. The goal of this implementation was to allow multiple authentication providers to coexist within the same deployment while preserving compatibility with the existing Superset authentication framework.

---

## Approach and Plan

To support multiple authentication methods, a custom security manager and a custom login view were introduced.

Instead of relying on a single `AUTH_TYPE`, a new configuration named `AUTH_TYPES` was implemented to allow multiple authentication backends to be configured simultaneously.

Example:

```python
AUTH_TYPES = [
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
]
```

The solution was designed to minimize changes to the existing Superset authentication architecture while extending its functionality.

---

## Solution Architecture

```text
User Login
    |
    v
MultiAuthView
    |
    +--------------------+
    |                    |
    v                    v
 AUTH_DB            AUTH_LDAP
(Database)            (LDAP)
    |
    +--------------------+
             |
             v
      Authenticated User
             |
             v
          Superset

OAuth Providers
(Google / Azure / GitHub / Others)
remain available through
Superset OAuth configuration
```

---

## Changes Made and Why

### 1. Custom Security Manager

Created:

```text
superset/custom_security_manager.py
```

Purpose:

* Introduced support for multiple authentication providers.
* Added support for the new `AUTH_TYPES` configuration.
* Kept authentication customization separate from the core Superset codebase.

---

### 2. Custom Login View

Implemented a custom login view that extends Superset's existing authentication flow.

Purpose:

* Authenticate users against multiple providers.
* Attempt database authentication first.
* Fall back to LDAP authentication when database authentication fails.
* Maintain compatibility with existing login functionality.

---

### 3. Configuration Changes

Updated `superset_config.py`:

```python
CUSTOM_SECURITY_MANAGER = MultiAuthSecurityManager

AUTH_TYPES = [
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
]
```

Purpose:

* Register the custom security manager.
* Enable multiple authentication providers within a single deployment.

---

### 4. OAuth Support

OAuth authentication support was preserved by registering Superset's existing OAuth authentication view within the custom security manager.

```python
authoauthview = AuthOAuthView
```

Purpose:

* Retain compatibility with Superset's native OAuth authentication mechanism.
* Allow integration with OAuth providers such as Google, Azure AD, GitHub, and other supported providers.
* Avoid modifying the existing OAuth authentication flow.

OAuth providers can be configured using Superset's standard `OAUTH_PROVIDERS` configuration.

---

## Authentication Flow

1. User enters username and password.
2. Database authentication is attempted first.
3. If database authentication fails, LDAP authentication is attempted.
4. If authentication succeeds, the user is logged in.
5. OAuth authentication remains available through Superset's existing OAuth configuration and authentication views.

---

## Modified Files

```text
superset/custom_security_manager.py
superset_config.py
ABANA_ASSIGNMENT.md
```

---

## Trade-offs and Considerations

* Authentication providers are evaluated sequentially.
* Multiple authentication checks may introduce a small increase in login response time.
* Existing Superset authentication configurations remain compatible.
* OAuth provider selection can be enhanced further through a dedicated login interface.
* LDAP authentication requires access to an external LDAP server for complete validation.
* OAuth authentication requires valid provider credentials (Google, Azure AD, GitHub, etc.) for end-to-end testing.
* The implementation supports OAuth through Superset's native OAuth framework, but external OAuth providers were not configured in the local development environment.
* The solution prioritizes minimal changes to the existing Superset architecture to simplify maintenance and future upgrades.

---

## Testing

### Test Case 1 – Database Authentication

* Authentication Type: AUTH_DB
* Expected Result: Successful login with valid database credentials.
* Result: Passed

### Test Case 2 – LDAP Authentication

* Authentication Type: AUTH_LDAP
* Expected Result: Successful login when valid LDAP credentials are provided.
* Result: Logic Implemented

### Test Case 3 – Invalid Credentials

* Authentication Type: AUTH_DB / AUTH_LDAP
* Expected Result: Authentication failure and login rejection.
* Result: Passed

### Test Case 4 – OAuth Authentication

* Authentication Type: AUTH_OAUTH
* Expected Result: Authentication through configured OAuth provider.
* Result: Configuration Support Implemented (Provider credentials not available for local validation)

---

## Summary

This implementation extends Apache Superset v5.0.0 to support multiple authentication methods simultaneously while preserving compatibility with the existing authentication framework.

The solution introduces a custom security manager, a custom login view, and a new `AUTH_TYPES` configuration to support database authentication, LDAP authentication, and OAuth authentication within the same deployment.

The implementation maintains Superset's native OAuth functionality through `AuthOAuthView` while providing flexible multi-authentication support with minimal impact on the existing codebase.
