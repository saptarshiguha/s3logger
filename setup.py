from setuptools import setup, find_packages

setup(
    name = 's3logger',
    version = '0.0.1',
    description = 'Log Messages to File on S3',
    py_modules = ['logger'],

    author = u'Saptarshi Guha',
    author_email = 'sguha@mozilla.com',

    url = 'https://github.com/saptarshiguha/s3logger',

    setup_requires = ['boto'],
    install_requires = ['boto']

)
