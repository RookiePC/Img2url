# Img2url

A simple desktop for image inserting while writing markdown files.      
When triggerd, this little application grab the image in clipboard, upload it to seafile server, get the share link, and format the url with pre-defined(custimizable) format string, and copy it to clipboar or replace the trigger keyword you just inputed in markdown file.

# Features
- completely custimizable paste format for image url
- supports hot-key trigger and keyword trigger, both hot-key and key-word are custimizeable.
- cute floating dektop tool notification on current state.

# Known limitations
* Grab image from clipboard only supports Windows/MacOS (for now)
* Has to authenticate the application on MacOS or won't be able to listen to keyboard event.

# Specail Thanks
- UI writes with [PySide2](https://pypi.org/project/PySide2/)
- hook key board events writing with Python module [keyboard](https://github.com/boppreh/keyboard)
