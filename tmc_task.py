import threading

class Taks(threading.Thread):

    def __init__(self):
        super().__init__()
        self.started = False
        self.canceled = False

    def start(self):
        super().start()
        self.started = True

    def run(self):
        pass

    def finish(self):
        pass

    def cancel(self):
        self.canceled = True

class TaskManager:

    def __init__(self):
        self.tasks = []

    def enqueue(self,task):
        self.tasks.append(task)

    def check(self):

        while True:
        
            # queue is empty
            if not self.tasks:
                break

            head = self.tasks[0]

            # consume head
            if not head.started:

                if head.canceled:
                    self.tasks.pop()
                    continue

                assert not head.is_alive()
                head.start()
                assert head.is_alive()

                break

            # head is finished
            if not head.is_alive():
        
                head.finish()
                head.join()
                self.tasks.pop()

                continue
            
            # head is running
            break

