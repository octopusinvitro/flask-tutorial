from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    description='Flask tutorial of a simple blog with a SWLite database',
    url='https://github.com/octopusinvitro/flask-tutorial',
    author='Octopus in Vitro',
    author_email='octopusinvitro@users.noreply.github.com',
    license='MIT',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'flask',
    ],
    tests_require=[
        'coverage',
        'flake8',
        'pytest'
        # 'coveralls-python',
    ]
)
