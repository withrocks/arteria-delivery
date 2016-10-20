
import threading
import os
import time
import random


class StagingService(object):

    def __init__(self, staging_dir):
        print("Test this!")
        self.staging_dir = staging_dir

    @staticmethod
    def _copy_dir(dir_to_copy, target_directory):
        print("Copying in thread...")
        print(dir_to_copy)
        print(target_directory)
        sleep_time = random.randint(1, 5)
        start_time = time.time()
        time.sleep(sleep_time)
        stop_time = time.time()
        print("After sleeping {} s".format(stop_time - start_time))
        # TODO Idea: Attempt to copy and then switch name at the end as a means to check the status
        pass

    def stage_directory(self, dir_to_stage):
        print("Stage directory: {}".format(dir_to_stage))
        thread = threading.Thread(target=StagingService._copy_dir,
                                  kwargs={"dir_to_copy": dir_to_stage,
                                          "target_directory": os.path.join(self.staging_dir)})
        #thread.setDaemon(True)
        thread.start()
