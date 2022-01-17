from setuptools import setup, find_packages

setup(
    name="continuous_security_account_setup",
    version="0.0.1",
    description="Account setup for the Continuous Security project",
    author="Eric Kascic",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "create_org=continuous_security_account_setup.create_org:main"
        ],
    },
    install_requires=["boto3", "polling2"],
)
