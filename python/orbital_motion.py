from engine import Engine


class OrbitalMotion(Engine):
  def __init__(
    self,
    *,
    sun_spin,
    earth_orbit,
    earth_spin,
    moon_orbit,
    moon_spin,
    venus_orbit,
    venus_spin,
    sun_spin_speed=8.0,
    earth_orbit_speed=7.5,
    earth_spin_speed=50.0,
    moon_orbit_speed=40.0,
    moon_spin_speed=80.0,
    venus_orbit_speed=12.5,
    venus_spin_speed=40.0,
  ):
    self._motions = (
      (moon_spin, moon_spin_speed),
      (venus_spin, venus_spin_speed),
      (earth_spin, earth_spin_speed),
      (sun_spin, sun_spin_speed),
      (moon_orbit, moon_orbit_speed),
      (venus_orbit, venus_orbit_speed),
      (earth_orbit, earth_orbit_speed),
    )

  def Update(self, dt: float):
    for transform, degrees_per_second in self._motions:
      transform.Rotate(degrees_per_second * dt, 0, 1, 0)
