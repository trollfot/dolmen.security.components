# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version = '0.1a1'
readme = open('README.txt').read()
history = open(os.path.join("docs", "HISTORY.txt")).read()

install_requires = [
    'grokcore.component',
    'grokcore.security',
    'martian',
    'setuptools',
    'zope.component',
    'zope.i18nmessageid',
    'zope.securitypolicy',
    ]

tests_require = [
    'pytest',
    'zope.testing',
    ]

setup(name='dolmen.security.components',
      version=version,
      description="Security related components for Dolmen.",
      long_description=readme + "\n\n" + history,
      classifiers=[
          "Programming Language :: Python",
          ],
      keywords='Dolmen security',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://www.dolmen-project.org',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.security'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
