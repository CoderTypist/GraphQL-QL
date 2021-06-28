import platform
from typing import List

WINDOWS = 0
LINUX = 1
WSL = 2


class InvalidTargetException(Exception):
    def __init__(self, source, target):
        message = f'{str_platform(source)} cannot target {str_platform(target)}'
        super().__init__(message)


class UnknownPlatformException(Exception):
    def __init__(self, message="Could not determine platform"):
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


def str_platform(p) -> str:
    if WINDOWS == p:
        return 'Windows'
    elif WSL == p:
        return 'WSL'
    elif LINUX == p:
        return 'Linux'
    else:
        raise UnknownPlatformException()


def win_or_linux():
    p = get_platform()

    if WINDOWS == p:
        return WINDOWS
    if WSL == p or LINUX == p:
        return LINUX


# a wrapper for subprocess()
def smartprocess(target: int, args: List):

    p = get_platform()

    if WINDOWS == p:
        if WINDOWS == target:
            pass
        elif WSL == target or LINUX == target:
            pass
        else:
            raise UnknownPlatformException()

    elif WSL == p:
        if WINDOWS == target:
            pass
        elif WSL == target or LINUX == target:
            pass
        else:
            raise UnknownPlatformException()

    elif LINUX == p:
        if WINDOWS == target or WSL == target:
            raise InvalidTargetException(p, target)
        elif LINUX == target:
            pass
        else:
            raise UnknownPlatformException()

    else:
        raise UnknownPlatformException()
