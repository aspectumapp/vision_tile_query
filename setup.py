import vision_tile_query
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='vision_tile_query',
    version=vision_tile_query.version,
    description='Library for creating MVT SQL query',
    long_description=open('Readme.md').read(),
    author='Andrey Sorokin',
    author_email='andreysrkn@eosda.com',
    url='https://github.com/eos-vision/vision_tile_query',
    packages=['vision_tile_query',
              'vision_tile_query/utils',
              'vision_tile_query/contrib'],
    install_requires=[
        'SQLAlchemy', 'mercantile', 'geoalchemy2'
    ],
    license='Unlicense',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
    ],
)
