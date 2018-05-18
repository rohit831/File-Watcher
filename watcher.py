import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


#  This class watches for an event on a directory
#  Also when a event occurs, it calls the respective handler for the event
class Watcher:
    DIRECTORY_TO_WATCH = '/media/rohit/New Volume/PROJECTS/File-Watcher/watch_this_directory'

    def __init__(self):
        self.observer = Observer()
        self.update_log_file_on_start()

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

    def get_original_structure(self):
        """
        This function gets the original directory structure and loads them into a list
        """
        entries= []
        for root, dirs, files in os.walk(self.DIRECTORY_TO_WATCH):
            for dir in dirs:
                entries.append(os.path.join(root, dir))

            for file in files:
                entries.append(os.path.join(root, file))

        return entries

    def get_current_structure(self):
        """
         This function loads the watcher list from the log file
        """
        entries = []
        with open("watcher-log.txt", 'r') as logfile:
            for fileEntry in logfile:
                entries.append(fileEntry[:-1])
        return entries

    def update_log_file_on_start(self):
        """
        This function will update the log file for the
        differences when the service was not running
        """
        current_entries = self.get_current_structure()
        original_entries = self.get_original_structure()
        difference_list = list(set(original_entries) - set(current_entries))
        with open("watcher-log.txt", "a") as logfile:
            for file in difference_list:
                logfile.write('%s\n' % file)

        print("Updated log files for differences ..")


#  This class is used for handling all the events which occur on a directory
#  Also it performs respective actions corresponding to the particular actions
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

    # whenever a new file or directory is created
    def on_created(self, event):
        with open("watcher-log.txt", 'a') as logfile:
            logfile.write(event.src_path + "\n")
        self.process(self,event)

    # whenever a new file or directory is deleted
    def on_deleted(self, event):
        self.process(self,event)

    # whenever a new file or directory is moved
    def on_moved(self, event):
        self.process(self,event)


if __name__ == '__main__':
    print("Starting watcher.. ")
    w = Watcher()
    w.run()
