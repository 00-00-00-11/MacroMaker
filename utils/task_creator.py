import keyboard
import mouse
import os
import sys
import time


class TaskCreator:
    def __init__(self, filename: str, debug: bool = False, compile: bool = True):
        self.filename = filename
        self.debug = debug
        self.loop_count = 0
        self._list = []

        if compile:
            self.compile_macro()

    def linter_garbage_collector(self):
        """ This was only made to have linter not complain about 'unused variables' """
        time.time()
        return "yes"

    def error_break(self, line: int, text_line: str, reason: str):
        """ A simple and nice custom error breaker I made for fun, lol """
        print(
            f"\nTraceback (most recent call last)\n"
            f'  File "{self.filename}", line {line}, in <compiler>\n'
            f"    {text_line}\n"
            f"  {reason}\n"
        )

        try:
            input("Press enter or click X in this window to exit...")
        except Exception:
            pass  # Well fuck you too, you're going out anyway!

        sys.exit(1)

    def keyboard_press(self, value: str):
        """ Generates a keypress press """
        try:
            if "+" in value and len(value) > 1:
                keyboard.parse_hotkey(value)
            else:
                keyboard.key_to_scan_codes(value)
        except ValueError as e:
            if str(e).startswith("Unexpected key type"):
                return "notReadable"
            else:
                return "notMapped"

        if self.debug:
            self._list.append(f"print('Pressing {str(value)}')")

        self._list.append(f"keyboard.press_and_release('{value}')")
        return True

    def mouse_press(self, value: str):
        """ Generates a mouse press """
        if value == "left":
            direction = "left"
        elif value == "right":
            direction = "right"
        else:
            return "invalidButton"

        self._list.append(f"mouse.click(button='{direction}')")
        return True

    def mouse_scroll(self, value: str):
        """ Generates a mouse scroll movement """
        if value == "up":
            direction = 1
        elif value == "down":
            direction = -1
        else:
            return "invalidDirection"

        self._list.append(f"mouse.wheel(delta={direction})")
        return True

    def mouse_movement(self, value: str):
        """ Coming soon... """
        if input == "up":
            mouse.move(0, -self.mouse_movement, absolute=False, duration=self.mouse_delay)
            return True
        if input == "down":
            mouse.move(0, self.mouse_movement, absolute=False, duration=self.mouse_delay)
            return True
        if input == "left":
            mouse.move(-self.mouse_movement, 0, absolute=False, duration=self.mouse_delay)
            return True
        if input == "right":
            mouse.move(self.mouse_movement, 0, absolute=False, duration=self.mouse_delay)
            return True

    def debug_manager(self, value: str):
        """ Manages the debug mode """
        if value.lower() not in ["true", "false"]:
            return "invalid"

        if value.lower() == "true":
            if not self.debug:
                print("\nDebug mode: enabled\n")
                self.debug = True
                return True
            else:
                return False
        else:
            self.debug = False
            return False

    def keyboard_type(self, text: str):
        """ Generates a keypress write command """
        if self.debug:
            self._list.append(f"print('Wrote the following: {str(text)}")

        self._list.append(f"keyboard.write('{text}')")
        return True

    def timeout(self, timeout: float):
        """ Generates a Python.time timeout """
        if len(timeout.split(" ")) != 1:
            return "errVal"
        else:
            try:
                get_value = float(timeout)
            except ValueError:
                return "errFloat"

            if self.debug:
                self._list.append(f"print('Waiting {get_value} seconds due to TIMEOUT')")

            self._list.append(f"time.sleep({get_value})")
            return True

    def to_execute(self):
        """ Makes all commands to a string for Python.exec() """
        make_stringable = "\n".join(self._list)

        self.loop_count += 1
        if self.debug:
            print(f"\n--- Loop counter: {self.loop_count} ---\n")
        else:
            print(f"Loop counter: {self.loop_count}", end='\r')

        return make_stringable

    def execute_commands(self):
        """ Executes the ready-to-use string made by self.to_execute() """
        exec(self.to_execute())
        return True

    def compile_macro(self):
        """ Compiles the .txt file prompted by main file and gives error if failed """
        print("\nAttempting to compile...")
        with open(self.filename, "r", encoding="utf-8") as f:
            data = f.read().splitlines()

        for num, line in enumerate(data, start=1):
            if not line:
                continue

            make_list = line.split(" ")
            prefix = make_list[0].lower()
            context = " ".join([g for g in make_list[1:]]) if len(make_list) > 1 else None

            if not context:
                self.error_break(num, line, f"Missing context to '{prefix.upper()}', can't handle empty context")

            if prefix == "press":
                send_context = self.keyboard_press(context)
                if send_context == "notReadable":
                    self.error_break(num, line, "Could not understand what key you want the script to press")
                if send_context == "notMapped":
                    self.error_break(num, line, "Unknown key, if you're trying to press more at a time, use '+' between or use 'WRITE' for whatever to type.")
            elif prefix == "click":
                send_context = self.mouse_press(context)
                if send_context == "invalidButton":
                    self.error_break(num, line, f"Expected either 'left' or 'right', got '{context}'")
            elif prefix == "scroll":
                send_context = self.mouse_scroll(context)
                if send_context == "invalidDirection":
                    self.error_break(num, line, f"Expected either 'up' or 'down', got '{context}'")
            elif prefix == "timeout":
                send_context = self.timeout(context)
                if send_context == "errVal":
                    self.error_break(num, line, "Expected timeout value of one, got either None or too many")
                if send_context == "errFloat":
                    self.error_break(num, line, f"Could not convert value to float: '{context}'")
            elif prefix == "write":
                send_context = self.keyboard_type(context)
            elif prefix == "debug":
                send_context = self.debug_manager(context)
                if send_context == "invalid":
                    self.error_break(num, line, f"Debug mode only accepts 'TRUE' or 'FALSE'")
            else:
                self.error_break(num, line, f"Unknown command '{prefix.upper()}'")

        if self.debug:
            print(data)

        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        return True
