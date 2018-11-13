from setuptools import setup


setup(
    name='ftree',
    version='0.0.1',
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'ftree = ftree.main:cli'
        ]
    }
)
