'''OpenGL extension OES.vertex_array_object

This module customises the behaviour of the 
OpenGL.raw.GLES2.OES.vertex_array_object to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension introduces vertex array objects which encapsulate
	vertex array states on the server side (vertex buffer objects).
	These objects aim to keep pointers to vertex data and to provide
	names for different sets of vertex data. Therefore applications are
	allowed to rapidly switch between different sets of vertex array
	state, and to easily return to the default vertex array state.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/vertex_array_object.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.OES.vertex_array_object import *
from OpenGL.raw.GLES2.OES.vertex_array_object import _EXTENSION_NAME

def glInitVertexArrayObjectOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glDeleteVertexArraysOES.arrays size not checked against n
glDeleteVertexArraysOES=wrapper.wrapper(glDeleteVertexArraysOES).setInputArraySize(
    'arrays', None
)
# INPUT glGenVertexArraysOES.arrays size not checked against n
glGenVertexArraysOES=wrapper.wrapper(glGenVertexArraysOES).setInputArraySize(
    'arrays', None
)
### END AUTOGENERATED SECTION