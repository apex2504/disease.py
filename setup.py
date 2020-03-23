from setuptools import setup

with open('README.md', 'r') as f:
  long_desc = f.read()

setup(
  name = 'corona_api',
  packages = ['corona_api'],
  version = '0.4.4',
  license='MIT',
  description = 'An asynchronous wrapper for the corona.lmao.ninja API written in Python.',
  long_description= long_desc,
  long_description_content_type = 'text/markdown',
  author = 'Rob Wainwright',
  author_email = 'wainwrightbobby@gmail.com',
  url = 'https://github.com/apex2504/python-corona-api',
  keywords = ['coronavirus', 'covid-19'],
  install_requires=[
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)