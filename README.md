# python-laba1

Лабораторная №1: калькулятор и конвертер в терминале.
Калькулятор считает выражения, конвертер решает единицы.

Операции: "+", "-", "*", "/", унарные знаки и скобки.
Единицы: "mm", "cm", "m", "km"; "g", "kg"; "c", "f", "k".

Запуск из папки проекта в PowerShell, нужен Python 3.12+:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
python -m toolkit --help
python -m toolkit calc "2 + 3 * 4"
python -m toolkit convert 2.5 --from m --to cm
```

Программа запускаеться через "__main__.py", команды разбирает "main.py".
"__init__.py" обозначает пакет, "calculator.py" считает, "converter.py" переводит величины,
"constants.py" хранит постоянные значения, "errors.py" — классы ошибок, "tests/" — тесты.
"power.py" — пример из шаблона.

Тесты: "python -m pytest". Проверка стиля: "ruff check .".
Ошибки выводятся в stderr с кодом 2, успешная команда — с кодом 0.
