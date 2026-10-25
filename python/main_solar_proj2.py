import glfw
from OpenGL.GL import (
  GL_COLOR_BUFFER_BIT,
  GL_CULL_FACE,
  GL_DEPTH_BUFFER_BIT,
  GL_DEPTH_TEST,
  GL_TRUE,
  glClear,
  glClearColor,
  glEnable,
)
from pathlib import Path

from camera3d import Camera3D
from cut_plane import CutPlane
from light import Light
from material import Material
from moon_camera import MoonCameraRig
from node import Node
from orbital_motion import OrbitalMotion
from scene import Scene
from shader import Shader
from skybox import SkyBox
from sphere import Sphere
from texcube import TexCube
from texture import Texture
from transform import Transform

overview_camera = None
surface_camera = None
current_camera = None
world_scene = None
section_plane = None
earth_anchor = None
moon_anchor = None
planet_shader = None
relief_shader = None
sun_shader = None
star_shader = None
sun_light = None


def _material(ambient, diffuse, specular, shininess):
  material = Material()
  material.SetAmbient(*ambient)
  material.SetDiffuse(*diffuse)
  material.SetSpecular(*specular)
  material.SetShininess(shininess)
  return material


def handle_key(win, key, scancode, action, mods):
  global current_camera

  if action != glfw.PRESS:
    return

  if key in (glfw.KEY_Q, glfw.KEY_ESCAPE):
    glfw.set_window_should_close(win, glfw.TRUE)
  elif key == glfw.KEY_C:
    if current_camera is overview_camera:
      current_camera = surface_camera
      print("Câmera: superfície da Terra -> Lua")
    else:
      current_camera = overview_camera
      print("Câmera: visão orbital")
  elif key == glfw.KEY_X:
    active = section_plane.switch()
    print("Corte no Sol:", "ligado" if active else "desligado")


def draw_frame():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  world_scene.Render(current_camera)


def advance(dt):
  world_scene.Update(dt)


def build_scene():
  global overview_camera, surface_camera, current_camera
  global world_scene, section_plane, earth_anchor, moon_anchor
  global planet_shader, relief_shader, sun_shader, star_shader, sun_light

  glClearColor(0.006, 0.009, 0.020, 1.0)
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)

  project_root = Path(__file__).resolve().parent.parent

  planet_shader = Shader(space="world")
  planet_shader.AttachVertexShader(project_root / "shaders/solar/planet_vertex.glsl")
  planet_shader.AttachFragmentShader(project_root / "shaders/solar/planet_fragment.glsl")
  planet_shader.Link()

  relief_shader = Shader(space="world")
  relief_shader.AttachVertexShader(project_root / "shaders/solar/relief_vertex.glsl")
  relief_shader.AttachFragmentShader(project_root / "shaders/solar/relief_fragment.glsl")
  relief_shader.Link()

  sun_shader = Shader(space="world")
  sun_shader.AttachVertexShader(project_root / "shaders/solar/star_vertex.glsl")
  sun_shader.AttachFragmentShader(project_root / "shaders/solar/star_fragment.glsl")
  sun_shader.Link()

  star_shader = Shader(space="world")
  star_shader.AttachVertexShader(project_root / "shaders/solar/starfield_vertex.glsl")
  star_shader.AttachFragmentShader(project_root / "shaders/solar/starfield_fragment.glsl")
  star_shader.Link()

  overview_camera = Camera3D(18.0, 10.0, 26.0)
  overview_camera.SetCenter(0.0, 0.0, 0.0)
  overview_camera.SetUpDir(0.0, 1.0, 0.0)
  overview_camera.SetAngle(44.0)

  surface_camera = Camera3D(0.0, 0.0, 0.0)
  surface_camera.SetUpDir(0.0, 1.0, 0.0)
  surface_camera.SetAngle(55.0)
  current_camera = overview_camera

  sun_light = Light(0.0, 0.0, 0.0, 1.0, "world")
  sun_light.SetAmbient(0.18, 0.20, 0.24)
  sun_light.SetDiffuse(1.0, 0.96, 0.88)
  sun_light.SetSpecular(0.85, 0.92, 1.0)

  section_plane = CutPlane("cutPlane", 0.62, 0.78, 0.0, 0.0)

  sun_texture = Texture("decal", project_root / "images/sun_texture.jpg")
  earth_texture = Texture("decal", project_root / "images/earth.jpg")
  earth_relief = Texture("normalMap", project_root / "images/earth-normal.png")
  venus_texture = Texture("decal", project_root / "images/venus_texture.jpg")
  moon_texture = Texture("decal", project_root / "images/moon_texture.jpg")
  moon_relief = Texture("normalMap", project_root / "images/moon_normal.png")
  sky_texture = TexCube("skybox", project_root / "images/a.jpg")

  sun_mesh = Sphere(72, 72)
  earth_mesh = Sphere(52, 52)
  venus_mesh = Sphere(44, 44)
  moon_mesh = Sphere(36, 36)
  sky_mesh = SkyBox()

  sun_material = _material((1.0, 0.82, 0.34), (1.0, 0.91, 0.52), (1.0, 0.96, 0.82), 64.0)
  earth_material = _material((0.18, 0.25, 0.36), (0.70, 0.83, 1.0), (0.45, 0.60, 0.85), 48.0)
  venus_material = _material((0.38, 0.30, 0.18), (0.93, 0.76, 0.45), (0.75, 0.62, 0.38), 56.0)
  moon_material = _material((0.22, 0.23, 0.27), (0.68, 0.69, 0.72), (0.12, 0.14, 0.18), 12.0)

  sun_radius = 2.8
  venus_radius = 0.66
  earth_radius = 0.78
  moon_radius = 0.28

  venus_orbit_radius = 7.0
  earth_orbit_radius = 14.0
  moon_orbit_radius = 1.9

  sun_scale = Transform()
  sun_scale.Scale(sun_radius, sun_radius, sun_radius)
  sun_spin = Transform()

  venus_orbit = Transform()
  venus_orbit.Rotate(215.0, 0.0, 1.0, 0.0)
  venus_offset = Transform()
  venus_offset.Translate(venus_orbit_radius, 0.0, 0.0)
  venus_scale = Transform()
  venus_scale.Scale(venus_radius, venus_radius, venus_radius)
  venus_spin = Transform()

  earth_orbit = Transform()
  earth_orbit.Rotate(40.0, 0.0, 1.0, 0.0)
  earth_offset = Transform()
  earth_offset.Translate(earth_orbit_radius, 0.0, 0.0)
  earth_scale = Transform()
  earth_scale.Scale(earth_radius, earth_radius, earth_radius)
  earth_spin = Transform()
  earth_tilt = Transform()
  earth_tilt.Rotate(24.0, 0.0, 0.0, 1.0)

  moon_orbit = Transform()
  moon_orbit.Rotate(130.0, 0.0, 1.0, 0.0)
  moon_offset = Transform()
  moon_offset.Translate(moon_orbit_radius, 0.0, 0.0)
  moon_scale = Transform()
  moon_scale.Scale(moon_radius, moon_radius, moon_radius)
  moon_spin = Transform()

  sun_body = Node(trf=sun_spin, apps=[sun_material, sun_texture, section_plane], shps=[sun_mesh])
  sun_node = Node(shader=sun_shader, trf=sun_scale, nodes=[sun_body])

  venus_body = Node(trf=venus_scale, apps=[venus_material, venus_texture], shps=[venus_mesh])
  venus_spin_node = Node(trf=venus_spin, nodes=[venus_body])
  venus_anchor = Node(trf=venus_offset, nodes=[venus_spin_node])
  venus_branch = Node(trf=venus_orbit, nodes=[venus_anchor])

  moon_body = Node(trf=moon_scale, apps=[moon_material, moon_texture, moon_relief], shps=[moon_mesh])
  moon_spin_node = Node(trf=moon_spin, nodes=[moon_body])
  moon_anchor = Node(trf=moon_offset, nodes=[moon_spin_node])
  moon_orbit_node = Node(trf=moon_orbit, nodes=[moon_anchor])

  earth_body = Node(trf=earth_scale, apps=[earth_material, earth_texture, earth_relief], shps=[earth_mesh])
  earth_spin_node = Node(trf=earth_spin, nodes=[earth_body])
  earth_tilt_node = Node(trf=earth_tilt, nodes=[earth_spin_node])
  earth_anchor = Node(trf=earth_offset, shader=relief_shader, nodes=[earth_tilt_node, moon_orbit_node])
  earth_branch = Node(trf=earth_orbit, nodes=[earth_anchor])

  sky_node = Node(shader=star_shader, apps=[sky_texture], shps=[sky_mesh])

  root = Node(planet_shader, nodes=[sky_node, earth_branch, venus_branch, sun_node])

  world_scene = Scene(root)
  world_scene.SetLight(sun_light)

  world_scene.AddEngine(
    OrbitalMotion(
      sun_spin=sun_spin,
      earth_orbit=earth_orbit,
      earth_spin=earth_spin,
      moon_orbit=moon_orbit,
      moon_spin=moon_spin,
      venus_orbit=venus_orbit,
      venus_spin=venus_spin,
      sun_spin_speed=8.0,
      earth_orbit_speed=7.5,
      earth_spin_speed=50.0,
      moon_orbit_speed=40.0,
      moon_spin_speed=80.0,
      venus_orbit_speed=12.5,
      venus_spin_speed=40.0,
    )
  )

  world_scene.AddEngine(
    MoonCameraRig(
      camera=surface_camera,
      earth_node=earth_anchor,
      moon_node=moon_anchor,
      eye_lift=earth_radius * 1.03,
    )
  )


def run():
  if not glfw.init():
    return

  glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
  glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
  glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
  glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

  win = glfw.create_window(1120, 800, "Projeto 2 - Sistema Solar 3D", None, None)
  if not win:
    glfw.terminate()
    return

  glfw.set_key_callback(win, handle_key)
  glfw.make_context_current(win)

  build_scene()
  print("Controles: C = câmera orbital/superfície | X = corte no Sol | Q/ESC = sair")

  previous = glfw.get_time()
  while not glfw.window_should_close(win):
    now = glfw.get_time()
    dt = min(now - previous, 0.05)
    previous = now

    advance(dt)
    draw_frame()
    glfw.swap_buffers(win)
    glfw.poll_events()

  glfw.terminate()


if __name__ == "__main__":
  run()
