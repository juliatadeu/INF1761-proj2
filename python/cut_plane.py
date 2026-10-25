import glm
from OpenGL.GL import *
from appearance import Appearance


class CutPlane(Appearance):
  def __init__(self, uniform_name, x, y, z, offset=0.0):
    self.uniform_name = uniform_name
    self.normal = glm.normalize(glm.vec3(x, y, z))
    self.offset = offset
    self.active = False

  def switch(self):
    self.active = not self.active
    return self.active

  def configure(self, x, y, z, offset=0.0):
    self.normal = glm.normalize(glm.vec3(x, y, z))
    self.offset = offset

  def _equation(self):
    return glm.vec4(self.normal.x, self.normal.y, self.normal.z, self.offset)

  def Load(self, st):
    shader = st.GetShader()
    if self.active:
      shader.SetUniform(self.uniform_name, self._equation())
      glEnable(GL_CLIP_DISTANCE0)
    else:
      shader.SetUniform(self.uniform_name, glm.vec4(0.0, 0.0, 0.0, 1.0))
      glDisable(GL_CLIP_DISTANCE0)

  def Unload(self, st):
    glDisable(GL_CLIP_DISTANCE0)
