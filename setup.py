import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


requirements = [line for line in read_file('requirements/base.txt').split('\n')]

setup(
    name='rapidsms-reports',
    version=__import__('reports').__version__,
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['distribute'] + requirements,
    url='https://github.com/caktus/rapidsms-reports/',
    license='BSD',
    description=u' '.join(__import__('reports').__doc__.splitlines()).strip(),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.rst'),
    test_suite="runtests.runtests",
    zip_safe=False,
)
