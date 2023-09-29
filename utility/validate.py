#!/usr/bin/env python3

import argparse
import json
import pathlib

import jsonschema


schema = {
    "type": "array",
    "minItems": 1,
    "uniqueItems": True,
    "items": {
        "type": "object",
        "properties": {
            "package_name": {"type": "string"},
            "version": {
                "type": "string",
                # PEP404 version string prefixed with a comparison operator
                # Excluding trailing '.*'
                # https://peps.python.org/pep-0440/#version-specifiers
                # https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
                "pattern": r'^(~=|==|!=|<=|>=|<|>|===)\s*([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$'
            },
            "approval_date": {
                "type": "string",
                "format": "date"
            },
            "revoke_date": {
                "oneOf": [
                    {
                        "type": "string",
                        "format": "date"
                    },
                    {
                        "type": "null"
                    }
                ]
            }
        }
    }
}


class ValidationError(Exception):
    pass


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="validate",
        description="Validate package files",
    )
    parser.add_argument(
        "filename",
        type=pathlib.Path,
        nargs="+",
    )

    clargs = parser.parse_args()

    for path in clargs.filename:
        with open(path, "r") as file:
            try:
                jsonschema.validate(
                    instance=json.load(file),
                    schema=schema,
                    format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER
                )
            except jsonschema.exceptions.ValidationError as exc:
                raise ValidationError(
                    f"File {path} is not valid"
                ) from exc


if __name__ == "__main__":
    main()
