from setuptools import setup

setup(
    name="django-fernet-encrypted-fields",
    description=("This is inspired by django-encrypted-fields."),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jazzband/django-fernet-encrypted-fields",
    license="MIT",
    author="fragment.co.jp",
    author_email="info@fragment.co.jp",
    packages=["encrypted_fields"],
    version="0.1.3",
    install_requires=[
        "Django>=3.2",
        "cryptography>=35.0.0",
    ],
)
