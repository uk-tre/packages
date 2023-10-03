#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

import jsonschema


class ValidationError(Exception):
    pass


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="validate",
        description="Validate package files",
    )
    parser.add_argument(
        "filename",
        type=Path,
        nargs="+",
    )
    parser.add_argument(
        "-o",
        "--other",
        action="store_true"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true"
    )

    clargs = parser.parse_args()

    if clargs.other:
        schema_filename = "schema_other.json"
    else:
        schema_filename = "schema.json"

    schema_path = Path(__file__).parent.parent.absolute() / schema_filename
    with open(schema_path, "r") as file:
        schema = json.load(file)

    for path in clargs.filename:
        if clargs.verbose:
            print(f"Validating {path}")
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
