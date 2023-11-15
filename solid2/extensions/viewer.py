import pathlib
import tempfile
import uuid
import subprocess

from .. import config
from ..core.scad_render import scad_render_to_file

class Viewer():
    """
    Creates a temporary .scad file containing the file rendered as Openscad and
    then executes OpenSCAD, opening the file.  
    """
    def __init__(self, shape=None, fn=16):
        self.fn = fn
        self.id = uuid.uuid4()
        self.filepath = pathlib.Path(tempfile.gettempdir())/f"{self.id}.scad"
        self.openWindow()
        if shape != None:
            self.update(shape)
    
    def __repr__(self):
        return f"OpenSCAD viewer {self.id}"

    def openWindow(self):
        comm = [config.openscad_exec_path, self.filepath]
        self.openscad_window = subprocess.Popen(comm)        

    def update(self, shape):
        if self.openscad_window.poll() != None: # if None, it still runs
            self.openWindow()
        scad_render_to_file(shape, self.filepath, file_header=f"$fn = {self.fn};")
        return self.__repr__()
