from os import environ
from os.path import join
import sys
import traceback

import sublime
import sublime_plugin

## Settings
settings = sublime.load_settings('HoudiniSublime.sublime-settings')


class Pref:
    def load(self):
        Pref.host = settings.get("houdini_hostname", "127.0.0.1")
        Pref.port = settings.get("python_port", 18811)

Pref = Pref()
Pref.load()
# Setup a callback to reload the setting incase the user changes them.
settings.add_on_change("HoudiniSublime.settings", Pref.load())


def enableHouModule():
    '''Set up the environment so that "import hou" works.'''
    try:
        import hou
    except ImportError:
        # Add $HFS/houdini/python2.6libs to sys.path so Python can find the
        # hou module.
        lib_path = join(environ['HFS'], "python", "lib", "python%d.%d" % (sys.version_info[:2]))
        hou_path = join(environ['HFS'], "houdini", "python%d.%dlibs" % (sys.version_info[:2]))
        paths = [lib_path, hou_path]
        for path in paths:
            if not path in sys.path:
                sys.path.append(path)

enableHouModule()
import hrpyc

# the meat of the potato.
# create the client and exec the selected text. this gives you access to the
# hou object.
class SendToHoudiniCommand(sublime_plugin.TextCommand):
    def run(self):
        connection, hou = hrpyc.import_remote_module(server=Pref.host, port=Pref.port)
        for region in self.view.sel():
            try:
                exec self.view.substr(region)
            except:
                traceback.print_exc(0)
