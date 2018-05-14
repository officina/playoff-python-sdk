from setuptools import setup, find_packages
setup(
  name = 'playoff',
  version = '0.5.0',
  packages= ['src'],
  description='This is the official OAuth 2.0 Python client SDK for the Playoff API',
  long_description='''
    It supports the client_credentials and authorization code OAuth 2.0 flows.
    For a complete API Reference checkout [Playoff Developers](https://dev.playoff.cc/docs/api) for more information.
  ''',
  url='https://github.com/officina/playoff-python-sdk',
  author='Officina',
  author_email='support@playoff.cc',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.6'
  ],
  keywords='REST, Playoff API, Playoff SDK, Gamification'
)
