
from flask import flash, g, redirect, request
from flask_login import login_user

from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.forms import LoginForm_db
from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_LDAP,
)
from flask_appbuilder.security.views import (
    AuthDBView,
    AuthOAuthView,
    expose,
    no_cache,
    get_safe_redirect,
)

from superset.security import SupersetSecurityManager


class MultiAuthView(AuthDBView):
    """
    Custom Login View for Multi Authentication
    """

    @expose("/login/", methods=["GET", "POST"])
    @no_cache
    def login(self):

        if g.user is not None and g.user.is_authenticated:
            return redirect(
                self.appbuilder.get_url_for_index()
            )

        form = LoginForm_db()

        if form.validate_on_submit():

            next_url = get_safe_redirect(
                request.args.get("next", "")
            )

            user = None

            # Try Database Authentication
            if AUTH_DB in self.appbuilder.sm.auth_types:
                user = self.appbuilder.sm.auth_user_db(
                    form.username.data,
                    form.password.data,
                )

            # Try LDAP Authentication
            if (
                not user
                and AUTH_LDAP in self.appbuilder.sm.auth_types
            ):
                user = self.appbuilder.sm.auth_user_ldap(
                    form.username.data,
                    form.password.data,
                )

            if not user:
                flash(
                    as_unicode(
                        self.invalid_login_message
                    ),
                    "warning",
                )

                return redirect(
                    self.appbuilder.get_url_for_login()
                )

            login_user(
                user,
                remember=False,
            )

            return redirect(next_url)

        return self.render_template(
            self.login_template,
            title=self.title,
            form=form,
            appbuilder=self.appbuilder,
        )


class MultiAuthSecurityManager(SupersetSecurityManager):
    """
    Custom Security Manager supporting
    DB + LDAP + OAuth authentication.
    """

    authdbview = MultiAuthView
    authoauthview = AuthOAuthView

    @property
    def auth_types(self):
        return self.appbuilder.get_app.config.get(
            "AUTH_TYPES",
            [self.auth_type],
        )

    def authenticate_user(self, username, password):

        if AUTH_DB in self.auth_types:
            user = self.auth_user_db(
                username,
                password,
            )
            if user:
                return user

        if AUTH_LDAP in self.auth_types:
            user = self.auth_user_ldap(
                username,
                password,
            )
            if user:
                return user

        return None
