
from delivery.models import BaseModel


class ExecutionResult(BaseModel):
    """
    Used to represent the result of a external program execution
    """

    def __init__(self, stdout, stderr, status_code):
        """
        Instantiate the execution result
        :param stdout: of the executed process
        :param stderr: of the executed process
        :param status_code: exit code of the program
        """
        self.stdout = stdout
        self.stderr = stderr
        self.status_code = status_code


class Execution(BaseModel):
    """
    Model a ongoing execution and provides a handle for the associated process object
    """

    def __init__(self, pid, process_obj):
        """
        Instantiate a ongoing external program execution
        :param pid: of the process
        :param process_obj: the python process object associated with the execution
        """
        self.pid = pid
        self.process_obj = process_obj
