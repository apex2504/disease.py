from setuptools import setup

ver = '1.0.2'

with open('README.md', 'r') as f:
  long_desc = f.read()

setup(
  name = 'disease.py',
  packages = ['diseaseapi'],
  version = ver,
  license='MIT',
  description = 'An asynchronous wrapper for the Open Disease API written in Python.',
  long_description= long_desc,
  long_description_content_type = 'text/markdown',
  author = 'Rob Wainwright',
  author_email = 'wainwrightbobby@gmail.com',
  url = 'https://github.com/apex2504/disease.py',
  keywords = ['coronavirus', 'covid-19'],
  install_requires=[
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
