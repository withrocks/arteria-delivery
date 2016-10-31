
import subprocess

from delivery.models.execution import ExecutionResult, Execution


class ExternalProgramService():

    @staticmethod
    def run(cmd):
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        return Execution(pid=p.pid, process_obj=p)

    @staticmethod
    def run_and_wait(cmd):
        execution = ExternalProgramService.run(cmd)
        out, err = execution.process_obj.communicate()
        status_code = execution.process_obj.wait()
        return ExecutionResult(out, err, status_code)

