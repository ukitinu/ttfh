from src import ini

from src.setupdata import SetupData

SH_DATA: SetupData = SetupData('PYTHON_CMD=', 'ENTRYPOINT=')
VBS_DATA: SetupData = SetupData('pythonCmd = ', 'entrypoint = ')


def __setup_script(file_key: str, file_data: SetupData) -> None:
    py_cmd = ini.get_sys('python3')
    entry = ini.get_sys('entrypoint')

    file = ini.get_sys(file_key)
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


def setup_sh() -> None:
    """ Updates the run.sh file with the settings from the .ini file. """
    __setup_script('run-sh', SH_DATA)


def setup_vbs() -> None:
    """ Updates the run.vbs file with the settings from the .ini file. """
    __setup_script('run-vbs', VBS_DATA)


if __name__ == '__main__':
    setup_sh()
    setup_vbs()
