"""
setup.py

used for creating twender package
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'description': 'Machine Learning Project',
    'author': 'Matt Stanley',
    'url': 'url',
    'download_url': 'download url',
    'author_email': 'stanley.t.matthew@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['tweet_collection', 'tweet_analysis', 'tweet_application'],
    'scripts': [],
    'name': 'twender'
}

setup(**config)
