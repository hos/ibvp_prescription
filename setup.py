from setuptools import setup, find_packages
from os import path
from setuptools.extension import Extension


here = path.abspath(path.dirname(__file__))


setup(
    name = 'ibvp_prescription',

    version = '0.0',

    description = '',

    author = 'Onur Solmaz',

    author_email = 'onursolmaz@gmail.com',

    packages = find_packages(exclude=['contrib', 'docs', 'tests']),

    extras_require = {
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # data_files = [
    #     ('packages',['lazyeqn/lazyeqn.sty']),
    #     # ('shortsym',['shortsym.sty']),
    # ],
    include_package_data=True,
    package_data={'ibvp_prescription': ['lazyeqn/lazyeqn.sty', 'shortsym/shortsym.sty']},

    setup_requires = [
        # 'numpy',
        # 'sympy',
        # 'scipy',
        # 'petsc',
        # 'petsc4py',
        # 'progressbar2',
    ],

    entry_points = {
        'console_scripts': [
            'generate_prescription=ibvp_prescription.generate_prescription:__main__',
        ],
    },
)



