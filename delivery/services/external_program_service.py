
import subprocess

from delivery.models.execution import ExecutionResult


class ExternalProgramService():

    @staticmethod
    def run(cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate()
        status_code = p.wait()
        return ExecutionResult(out, err, status_code)
