#this is global config file for exp_solid
from pathlib import Path
import os
import platform
import sys
import re
import subprocess
import platform

class Config:
    def __init__(self):
        self.use_implicit_builtins = "--implicit" in sys.argv

        self.enable_pickle_cache = True
        self.pickle_cache_dir = self.get_pickle_cache_dir()

        self.openscad_library_paths = self.get_openscad_library_paths()

        self.openscad_exec_path = self.get_openscad_exec()
        if self.openscad_exec_path == None:
            self.pretty_viewer = False
        else:
            self.pretty_viewer = True

    def get_openscad_exec(self):
        """
        Check for openscad path and return path if successful. Else return None."""
        try:
            openscad_exec = os.environ["OPENSCAD_EXEC"]
            subprocess.run([openscad_exec_path, "--version"])
            return openscad_exec_path
        except (KeyError, FileNotFoundError):
            pass

        try:
            openscad_exec_path = "openscad"
            subprocess.run([openscad_exec_path, "--version"])
            return openscad_exec_path
        except FileNotFoundError:
            pass
        
        try:
            openscad_exec_path = "openscad-nightly"
            subprocess.run([openscad_exec_path, "--version"])
            return openscad_exec_path
        except FileNotFoundError:
            pass

        if "Windows" in platform.platform():
            try:
                openscad_exec_path = r"C:\Program Files\OpenSCAD\openscad.exe"
                subprocess.run([openscad_exec_path, "--version"])
                return openscad_exec_path
            except FileNotFoundError:
                pass

        openscad_exec_path = None
        return openscad_exec_path

    def get_openscad_library_paths(self):
        """
        Return system-dependent OpenSCAD library paths or paths defined in
        os.environ['OPENSCADPATH'] """
        paths = [Path('.')]

        user_path = os.environ.get('OPENSCADPATH')
        if user_path:
            for s in re.split(r'\s*[;:]\s*', user_path):
                paths.append(Path(s))

        #user wide path
        default_paths = {
            'Linux':   Path.home() / '.local/share/OpenSCAD/libraries',
            'Darwin':  Path.home() / 'Documents/OpenSCAD/libraries',
            'Windows': Path('My Documents/OpenSCAD/libraries')
        }

        paths.append(default_paths[platform.system()])

        #system wide paths
        if platform.system() == 'Linux':
            #sorry, but I've no clue what the paths are on other operating systems
            paths.append(Path("/usr/share/openscad/libraries"))

        return paths

    def get_pickle_cache_dir(self):
        default_paths = {
            'Linux':   Path.home() / '.local/share/expSolidPython/pickle_cache',
            'Darwin':  Path.home() / 'Documents/expSolidPython/pickle_cache',
            'Windows': Path('My Documents/expSolidPython/pickle_cache')
        }
        return default_paths[platform.system()]


config = Config()

