import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eruditcache",
    version="0.0.1",
    author="Erudit",
    author_email="info@erudit.org",
    description="Redis wrapper to group cache keys in Redis sets for easier cache invalidation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.erudit.org/erudit/portail/eruditcache",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
