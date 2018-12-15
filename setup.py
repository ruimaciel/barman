from setuptools import setup

setup(
    name='barman',
    version='0.1.0',
    description='A 2D engineering beam theory model implemente in Python 3',
    packages=['barman'],
    author='Rui Maciel',
    author_email='rui.maciel@gmail.com',
    maintainer='Rui Maciel',
    maintainer_email='rui.maciel+barman@gmail.com',
    url='http://github.com/ruimaciel/barman',
    license='GPLv3',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'numpy>=1.14,<2.0',
        'scipy>=1.1,<2.0',
    ],
)
