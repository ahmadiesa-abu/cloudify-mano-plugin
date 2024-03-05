from setuptools import setup

setup(
    name='cloudify-mano-plugin',
    version='0.1.0',
    packages=[
        'mano_plugin',
        'mano_sdk'
    ],
    zip_safe=False,
    install_requires=[
        "cloudify-common==6.4.0",
        "requests",
        "xmltodict"
    ],
    test_requires=[]
)