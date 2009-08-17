from setuptools import setup, find_packages

setup(
    name = "Wave",
    version = "0.0.1",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    entry_points = {
        'console_scripts': ['wavegui = Wave.wavegui:main']
	},
    )
