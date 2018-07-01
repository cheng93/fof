from setuptools import setup

install_requires = [
    "aiohttp",
    "aiopg[sa]",
    "marshmallow",
    "simplejson"
]

setup_requires = [
    "pytest-runner"
]

tests_require = [
    "pytest",
    "pytest-asyncio",
    "pytest-mock",
]

setup(name="fof",
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require)