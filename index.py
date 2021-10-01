import os
import ctypes
import keyboard
import threading

from utils import config_handler
from utils.task_creator import TaskCreator


class MainIndex:
    def __init__(self, extension: str = ".txt"):
        self.version = "1.1.3"
        self.extension = extension
        self.compiled = False
        self.is_paused = False
        self.config = config_handler.Config().get()
        self.e = threading.Event()

        ctypes.windll.kernel32.SetConsoleTitleW("MacroMaker")
        self.main_handler()

    def find_config(self):
        """ Find .txt files located in the same directory """
        collector = []
        for file in os.listdir():
            if file.endswith(self.extension):
                collector.append(file)

        return sorted(collector, key=lambda g: g.lower())

    def get_config(self):
        """ Get .txt files and make a list to choose from, then check if it's valid """
        find_files = self.find_config()
        make_list = "\n".join([f"[{num}] {g}" for num, g in enumerate(find_files)])

        if not make_list:
            TaskCreator("MacroMaker.exe", compile=False).error_break(
                0, 'make_list = "\\n".join([f"[{num}] {g}" for num, g in enumerate(find_files)])',
                "Could not find any .txt files in the same directory"
            )

        while True:
            print(f"Select a file:\n{make_list}")
            filename = input("> ")
            try:
                num = int(filename)
                selected = find_files[num]
                return selected
            except ValueError:
                pass
            except IndexError:
                pass

    def toggle_pause(self):
        if not self.compiled:
            return False

        self.is_paused = False if self.is_paused else True

        if self.is_paused:
            print("--- Macro script has been set to pause ---", end='\r')
        else:
            print(" " * 50, end="\r")
            self.e.set()

    def macro_loop(self, e, manager):
        while True:
            if self.is_paused:
                e.wait()
                self.is_paused = False
                e.clear()

            manager.execute_commands()

    def main_handler(self):
        """ The start of the script """
        pause_key = self.config["MacroMaker"]["pause"]

        try:
            keyboard.add_hotkey(pause_key, self.toggle_pause)
        except ValueError:
            self.filename = "config.ini"
            TaskCreator("MacroMaker.exe", compile=False).error_break(
                2, f"pause={pause_key}",
                f"Pause key '{pause_key}' is not a valid keyboard input..."
            )

        print(
            f"  Welcome to MacroMaker v{self.version}\n"
            f"  If you need help, please visit the following link:\n"
            f"  https://github.com/AlexFlipnote/MacroMaker\n"
            f"\n  [!] pause={pause_key} (Button you use to pause script)\n"
        )

        filename = self.get_config()
        task_manager = TaskCreator(filename)

        # Print it out as a reminder while loop goes on
        print(f"[ Your pause key is '{pause_key}' ]")

        if not task_manager.debug:
            print('')  # This is only used to have some nice spacing with the text

        t = threading.Thread(name="yes", target=self.macro_loop, args=(self.e, task_manager))
        t.start()
        self.compiled = True

        """while True:
            if not self.is_paused:
                task_manager.execute_commands()

            self.is_paused = True if task_manager.paused else False"""


if __name__ == "__main__":
    try:
        MainIndex()
    except KeyboardInterrupt:
        TaskCreator("MacroMaker.exe", compile=False).error_break(
            0, "task_manager.execute_commands()", "KeyboardInterrupt"
        )
