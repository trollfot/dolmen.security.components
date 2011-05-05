# -*- coding: utf-8 -*-

from zope.securitypolicy.role import Role as securitypolicy_Role


class Role(securitypolicy_Role):
    """Base class for roles in Grok applications.

    A role is a description of a class of users that gives them a
    machine-readable name, a human-readable title, and a set of
    permissions which users belong to that role should possess::

        class Editor(grok.Role):
            grok.name('news.Editor')
            grok.title('Editor')
            grok.permissions('news.EditArticle', 'news.PublishArticle')

    """
