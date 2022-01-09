from os.path import exists

from src import ini


class MakeScriptData:
    def __init__(self, py_start: str, entry_start: str):
        self.py_start = py_start
        self.entry_start = entry_start

    def get_py_line(self, py_cmd: str) -> str:
        return f'{self.py_start}"{py_cmd}"\n'

    def get_entry_line(self, entry_name: str) -> str:
        return f'{self.entry_start}"{entry_name}"\n'


_SH = MakeScriptData('PYTHON_CMD=', 'ENTRYPOINT=')
_VBS = MakeScriptData('pythonCmd = ', 'entrypoint = ')


def _make_script(file_key: str, file_data: Dict[str, str]) -> None:
    py_cmd = ini.sys('python3')
    entry = ini.sys('entrypoint')

    file = ini.sys(file_key)
    if not exists(file):
        return

    newlines = []
    with open(file, 'r', encoding='utf-8') as script:
        for line in script.readlines():
            if line.startswith(file_data.py_start):
                newlines.append(file_data.get_py_line(py_cmd))
            elif line.startswith(file_data.entry_start):
                newlines.append(file_data.get_entry_line(entry))
            else:
                newlines.append(line)
    with open(file, 'w', encoding='utf-8') as script:
        for line in newlines:
            script.write(line)


def make_sh() -> None:
    """ Updates the run.sh file with the settings from the .ini file. """
    _make_script('run-sh', _SH)


def make_vbs() -> None:
    """ Updates the run.vbs file with the settings from the .ini file. """
    _make_script('run-vbs', _VBS)


if __name__ == '__main__':
    make_sh()
    make_vbs()
