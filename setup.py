from setuptools import setup, find_packages
import os
import os.path

version = '1.0.0'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = read('README.txt') + '\n\n' + read('docs', 'HISTORY.txt')

setup(
    name='rbco.wfdocumentator',
    version=version,
    description='An add-on for Zope and Plone which aims to provide '
    'user-friendly automatically generated documentation about workflow '
    'definitions.',
    long_description=long_description,
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone workflow',
    author='Rafael Oliveira',
    author_email='rafaelbco@gmail.com',
    url='https://github.com/rafaelbco/rbco.wfdocumentator',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['rbco'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'rbco.commandwrap<=0.0.99',
        'prdg.util<=0.0.99',
    ],
    extras_require={
        'test': [
        ]
    },
    entry_points='''
    [z3c.autoinclude.plugin]
    target = plone
    ''',
)
