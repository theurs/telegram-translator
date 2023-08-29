#!/usr/bin/env python3


import platform as platform_module


def platform() -> str:
    """
    Return the platform information.
    """
    return platform_module.platform()


if __name__ == '__main__':
    pass