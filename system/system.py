import platform
import re
import subprocess
from typing import List
import warnings

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


def get_platform() -> int:
    p = platform.platform().lower()

    if 'windows' in p:
        return WINDOWS
    elif 'microsoft' in p:
        return WSL
    elif 'linux' in p:
        return LINUX
    else:
        return -1


def str_stat(p: int) -> str:
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


def win_or_linux() -> int:

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
    # command to execute in the shell
    com = None
    # output from running com
    ret = None

    if verbose:
        info()

    # if WINDOWS is specific as target, set the target to the default shell
    default_shell = None

    if WINDOWS == target:
        default_shell = win_default_shell()
        target = default_shell

    if WINDOWS == p:
        if CMD == target:
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

        if CMD == target:
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
        if CMD == target or POWERSHELL == target or WSL == target:
            raise InvalidTargetException(p, target)

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


def windows(args: List, tab=False, verbose=False) -> str:
    return shell(WINDOWS, args, tab=tab, verbose=verbose)


def cmd(args: List, tab=False, verbose=False) -> str:
    return shell(CMD, args, tab=tab, verbose=verbose)


def powershell(args: List, tab=False, verbose=False) -> str:
    return shell(POWERSHELL, args, tab=tab, verbose=verbose)


def wsl(args: List, tab=False, verbose=False) -> str:
    return shell(WSL, args, tab=tab, verbose=verbose)


def linux(args: List, tab=False, verbose=False) -> str:
    return shell(LINUX, args, tab=tab, verbose=verbose)


def is_alpha(text: str, extra: List = None) -> bool:

    lower = [chr(_) for _ in range(ord('a'), ord('z')+1)]
    upper = [chr(_) for _ in range(ord('A'), ord('Z')+1)]

    alpha = lower
    alpha.extend(upper)

    if extra:
        alpha.extend(extra)

    for c in text:
        if c not in alpha:
            print('ERROR:', c)
            return False

    return True


# Assumes that the environment variable already exists
def env(target: int, var_name: str) -> str:

    if not is_alpha(var_name, extra=['_']):
        raise Exception('var_name can only contain letters and underscores: ' + var_name)

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
        raise InvalidTargetException(get_platform(), target)

    if var:
        return var.strip()
    else:
        return None



def wenv(var_name: str) -> str:
    return env(WINDOWS, var_name)


def lenv(var_name: str) -> str:
    return env(LINUX, var_name)


# Using denv() is not recommended
# Behavior will change as the platform/default shell changes
# For more predictable behavior, use wenv() or lenv()
def denv(var_name: str) -> str:

    w = '\n\n\tUsing denv() is not recommended due to potential unexpected behavior'
    w += '\n\t\tConsider wenv() for targeting Windows or lenv() for targeting Linux'
    w += '\n\t\tUse env() if the use of a specific shell is required\n'
    warnings.warn(w)
    p = get_platform()
    return env(p, var_name)