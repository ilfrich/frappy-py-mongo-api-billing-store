from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappymongoapibilling",
      version="0.1.1",
      description="MongoDB Store for the API Billing Backend",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-py-api-billing-store",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappymongoapibilling"
      ],
      install_requires=[
          "frappyapibilling",
          "pbumongo>=1.0.0"
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
