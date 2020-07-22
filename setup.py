from setuptools import setup, find_packages


INSTALL_REQUIRES = ['requests', 'log_color', ]


setup(
    name='dopameme',
    author='Sparkle Wonder',
    author_email='sekret@gmail.com',
    description='Get a quick dopamine hit of cuteness',
    version='0.1.1',
    url='https://github.com/middlemarch/cutiverse',
    license="wtfpl",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['dopameme = dopameme.entry_point:main']
    },
)
