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
        
            if not self.tasks:
                break

            if self.tasks[0].canceled:
                del self.tasks[0]
                continue

            if not self.tasks[0].started:
                assert not self.tasks[0].is_alive()
                self.tasks[0].start()
                assert self.tasks[0].is_alive()
                break

            if not self.tasks[0].is_alive():
                self.tasks[0].finish()
                del self.tasks[0]
                continue


