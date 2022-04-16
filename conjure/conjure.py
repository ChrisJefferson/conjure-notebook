from ast import arg
import sys
from subprocess import Popen, PIPE
from .conjurehelper import ConjureHelper

class Conjure:
    def solve(self, code: str, args: str, shell_params: dict):
        conjurehelper = ConjureHelper()
        conjurehelper.clean_tmp_files() # clean temp files of previous run

        param_names = conjurehelper.get_required_params(code)
        temp_essence_file = conjurehelper.create_temp_file(code)
        if len(param_names) > 0:
            params = {}
            for p in param_names:
                if p in shell_params:
                    params[p] = shell_params[p]
                else:
                    raise Exception("Variable {0} is not defined".format(p))
            temp_params_file = conjurehelper.create_params_file(params)
            shell_output = Popen(["conjure solve -ac " + temp_essence_file + " " + temp_params_file +" --output-format=json " + args, ], shell=True, stdout=PIPE, stderr=PIPE)
        else:
            shell_output = Popen(["conjure solve -ac " + temp_essence_file + " --output-format=json " + args, ], shell=True, stdout=PIPE, stderr=PIPE)

        _, error = shell_output.communicate()
        if(error):
            raise Exception(error.decode('utf-8'))
        return conjurehelper.read_solution_json_file()

    def check_conjure():
        try:
            pipes = Popen(["conjure", "--version"],shell=True,
                                    stdout=PIPE, stderr=PIPE)
            (output, erroutput) = pipes.communicate()
            if pipes.returncode != 0:
                print("Error while initializing extension: cannot run conjure. Make sure conjure is on the PATH" , file=sys.stderr)
                return False
        except OSError as _:
                print("Error while initializing extension: cannot run conjure. Make sure conjure is on the PATH" , file=sys.stderr)
                return False
        return True