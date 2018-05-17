import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    DIRECTORY_TO_WATCH = '/media/rohit/New Volume/PROJECTS/File-Watcher/watch_this_directory'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print("Watcher running ...")
        try:
            while(True):
                time.sleep(5)
        except:
            self.observer.stop()
            print("Some error occurred . Stopping the watcher.")

        self.observer.join()


class Handler(FileSystemEventHandler):


    @staticmethod
    def process(self, event):
        """
        File actions will be processed here
        Printing only as of now for debugging
        """
        print(event.src_path, event.event_type)

    # def on_modified(self, event):
    #     self.process(self,event)

    def on_created(self, event):
        with open("watcher-log.txt", 'a') as logfile:
            logfile.write(event.src_path + " " + event.event_type + "\n")
        self.process(self,event)

    def on_deleted(self, event):
        self.process(self,event)

    def on_moved(self, event):
        self.process(self,event)


if __name__ == '__main__':
    w = Watcher()
    print("Starting watcher.. ")
    w.run()
