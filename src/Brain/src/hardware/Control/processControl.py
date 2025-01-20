if __name__ == "__main__":
    import sys
    sys.path.insert(0, "../../..")

from src.templates.workerprocess import WorkerProcess
from enum import Enum
import src.utils.messages.allMessages as allMessages
from src.hardware.Control.threads.threadControl import threadControl
from src.utils.messages.messageHandlerSender import messageHandlerSender

class processControl(WorkerProcess):
    """This process handles Control.
    Args:
        queueList (dictionary of multiprocessing.queues.Queue): Dictionary of queues where the ID is the type of messages.
        logging (logging object): Made for debugging.
        debugging (bool, optional): A flag for debugging. Defaults to False.
    """

    def __init__(self, queueList, logging, debugging=False, auto = False):
        self.queuesList = queueList
        self.logging = logging
        self.debugging = debugging
        self.auto = auto

        super(processControl, self).__init__(self.queuesList)




    def run(self):
        """Apply the initializing methods and start the threads."""
        super(processControl, self).run()
        self._init_threads()

        

    def _init_threads(self):
        """Create the Control Publisher thread and add to the list of threads."""
        ControlTh = threadControl(
            self.queuesList, self.logging, self.debugging, self.auto
        )
        self.threads.append(ControlTh)
