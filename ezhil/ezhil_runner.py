# ezhil_runner.py
import sys
import os
import io
import contextlib
import traceback
from ezhil import EzhilFileExecuter,EzhilCustomFunction

class InputPool:

    def __init__(self, inputs):
        self.inputs = inputs
        self._it = iter(inputs)
    def __call__(self, prompt=""):
        try:
            return next(self._it)
        except StopIteration:
            raise RuntimeError("Input exhausted")
    def reset(self):
        self._it = iter(self.inputs)

def main():    
    output_buffer = io.StringIO()
    exitcode = 0
    inputs = sys.stdin.read()
    if sys.argv[1]:
        print("File present")
        program_file = open(sys.argv[1],"r",encoding='utf-8')
        program = program_file.read()
    try:
        inputs = []
        ## __EZHIL_INPUTS__
        #print(program)
        raw = program.split("__EZHIL_INPUTS__")[1:][0]
        normalized = [line.strip() for line in raw.splitlines() if line.strip()]

        for input_value in normalized:
            inputs.append(input_value)
        
        program = program.split("__EZHIL_INPUTS__")[0]

        with contextlib.redirect_stdout(output_buffer):
            EzhilCustomFunction.set(InputPool(inputs))
            obj = EzhilFileExecuter(
                file_input=[program],
                redirectop=False,
                debug=False
            )
            exitcode = obj.exitcode
            EzhilCustomFunction.reset()
    except IndexError as e:
        print(traceback.print_exc(e)[0])
        print("Input Parsing Failed",str(e))
        exitcode = 1            
    except Exception as e:
        print(traceback.print_exc(e)[0])
        print("FAILED EXECUTION:", str(e))
        exitcode = 1

    #print("\n__EZHIL_EXITCODE__", exitcode)
    print(output_buffer.getvalue())
    sys.exit(exitcode)
if __name__ == "__main__":
    main()
