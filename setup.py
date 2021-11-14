'''
    will setup the project, by install it local
    with needed dependencies
'''
import os
from subprocess import check_call

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

try:
    from dotenv import load_dotenv
    load_dotenv('.env_project')
except ImportError:
    import logging
    import sys

    source_to_install = 'python-dotenv'
    logging.log(logging.CRITICAL, f'Failed to Import {source_to_install}')
    logging.log(logging.INFO, f'Attempting to Install {source_to_install}')
    try:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '-q', source_to_install])
        from dotenv import load_dotenv
        load_dotenv('.env_project')
        logging.log(logging.INFO, '[DONE]')
    except Exception:
        logging.log(logging.CRITICAL, '[FAIL]')

PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'vm_vpn_connector')
VERSION: str = os.getenv('VERSION', '0.0.1')
SCRIPT_INST: bool = os.getenv('VM_SCRIPT_INST', False)


def main():
    PROJECT_NAME_SLUG = slugify(PROJECT_NAME)
    setup(
        # name=PROJECT_NAME,
        # version=VERSION,
        # license='GNU AGPLv3',
        # description=PROJECT_NAME,
        # long_description=read_long_description(),
        # long_description_content_type='text/markdown',
        # author='MVladislav',
        # author_email='info@mvladislav.online',
        # packages=find_packages(),
        # data_files=[('', ['requirements.txt', 'scripts/setup.sh', 'scripts/setup-dev.sh'])],
        # include_package_data=True,
        cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },
        install_requires=read_requirements(),
        # python_requires='>=3.8',
        # zip_safe=True,
        entry_points=f'''
            [console_scripts]
            {PROJECT_NAME_SLUG}=app.main:cli
        ''',
    )

# ------------------------------------------------------------------------------
#
# POST installer
#
# ------------------------------------------------------------------------------


class PostDevelopCommand(develop):
    '''
        Post-installation for development mode.
    '''

    def run(self):
        if SCRIPT_INST:
            check_call(['/bin/bash', './scripts/setup-dev.sh'])
        develop.run(self)


class PostInstallCommand(install):
    '''
        Post-installation for installation mode.
    '''

    def run(self):
        if SCRIPT_INST:
            check_call(['/bin/bash', './scripts/setup.sh'])
        install.run(self)

# ------------------------------------------------------------------------------
#
# TEXTs and requirements
#
# ------------------------------------------------------------------------------


def read_long_description():
    '''
        load the readme to add as long description
    '''
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
    return long_description


def read_requirements():
    '''
        load and read the dependencies
        from the requirements.txt file
        and return them as a list
    '''
    with open('requirements.txt', 'r', encoding='utf-8') as req:
        requirements = req.read().split('\n')
    return requirements

# ------------------------------------------------------------------------------
#
# HELPER
#
# ------------------------------------------------------------------------------


def slugify(value, allow_unicode=False):
    import re
    import unicodedata

    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[-\s]+', '-', re.sub(r'[^\w\s-]', '', value.lower())).strip('-_')

# ------------------------------------------------------------------------------
#
# SETUP
#
# ------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
