import argparse
import sys

from toolkit.calculator import calculate_expression
from toolkit.converter import convert
from toolkit.errors import ToolkitError


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(
    dest="command",
    required=True,
)

calc_parser = subparsers.add_parser("calc")
calc_parser.add_argument("expression")

convert_parser = subparsers.add_parser("convert")
convert_parser.add_argument("value", type=float)
convert_parser.add_argument(
    "--from",
    dest="from_unit",
    required=True,
)
convert_parser.add_argument(
    "--to",
    dest="to_unit",
    required=True,
)

args = parser.parse_args()

try:
    if args.command == "calc":
        result = calculate_expression(args.expression)
        print(result)

    elif args.command == "convert":
        result = convert(
            args.value,
            args.from_unit,
            args.to_unit,
        )
        print(result)

except ToolkitError as error:
    print(error, file=sys.stderr)
    raise SystemExit(2)
