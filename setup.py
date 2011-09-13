from distutils.core import setup

setup(name='plot85',
	version='0.1',
	description='Simple immediate-mode graphics library',
	author='Rich Wareham',
	author_email='rjw57@cam.ac.uk',
	url='https://github.com/rjw57/plot85',
	packages=['pi'],
	requires=['pygame'],
	package_data={'pi': ['*.ttf']}
)
