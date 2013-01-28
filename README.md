# HoudiniSublime
### A Sublime Text 2 plugin

Send selected Python code snippets to Houdini via a hrpyc

----------

### Installation

1. clone this repo into the `SublimeText2 -> Preference -> Browse Packages` directory:  
`git clone git://github.com/com48/HoudiniSublime.git`

2. Edit the `HoudiniSublime.sublime-settings` file, setting the port to match the port you have used to open your Server in Houdini

3. Optionally edit the keymap file to change the default hotkey from `ctrl+return` to something else.

### Usage

Simply select some code in python script, and hit `ctrl+return`. 
A socket conncetion will be made to a running Houdini instance on the configured port and the code will be 
run in Houdini's environment.

As an example, if you want to open a hrpyc server, you can do the following:

```python
import hrpyc
hrpyc.start_server()

```

Based of the code can be found here.
https://github.com/justinfx/MayaSublime

and the exec idea came from.
https://github.com/vhyza/exec-in-window

