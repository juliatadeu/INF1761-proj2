import glm
from engine import Engine


class MoonCameraRig(Engine):
  def __init__(self, camera, earth_node, moon_node, eye_lift=0.0):
    self._camera = camera
    self._earth = earth_node
    self._moon = moon_node
    self._eye_lift = eye_lift

  def Update(self, dt: float):
    earth_pos = glm.vec3(self._earth.GetModelMatrix()[3])
    moon_pos = glm.vec3(self._moon.GetModelMatrix()[3])

    sight = moon_pos - earth_pos
    if glm.length(sight) > 1.0e-6:
      eye = earth_pos + glm.normalize(sight) * self._eye_lift
    else:
      eye = earth_pos

    self._camera.SetEye(eye.x, eye.y, eye.z)
    self._camera.SetCenter(moon_pos.x, moon_pos.y, moon_pos.z)
    self._camera.SetUpDir(0.0, 1.0, 0.0)
