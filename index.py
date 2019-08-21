import os
import ctypes

from utils.taskcreator import TaskCreator


class MainIndex:
    def __init__(self, extension: str = ".txt"):
        self.version = "1.0"
        self.extension = extension
        self.stopped = False

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

    def main_handler(self):
        """ The start of the script """
        print(
            f"  Welcome to MacroMaker v{self.version}\n"
            f"  If you need help, please visit the following link:\n"
            f"  https://github.com/AlexFlipnote/MacroMaker\n"
        )

        filename = self.get_config()
        task_manager = TaskCreator(filename)
        print("Done, starting service...")

        if not task_manager.debug:
            print('')  # This is only used to have some nice spacing with the text

        while True:
            task_manager.execute_commands()


if __name__ == "__main__":
    try:
        MainIndex()
    except KeyboardInterrupt:
        TaskCreator("MacroMaker.exe", compile=False).error_break(
            0, "task_manager.execute_commands()", "KeyboardInterrupt"
        )
