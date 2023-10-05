# Packages

Structured records of approved packages from TRE operators.

## Structure

- Top level
    - Organisation
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
The other schema is described in [`schema_other.json`](schema_other.json).
