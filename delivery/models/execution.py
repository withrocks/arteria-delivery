
from delivery.models import BaseModel


class ExecutionResult(BaseModel):

    def __init__(self, stdout, stderr, status_code):
        self.stdout = stdout
        self.stderr = stderr
        self.status_code = status_code

class Execution(BaseModel):
    def __init__(self, pid, process_obj):
        self.pid = pid
        self.process_obj = process_obj
