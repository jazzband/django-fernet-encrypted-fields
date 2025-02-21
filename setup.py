from setuptools import setup

setup(
    name="django-fernet-encrypted-fields",
    description=("This is inspired by django-encrypted-fields."),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/jazzband/django-fernet-encrypted-fields/",
    license="MIT",
    author="jazzband",
    author_email="n.anahara@fragment.co.jp",
    packages=["encrypted_fields"],
    version="0.3.0",
    install_requires=[
        "Django>=3.2",
        "cryptography>=35.0.0",
    ],
)
