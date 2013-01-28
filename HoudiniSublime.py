import sublime, sublime_plugin  
import time
import re
import traceback
import sys
import os

_settings = {
    'host' : '127.0.0.1',
    'py_port' : 18811
}

#!/usr/bin/python2.6
def enableHouModule():
    '''Set up the environment so that "import hou" works.'''
    import sys, os

    try:
        import hou
    except ImportError:
        # Add $HFS/houdini/python2.6libs to sys.path so Python can find the
        # hou module.
        paths = ['/usr/lib/python2.6',os.environ['HFS'] + "/houdini/python%d.%dlibs" % sys.version_info[:2]]
        for path in paths:
            if not path in sys.path:
                sys.path.append(path)

enableHouModule()
import hou
import hrpyc

class SendToHoudiniCommand(sublime_plugin.TextCommand):
    
    def replace(self, edit, region, result):
        "Replace the contents of a region with a result converted to a string."
        self.view.replace(edit, region, str(result))
        
    def run(self, edit, lang="python"):
        host = _settings['host']
        port = _settings['py_port']
        connection, hou = hrpyc.import_remote_module(server= host,port =port)

        for region in self.view.sel():
            try:
                exec self.view.substr(region)
            except:
                traceback.print_exc(0)


def settings_obj():
    return sublime.load_settings("HoudiniSublime.sublime-settings")

def sync_settings():
    global _settings
    so = settings_obj()
    _settings['host'] = so.get('houdini_hostname')
    _settings['py_port'] = so.get('python_command_port')

settings_obj().clear_on_change("HoudiniSublime.settings")
settings_obj().add_on_change("HoudiniSublime.settings", sync_settings)
sync_settings()

