[![Jazzband](https://jazzband.co/static/img/jazzband.svg)](https://jazzband.co/)

This is a [Jazzband](https://jazzband.co/) project.
By contributing you agree to abide by the [Contributor Code of Conduct](https://jazzband.co/about/conduct) and follow the [guidelines](https://jazzband.co/about/guidelines).

## Contributing to Django Fernet Encrypted Fields

We welcome contributions from the community to improve and maintain Django Fernet Encrypted Fields.
Please follow these guidelines to ensure your contributions are accepted:

1. **Fork the Repository**: Start by forking the repository to a personal/organization GitHub account.
2. **Clone the Repository**: Clone the forked repository to your local machine.
3. **Set Up the Environment**: Set up a virtual environment and install the necessary
   dependencies for development and testing.
   ```shell
   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
4. **Install the pre-commit hooks**: We use [pre-commit](https://pre-commit.com/) to ensure code quality.
   Install the pre-commit hooks by running:
   ```shell
   $ pre-commit install
   ```
5. **Create a Branch**: Create a new branch for the feature or bug fix.
6. **Make Changes**: Make the changes and ensure they are well-documented.
7. **Run Tests**: Ensure all tests pass before submitting a pull request.
   ```shell
   $ pip install coverage pytest
   $ coverage3 run --source='./encrypted_fields' manage.py test
   ```
8. **Submit Pull Request**: Submit a pull request with a clear title, description of the changes,
   motivations, and any relevant issue numbers.
