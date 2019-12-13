# Img2url

A simple desktop for image inserting while writing markdown files.      
When triggerd, this little application grab the image in clipboard, upload it to seafile server, get the share link, and format the url with pre-defined(custimizable) format string, and copy it to clipboar or replace the trigger keyword you just inputed in markdown file.

<center>

![example_1](http://thomaslulu.com:8000/f/0d3a02afa744486b8015/?dl=1)<br /><font color="#757575" size =1>example</font>
</center>

# Development & Dependencies
- Python 3.6.8
- PyQt5 5.13.0
- requests 2.22.0
- pyperclip 1.7.0
- keyboard 0.13.3
- pillow 6.1.0
- pyqt5-tools 5.13.0.1.5 ( **For resource compile only, Not necessary**)
- fbs 0.8.3 ( **For deploy only, Not necessary** )

# Start Contributing the Project on Your System
## If you need to use the fbs to build the project and deploy
1. Make sure you've installed dependencies listed above. (Module versions' not restricted, excluding PyQt5 and Python itself)
2. Create a Startup project with fbs, run command `fbs startproject` or `python -m fbs startproject`, answers a few question, and the fbs will generate the structured sample project for you under the working directory.
3. Clone the project to your system, extract the files into the sample project you've just created( Overwrite of course).
4. Start your Python IDE to run `main.py` or use command `fbs run`(in the same path when you executes the create command) or `python -m fbs run`

## If no need for deployment.
1. Follow the Step1 up above.
2. Clone the project to your system and extract all files into wherever you like.
3. Start your Python IDE to run `img2url.py`.

# Features
- Completely **custimizable paste format** for image url
- Supports **hot-key trigger** and **keyword trigger**, both hot-key and key-word are custimizeable.
- **Cute** floating dektop tool notification on current state.
- **Migrates** images in makrdown files to another server or keep them local
- support insert images **offline** and **resubmit** them all to server later

# Known limitations
* Grab image from clipboard only supports Windows/MacOS (for now)
* Has to authenticate the application on MacOS or won't be able to listen to keyboard event.(Run as administrator)
* Specials keys like @# or symbols in key word is not supported for now on MacOS.

# Special Thanks
- UI writes with [PyQt5](https://pypi.org/project/PyQt5/)
- hook key board events writing with Python module [keyboard](https://github.com/boppreh/keyboard)
- key events listen and keyboard control module [pynput](https://github.com/moses-palmer/pynput)
