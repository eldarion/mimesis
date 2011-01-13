from distutils.core import setup


VERSION = __import__("mimesis").__version__


setup(
    name = "mimesis",
    version = VERSION,
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "a simple media management app",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/mimesis",
    packages = [
        "mimesis",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
