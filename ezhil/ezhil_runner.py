# ezhil_runner.py
import sys
import io
from contextlib import redirect_stdout
from ezhil import EzhilFileExecuter

def main():
    program = sys.stdin.read()

    output_buffer = io.StringIO()
    exitcode = 0

    try:
        with redirect_stdout(output_buffer):
            obj = EzhilFileExecuter(
                file_input=[program],
                redirectop=False,
                debug=False
            )
            exitcode = obj.exitcode

    except Exception as e:
        print("FAILED EXECUTION:", str(e))
        exitcode = 1

    #print("\n__EZHIL_EXITCODE__", exitcode)
    print(output_buffer.getvalue())
    sys.exit(exitcode)
if __name__ == "__main__":
    main()
