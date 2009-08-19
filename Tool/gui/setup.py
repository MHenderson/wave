from setuptools import setup, find_packages

setup(
    name = "Wave",
    version = "0.0.1",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    entry_points = 
    {
        'gui_scripts': 
        [
            'wavegui = Wave.wavegui:main'
        ]
    },
    install_requires = 
    [
	'sphinx >= 0.6.2',
    ],
    
    author = "P Henderson and M J Henderson",
    author_email = "matthew_henderson@berea.edu",
    description = "Whole Architecture Verification",
    license = "GPL",
    keywords = "wave verification",
    url = "http://wiki.github.com/MHenderson/wave",  
)
