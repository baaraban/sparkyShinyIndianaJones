This code is a wrapper over [periodo-date-parser](https://github.com/periodo/periodo-date-parser) tool developed by Periodo. If range of dates were detected, it returns average of them.

File wrapper.py implements wrapper functionality over this library to use it in Python.

### Usage

1. Install [Node](https://nodejs.org) of the latest stable version.
2. Navigate to this directory and run `npm install`
3. `from periodo_date_parser.periodo_date_parser import periodo` and then `periodo("200 AD")`. It returns either integer year, or raises an Exception.