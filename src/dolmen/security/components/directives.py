# -*- coding: utf-8 -*-

import martian
import martian.util
import martian.error
from grokcore.component import name, title, description
from grokcore.security import Permission


class permissions(martian.Directive):
    """This directive is used inside of a `Role` component to list the
    permissions which each member of the role should always possess.
    Note that permissions should be passed as strings, and that several
    permissions they can simply be supplied as multiple arguments; there
    is no need to place them inside of a tuple or list::

        class MyRole(Role):
            permissions('page.CreatePage', 'page.EditPage')

    """
    scope = martian.CLASS
    store = martian.ONCE
    default = []

    def validate(self, *values):
        for value in values:
            if martian.util.check_subclass(value, Permission):
                continue
            if martian.util.not_unicode_or_ascii(value):
                raise martian.error.GrokImportError(
                    "You can only pass unicode values, ASCII values, or "
                    "subclasses of grok.Permission to the '%s' directive."
                    % self.name)

    def factory(self, *values):
        permission_ids = []
        for value in values:
            if martian.util.check_subclass(value, Permission):
                permission_ids.append(name.bind().get(value))
            else:
                permission_ids.append(value)
        return permission_ids


__all__ = ['name', 'title', 'description', 'permissions']
