class SetupData:

    def __init__(self, py_start: str, entry_start: str):
        self.py_start = py_start
        self.entry_start = entry_start

    def get_py_line(self, py_cmd: str) -> str:
        return f'{self.py_start}"{py_cmd}"\n'

    def get_entry_line(self, entry_name: str) -> str:
        return f'{self.entry_start}"{entry_name}"\n'
