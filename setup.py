import os

from setuptools import setup

rootpath = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return open(os.path.join(rootpath, *parts)).read()


def walk_subpkg(name):
    data_files = []
    package_dir = "branca"
    for parent, dirs, files in os.walk(os.path.join(package_dir, name)):
        # Remove package_dir from the path.
        sub_dir = os.sep.join(parent.split(os.sep)[1:])
        for f in files:
            data_files.append(os.path.join(sub_dir, f))
    return data_files


pkg_data = {
    "": [
        "*.js",
        "plugins/*.js",
        "plugins/*.html",
        "plugins/*.css",
        "plugins/*.tpl",
        "templates/*.html",
        "templates/*.js",
        "templates/*.txt",
    ],
}
pkgs = ["branca"]

LICENSE = "MIT"
long_description = "{}".format(read("README.md"))

# Dependencies.
with open("requirements.txt") as f:
    tests_require = f.readlines()
install_requires = [t.strip() for t in tests_require]


setup(
    name="branca",
    description="Generate complex HTML+JS pages with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Martin Journois",
    url="https://github.com/python-visualization/branca",
    keywords="data visualization",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
    ],
    packages=pkgs,
    package_data=pkg_data,
    include_package_data=True,
    use_scm_version={
        "write_to": "branca/_version.py",
        "write_to_template": '__version__ = "{version}"',
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    },
    tests_require=["pytest"],
    license=LICENSE,
    install_requires=install_requires,
    python_requires=">=3.7",
    zip_safe=False,
)
