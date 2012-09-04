from distutils.core import setup
setup(
    name='cura-storage',
    description='Anaconda Storage Provider',
    author='Jan Safranek',
    author_email='jsafrane@redhat.com',
    url='https://fedorahosted.org/cura/',
    version='0.2.1',
    package_dir={'cura.storage': 'providers'},
    packages=['cura.storage', 'cura.storage.wrapper', 'cura.storage.util'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Systems Administration',
        ]
    )
