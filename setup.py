from setuptools import find_packages, setup

from vm_vpn_connector.config import PROJECT, VERSION


def read_requirements():
    with open("requirements.txt") as req:
        requirements = req.read().split("\n")
    return requirements


setup(
    name=f"{PROJECT}",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points=f"""
        [console_scripts]
        {PROJECT}={PROJECT}.cli:cli
    """,
)
