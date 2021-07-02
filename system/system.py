import platform
import re
import subprocess
from typing import List

OTHER = -1
WINDOWS = 0
CMD = 1
POWERSHELL = 2
LINUX = 3
WSL = 4


class InvalidTargetException(Exception):
    def __init__(self, source, target):
        message = f'{str_stat(source)} cannot target {str_stat(target)}'
        super().__init__(message)


class UnexpectedValueException(Exception):
    def __init__(self, item):
        message = f'Unexpected value: {item}'
        super().__init__(message)


class UnknownPlatformException(Exception):
    def __init__(self, platform):
        message = f'Could not resolve platform: {str(platform)}'
        super().__init__(message)


class UnknownShellException(Exception):
    def __init__(self, shell):
        message = f'Could not resolve shell: {str(shell)}'
        super().__init__(message)


def get_platform():
    p = platform.platform().lower()

    if 'windows' in p:
        return WINDOWS
    elif 'microsoft' in p:
        return WSL
    elif 'linux' in p:
        return LINUX
    else:
        return -1


def str_stat(p) -> str:
    if WINDOWS == p:
        return 'Windows'
    elif CMD == p:
        return 'CMD'
    elif POWERSHELL == p:
        return 'PowerShell'
    elif WSL == p:
        return 'WSL'
    elif LINUX == p:
        return 'Linux'
    elif WSL == p:
        return 'WSL'
    raise UnexpectedValueException(p)


def win_or_linux():

    p = get_platform()

    if WINDOWS == p:
        return WINDOWS
    elif WSL == p or LINUX == p:
        return LINUX
    raise UnknownPlatformException(p)


def win_default_shell() -> int:

    p = get_platform()

    # platform must be Windows
    if WINDOWS != p and WSL != p:
        raise UnknownPlatformException(p)

    default_shell = subprocess.run(['cmd.exe', '/c', 'echo', '%ComSpec%'], stdout=subprocess.PIPE).stdout.decode()

    # remove ending '\n\r'
    default_shell = default_shell[:-2]

    if '\\cmd.exe' == default_shell[-8:]:
        return CMD

    elif '\\powershell.exe' == default_shell[-15:]:
        return POWERSHELL

    # if the default shell was not cmd or powershell
    raise UnknownShellException(default_shell)


# A wrapper for subprocess()
# The only thing that may need to be changed is the target.
def shell(target: int, args: List, tab=False, verbose=False) -> str:

    # On WINDOWS/WSL, LINUX will default to mean WSL

    def info():
        if verbose:
            print()
            print(f'shell(): source: {str_stat(p)}')
            print(f'shell(): target: {str_stat(target)}')
            print()

    p = get_platform()
    com = None
    ret = None

    if verbose:
        info()

    if WINDOWS == p:

        default_shell = win_default_shell()

        if WINDOWS == target:
            target = default_shell

        if CMD == target:
            if CMD == default_shell:
                com = args
            elif POWERSHELL == default_shell:
                com = ['cmd.exe', '/c']
                com.extend(args)
            else:
                raise UnexpectedValueException(default_shell)

        elif POWERSHELL == target:
            if CMD == default_shell:
                com = ['cmd.exe', '/c']
                com.extend(args)
            elif POWERSHELL == default_shell:
                com = args
            else:
                raise UnexpectedValueException(default_shell)

            com = ['powershell.exe']
            com.extend(args)

        elif WSL == target or LINUX == target:
            com = ['wsl']
            com.extend(args)

        else:
            raise UnknownShellException(target)

        ret = subprocess.run(com, shell=True, stdout=subprocess.PIPE).stdout

    elif WSL == p:
        if CMD == target or WINDOWS == target:
            com = ['cmd.exe', '/c']
            com.extend(args)

        elif POWERSHELL == target:
            com = ['powershell.exe']
            com.extend(args)

        elif WSL == target or LINUX == target:
            com = args

        else:
            raise UnknownShellException(target)

        ret = subprocess.run(com, stdout=subprocess.PIPE).stdout

    elif LINUX == p:
        if CMD == target or WINDOWS == target or WSL == target:
            raise InvalidTargetException(p, target, shell=True, stdout=subprocess.PIPE)

        elif LINUX == target:
            com = args

        else:
            raise UnknownShellException(target)

        ret = subprocess.run(com, stdout=subprocess.PIPE).stdout.decode()

    else:
        raise UnknownPlatformException(target)

    if ret:

        text = ret.decode()

        if tab:
            if text[0] != '\t':
                text = '\t' + text
            text = re.sub('\n', '\n\t', text)

        return text

    else:
        return None


def env(target, var_name):

    if WINDOWS == target:
        target = win_default_shell()

    if CMD == target:
        var = shell(CMD, ['echo', '%' + var_name + '%'])
    elif POWERSHELL == target:
        var = shell(POWERSHELL, ['echo', '$env:' + var_name])
    elif WSL == target:
        var = shell(WSL, ['echo', '$' + var_name])
    elif LINUX == target:
        var = shell(LINUX, ['echo', '$' + var_name])
    else:
        raise InvalidTargetException(target)

    if var:
        return var.strip()
    else:
        return None
