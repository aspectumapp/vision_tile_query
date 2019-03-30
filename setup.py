try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='vision_tile_query',
    version='0.0.1',
    description='Library for create mVT SQL query',
    long_description=open('README.md').read(),
    author='Andrey Sorokin',
    author_email='andreysrkn@eosda.com',
    url='https://github.com/eos-vision/vision_tile_query',
    packages=['vision_tile_query'],
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
    # TODO package_data
)