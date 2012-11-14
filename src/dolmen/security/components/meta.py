# -*- coding: utf-8 -*-

import martian
from martian.error import GrokError

from dolmen.security.components import Role
from dolmen.security.components import directives
from grokcore.security.meta.permission import PermissionGrokker

from zope.i18nmessageid import Message
from zope.component import provideUtility
from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.rolepermission import rolePermissionManager


def fallback_to_name(factory, module, name, **data):
    return name


class RoleGrokker(martian.ClassGrokker):
    """Grokker for components subclassed from `grok.Role`.

    Each role is registered as a global utility providing the service
    `IRole` under its own particular name, and then granted every
    permission named in its `grok.permission()` directive.

    """
    martian.component(Role)
    martian.priority(martian.priority.bind().get(PermissionGrokker()) - 1)
    martian.directive(directives.name)
    martian.directive(directives.title, get_default=fallback_to_name)
    martian.directive(directives.description)
    martian.directive(directives.permissions)

    def execute(self, factory, config, name, title, description,
                permissions, **kw):
        if not name:
            raise GrokError(
                "A role needs to have a dotted name for its id. Use "
                "grok.name to specify one.", factory)

        # We can safely convert to unicode, since the directives makes sure
        # it is either unicode already or ASCII.
        if not isinstance(title, Message):
            title = unicode(title)

        if not isinstance(description, Message):
            description = unicode(description)

        role = factory(unicode(name), title, description)

        config.action(
            discriminator=('utility', IRole, name),
            callable=provideUtility, args=(role, IRole, name))

        for permission in permissions:
            config.action(
                discriminator=('grantPermissionToRole', permission, name),
                callable=rolePermissionManager.grantPermissionToRole,
                args=(permission, name))
        return True
