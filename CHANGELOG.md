# Changelog

All notable changes to `django-fernet-encrypted-fields` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `CHANGELOG.md` documenting the full release history of the project.

### Changed

- Applied `ruff format` across the codebase and enforced formatting in CI
  ([#40](https://github.com/jazzband/django-fernet-encrypted-fields/pull/40)).
- Moved `ruff` lint configuration into a dedicated `[tool.ruff.lint]` section and
  lowered the `target-version` to the earliest supported Python version.
- `pre-commit` now runs `ruff format` in addition to `ruff check`.
- Packaging metadata now sources the version directly from `pyproject.toml`.

### Fixed

- CI no longer runs `ruff check` during the installation step.

## [0.4.0] - 2026-04-14

### Added

- Jazzband contributing guide ([#37](https://github.com/jazzband/django-fernet-encrypted-fields/pull/37)).
- `dev` dependency group in `pyproject.toml` (mypy, pre-commit, ruff, pytest, pytest-cov, coverage).
- Django 6.0 compatibility ([#32](https://github.com/jazzband/django-fernet-encrypted-fields/pull/32)).

### Changed

- Migrated project to a `src/` layout ([#39](https://github.com/jazzband/django-fernet-encrypted-fields/pull/39)).
- Bumped minimum required Python version to **3.10**.
- CI now installs the package before running the test suite and uses the `dev` dependency group.

### Removed

- `requirements.txt` (dependencies are now fully managed via `pyproject.toml` with version ranges).

## [0.3.1] - 2025-11-10

### Changed

- Raised minimum Django requirement to **Django 4.2** ([#28](https://github.com/jazzband/django-fernet-encrypted-fields/pull/28)).
- Updated the supported Python / Django version matrix in CI (excluded Python 3.13 with Django 4.2, etc.).

## [0.3.0] - 2025-02-21

### Changed

- Project moved to the **Jazzband** organization (author, URL, and maintainer metadata updated)
  ([#25](https://github.com/jazzband/django-fernet-encrypted-fields/pull/25)).

## [0.2.0] - 2025-01-06

### Added

- Support for Django's `SECRET_KEY_FALLBACKS` to enable secret key rotation
  ([#24](https://github.com/jazzband/django-fernet-encrypted-fields/pull/24)).
- README documentation describing the secret-key rotation workflow.
- `pre-commit` configuration.

### Fixed

- `SECRET_KEY_FALLBACKS` handling for Django `< 4.1`.
- Lint errors and GitHub Actions workflow triggers.

## [0.1.3] - 2023-07-24

### Added

- Support for encrypted JSON fields (`EncryptedJSONField`) with tests ensuring key retention
  ([#14](https://github.com/jazzband/django-fernet-encrypted-fields/pull/14)).

### Changed

- Set minimum required Django version to **3.2**.

### Fixed

- `EncryptedIntegerField`: corrected `get_prep_value` / `to_python` behavior
  ([#11](https://github.com/jazzband/django-fernet-encrypted-fields/pull/11)).

## [0.1.2] - 2022-05-17

### Fixed

- `EncryptedIntegerField` now properly exposes default validators via a `cached_property`,
  restoring expected validation behavior ([#10](https://github.com/jazzband/django-fernet-encrypted-fields/issues/10)).

## [0.1.1] - 2021-12-19

### Fixed

- Django Admin no longer raises an exception when saving encrypted fields. A semaphore
  flag in `clean()` prevents `to_python()` from attempting to decrypt an already-decrypted
  value during form cleaning ([#4](https://github.com/jazzband/django-fernet-encrypted-fields/issues/4)).

## [0.1.0] - 2021-12-15

### Added

- Support for multiple `SALT_KEY` values, enabling SALT rotation while still decrypting
  data encrypted with legacy salts.
- Unit tests covering salt rotation with a retained legacy salt.
- README documentation for rotating salts.
- GitHub Actions CI: linting (black, flake8), testing, and coverage across multiple Python versions.

## [0.0.2] - 2021-09-30

### Added

- `long_description` (sourced from `README.md`) and `long_description_content_type` in
  `setup.py` so the project description renders correctly on PyPI.

## [0.0.1] - 2021-09-30

### Added

- Initial release inspired by `django-encrypted-fields`.
- Symmetric encryption for Django model fields backed by Fernet, including:
  `EncryptedFieldMixin`, `EncryptedTextField`, `EncryptedCharField`,
  `EncryptedDateTimeField`, `EncryptedIntegerField`, `EncryptedDateField`,
  `EncryptedFloatField`, `EncryptedEmailField`, `EncryptedBooleanField`.
