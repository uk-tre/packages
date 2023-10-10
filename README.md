# Packages

Structured records of approved packages from TRE operators.

## Structure

- `./`
  - `<organisation_name>`
    - `README.md`
      Organisational documentation
      For example, details of your approval process
    - `<repository>.json `
    - `other.json`

### Repositories

We recognise the following major repositories and organisations may create `<repository>.json` files for their packages,

- [PyPI](https://pypi.org)
- [CRAN](https://cran.r-project.org)

### Package list schema

Package lists are formatted as JSON.
The schema for major repositories is formally described in [`schema.json`](./schema.json).
This is a [JSON Schema](https://json-schema.org/overview/what-is-jsonschema) document using the 2020-12 draft.

In brief, each file is a list of package entries with the following fields.

- `package_name` (text, case sensitive, uniquely defines a package for a repository)
- `version` (text, comparison operator plus [PEP440 style](https://peps.python.org/pep-0440/#version-specifiers) version number)
- `approval_date` (ISO 8601)
- `revoke_date` (ISO 8601 or `null` if not revoked)

For example,

```JSON
[
  {
    "package_name": "numpy",
    "version": "== 1.2.3",
    "approval_date": "2023-09-29",
    "revoke_date": null
  }
]
```

Additionally for packages not in a major repository, _i.e._ those in `other.json`, a `url` field is added to uniquely identify the package and give its source.
The "other" schema is described in [`schema_other.json`](schema_other.json).

### Usage

The package lists are simply text files conforming to the JSON schemas.
You can build queries by parsing these files in a local copy of the repository or from GitHub.

#### Command line

Using [`httpie`](https://httpie.io/) and [`jq`](https://jqlang.github.io/jq/).
For example, to get a list of PyPI packages currently allowed by The Alan Turing Institute:

```console
$ https https://raw.githubusercontent.com/uk-tre/packages/main/alan_turing_institute/pypi.json  | jq '.[] | select(.revoke_date == null) | .package_name'
"pandas"
...
```

With a local copy of the repository using `cat` and `jq`.
For example, to get a list of PyPI packages currently allowed any organisation:

```console
$ cat **/pypi.json | jq -s 'add | map(select(.revoke_date == null)) | [.[].package_name] | unique | .[]'
"arviz"
"cycler"
"matplotlib"
"numpy"
"pandas"
"pymc3"
```

#### Python

With a local copy of the repository using the Python standard library.
For example, to get a list of PyPI packages currently allowed any organisation:

```Python
import json
from pathlib import Path

p = Path("./")
packages = [
    package
    for sublist in [json.load(open(f, "r")) for f in p.glob("**/pypi.json")]
    for package in sublist
]
allowed = [
    package["package_name"]
    for package in packages
    if package["revoke_date"] is None
]
allowed = list(set(allowed))
print(allowed)
```

### Contributing

#### Adding an organisation

To add your organisation, create a new directory at the top level of the repository.
Store your package lists in that directory.
Also, create a `README.md` file where you can write information about your organisation and its package approval process.

#### Making changes

After you have made your changes, open a PR to the main branch.

#### Validation and CI

There are CI jobs which must pass for changes to be merged.

A validation process ensures that package lists match the schemas.
You can test this locally using the script `utility/validate.py`.

[Prettier](https://prettier.io/) is used to enforce some code style.
The repository includes a [pre-commit](https://pre-commit.com/) hook for this.
