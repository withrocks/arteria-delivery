
import subprocess
import atexit

from delivery.models.execution import ExecutionResult, Execution


class ExternalProgramService():

    @staticmethod
    def run(cmd):
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        # On exiting the main program, make sure that the subprocess
        # gets killed.
        atexit.register(p.terminate)
        return Execution(pid=p.pid, process_obj=p)

    @staticmethod
    def run_and_wait(cmd):
        execution = ExternalProgramService.run(cmd)
        out, err = execution.process_obj.communicate()
        status_code = execution.process_obj.wait()
        return ExecutionResult(out, err, status_code)

