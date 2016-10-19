
from delivery.models import BaseModel


class DeliveryOrder(BaseModel):

    def __init__(self, delivery_project_id, delivery_target):

        # TODO Still need to figure out the details here...

        self.delivery_project_id = delivery_project_id
        # TODO Need to validate that delivery_target is a valid model i.e. Project or Runfolder
        self.delivery_target = delivery_target


class DeliveryStatus(BaseModel):

    def __init__(self, successful=None, msg=None):
        self.successful = successful
        self.msg = msg


class DeliveryIdentifier(BaseModel):

    def __init__(self, identifier):
        self.identifier = identifier
