import platform
import re
import subprocess
from typing import List

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


# a wrapper for subprocess()
# Even if the execution platform changes, you can still run
# the desired shell with little to no change.
# The only thing that may need to be changed is the target.
def shell(target: int, args: List, tab=False, verbose=False) -> str:
    # WINDOWS will default to mean CMD
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

        if CMD == target or WINDOWS == target:
            com = args

        elif POWERSHELL == target:
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


def test():

    print(shell(WINDOWS, ['dir'], tab=True, verbose=True))
    print(shell(CMD, ['dir'], tab=True, verbose=True))
    print(shell(POWERSHELL, ['ls'], tab=True, verbose=True))
    print(shell(WSL, ['ls', '-la'], tab=True, verbose=True))
    print(shell(LINUX, ['ls', '-la'], tab=True, verbose=True))
