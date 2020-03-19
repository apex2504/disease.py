from distutils.core import setup

setup(
  name = 'corona-api',
  packages = ['corona-api'],
  version = '0.1',
  license='MIT',
  description = 'An asynchronous wrapper for the corona.lmao.ninja API written in Python.',
  author = 'Rob Wainwright',
  author_email = 'wainwrightbobby@gmail.com',
  url = 'https://github.com/apex2504/python-corona-api',
  keywords = ['coronavirus', 'covid-19'],
  install_requires=[
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 4 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)