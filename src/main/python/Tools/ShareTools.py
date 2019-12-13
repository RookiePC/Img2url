"""
MIT License

Copyright (c) 2019 RookiePC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import datetime
import os


def get_timestamp():
    """
    returns a local timestamp string
    :return: string with format yy-mm-dd-HH-MM-SS
    """
    return datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')


def get_date():
    """
    returns a local date
    :return: string, formatted time in yy-mm-dd
    """
    return datetime.datetime.now().strftime('%y-%m-%d')


def get_default_path() -> str:
    """
    returns the default path for config files to store
    checks the path on each call, will create one if doesn't exists
    :return: the default path (existence checked)
    """
    default_path = os.path.expanduser('~') + os.path.sep + 'img2url'
    if not os.path.exists(default_path):
        os.mkdir(default_path)
    return default_path
