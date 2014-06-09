from setuptools import setup

setup(
    name="pagerglue",
    packages=["pagerglue", "pagerglue.methods"],
    scripts=["pagerglue-worker"],
    version="1.0",
    description="Tool to send short messages over various protocols from a queue.",
    license="ISC",
    author="mutantmonkey",
    author_email="pagerglue@mutantmonkey.in",
    url="https://github.com/mutantmonkey/pagerglue",
    install_requires=["amqp>=1.4.5", "kombu>=3.0.16", "PyYAML>=3.11"],
    extras_require={
        'xmpp': ["sleekxmpp>=1.0"],
        'sms': ["twilio>3.6.0"],
    }
)
