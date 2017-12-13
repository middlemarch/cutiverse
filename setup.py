from setuptools import setup, find_packages


TESTS_REQUIRE = []
INSTALL_REQUIRES = ['requests', 'log_color', ]


setup(
    name="dopamine",
    author="Sparkle Wonder",
    author_email="sekret@gmail.com",
    description="Get a quick dopamine hit of cuteness",
    version="0.1.1",
    url="https://github.com/middlemarch/cutiverse",
    license="wtfpl",
    packages=find_packages('src'),
    package_dir={"": "src"},
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    entry_points={
        "console_scripts": ["dopamine = dopamine.entry_point:main"]
    },
)
