from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric_posvel, get_body
import numpy as np

#t is just the time we are initializing, and the line below sets what ephemeris the code will use. There are a couple different options for that
t = Time("2022-04-27 23:22")
solar_system_ephemeris.set('jpl')

#This returns a class object tuple, the first part the position in km (x,y,z), and the second the velocity in km/d (x,y,z); still don't know what the d is.
earth = get_body_barycentric_posvel('earth',t)

#first part prints the methods we can use on earth (note that there are a couple other functions we can use to get the position like just get_body)
EarthCoords = np.array(earth[0].get_xyz())
print(EarthCoords)
print(type(EarthCoords))