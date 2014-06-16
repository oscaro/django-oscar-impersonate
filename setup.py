from setuptools import setup, find_packages


setup(

    name='django-oscar-impersonate',
    version='0.1',
    url='https://github.com/oscaro/django-oscar-impersonate',
    author="Nicolas Dubois",
    author_email="nicolas.c.dubois@gmail.com",
    description="Wrapper of django-impersonate for django-oscar",
    long_description=open('README.rst').read(),
    keywords="django, oscar, impersonate",
    license='BSD License',
    packages=find_packages(exclude=['sandbox*']),
    include_package_data=True,
    install_requires=['django-oscar>=0.4'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]

)
