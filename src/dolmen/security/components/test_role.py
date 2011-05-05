# -*- coding: utf-8 -*-

import pytest
import martian.error
from dolmen.security import components
from grokcore.component import testing
from zope.testing.cleanup import cleanUp
from zope.component import getUtility
from zope.securitypolicy.interfaces import IRole


def setup_module(module):
    testing.grok("dolmen.security.components.meta")


def teardown_module(module):
    cleanUp()


def test_no_name():
    """A role has to have a name to be defined.
    """
    class MissingName(components.Role):
        pass

    with pytest.raises(martian.error.GrokError):
        testing.grok_component('fail', MissingName)


def test_naming():

    class SomeName(components.Role):
        components.name('SomeName')

    assert components.name.bind().get(SomeName) == 'SomeName'


def test_registration():

    class MyRole(components.Role):
        components.name('SomeSillyRole')

    assert testing.grok_component('myrole', MyRole) == True

    role = getUtility(IRole, name='SomeSillyRole')
    assert isinstance(role, MyRole) is True


def test_permission_failure():

    class NotAPermissionSubclass(object):
        components.name('not really a permission')

    with pytest.raises(martian.error.GrokImportError) as error:
        class MyRole(components.Role):
            components.name('MyRole')
            components.permissions(NotAPermissionSubclass)

    assert str(error.value) == (
        "You can only pass unicode values, ASCII values, or subclasses"
        " of `Permission` to the 'permissions' directive.")


def test_permission():
    """A Role component optionally defines what permission it comprises.
    The `permissions` directive is used to specify the set of permissions
    that are aggregated in the particular Role. The permissions can be
    referenced by name or by class.
    """
    class FirstPermission(components.Permission):
        components.name('first permission')

    class SecondPermission(components.Permission):
        components.name('second permission')

    class RolePermissionsByName(components.Role):
        components.name('ByName')
        components.permissions(
            'first permission',
            'second permission')

    class RolePermissionsByClass(components.Role):
        components.name('ByClass')
        components.permissions(
            FirstPermission,
            SecondPermission)

    assert components.permissions.bind().get(RolePermissionsByName) == [
        'first permission', 'second permission']

    assert components.permissions.bind().get(RolePermissionsByClass) == [
        'first permission', 'second permission']

    assert (components.permissions.bind().get(RolePermissionsByName) ==
            components.permissions.bind().get(RolePermissionsByClass))
