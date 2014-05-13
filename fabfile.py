from __future__ import unicode_literals

from fabric.operations import local


def test():
    local("python manage.py test")


def publish():
    test()
    local("python setup.py publish")
