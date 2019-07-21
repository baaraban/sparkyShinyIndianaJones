import subprocess
import os

dirname, filename = os.path.split(os.path.abspath(__file__))

cmd = """cd {} && node -e 'require(\"./index.js\").parse(\"{}\")'"""

def periodo(value):
    output = subprocess.check_output(cmd.format(dirname, value), shell=True)
    try:
        return int(output)
    except:
        raise Exception('Periodo could not parse this date.')