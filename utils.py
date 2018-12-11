# coding:utf-8

import ctypes
import inspect
import struct
import os
import sys


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def real_length(s: str):
    length = len(s)
    utf8_length = len(s.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def wrap_data(data):
    return struct.pack('<i', len(data)) + data


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
