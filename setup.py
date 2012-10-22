from distutils.core import setup
setup(
    name='openlmi-storage',
    description='Anaconda Storage Provider',
    author='Jan Safranek',
    author_email='jsafrane@redhat.com',
    url='https://fedorahosted.org/openlmi/',
    version='0.4.0',
    package_dir={'openlmi.storage': 'providers'},
    packages=['openlmi.storage', 'openlmi.storage.wrapper', 'openlmi.storage.util'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Systems Administration',
        ]
    )
