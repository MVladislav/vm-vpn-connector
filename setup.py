from setuptools import find_packages, setup


def read_requirements():
    with open("requirements.txt") as req:
        requirements = req.read().split("\n")
    return requirements


setup(
    name="vm_vpn_connector",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        vm_vpn_connector=vm_vpn_connector.main.cli:cli
    """,
)
