from setuptools import setup

requires = [
    "aiohttp",
    "aiopg[sa]"
]

setup(name="fof",
    install_requires=requires)