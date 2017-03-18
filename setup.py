import setuptools

setuptools.setup(
    name='pacmods',
    version='0.1.0',
    description='Arch Linux tool to show changes to system config files',
    url='https://github.com/c4rlo/pacmods',
    author='Carlo Teubner',
    author_email='carlo.teubner@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='arch linux configuration',
    py_modules=["pacmods"],
    install_requires=['pyalpm'],
    entry_points={
        'console_scripts': [
            'pacmods=pacmods:main',
        ],
    },
)
