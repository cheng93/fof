from setuptools import setup

requires = [
    "aiohttp",
    "aiopg[sa]",
    "marshmallow",
    "simplejson"
]

setup(name="fof",
    install_requires=requires)