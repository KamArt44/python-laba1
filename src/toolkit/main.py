import argparse
import sys

from toolkit.calculator import calculate_expression
from toolkit.converter import convert
from toolkit.errors import CalculatorError, ConverterError
def main(argv: list[str] | None = None) -> int:
    #возвращает код завершения 0 или 2
    parser = argparse.ArgumentParser(description="Калькулятор и конвертер величин")
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc", help="Вычислить выражение")
    calc_parser.add_argument("expression")

    convert_parser = subparsers.add_parser("convert", help="Перевести величину")
    convert_parser.add_argument("value", type=float)
    convert_parser.add_argument("--from", dest="from_unit", required=True)
    convert_parser.add_argument("--to", dest="to_unit", required=True)

    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            result = calculate_expression(args.expression)
        else:
            result = convert(args.value, args.from_unit, args.to_unit)
    except (CalculatorError, ConverterError) as error:
        print(error, file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
