# standard lib imports
from os import environ
from os.path import join
import sys
import traceback

# sublime imports
import sublime
import sublime_plugin

settings = {}

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
    def run(self, edit):
        connection, hou = hrpyc.import_remote_module(server=settings['host'], port=settings['port'])
        for region in self.view.sel():
            try:
                exec self.view.substr(region)
            except:
                traceback.print_exc(0)

                
def settings_obj():
    return sublime.load_settings("HoudiniSublime.sublime-settings")

def sync_settings():
    global settings
    so = settings_obj()
    settings['host'] = so.get('houdini_hostname','127.0.0.1')
    settings['port'] = so.get('python_port',18811)

settings_obj().clear_on_change("HoudiniSublime.settings")
settings_obj().add_on_change("HoudiniSublime.settings", sync_settings)
sync_settings()
