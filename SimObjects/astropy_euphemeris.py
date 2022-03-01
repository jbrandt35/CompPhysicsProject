import astropy
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon

solar_system_ephemeris.set('jpl')

#Set time that we want to use from (noting that the 'de432s' is good for 1950 to 2050, and if we go outside we will need to download stuff for 'de430')
t = Time("2014-09-22 23:22")

#Lists all the bodies that the package comes with
print(solar_system_ephemeris.bodies)
#Sample call to get earths position at that time
#'get_body_barycentric' uses the solar system barycenter as reference from, 'get_body' uses earths center of mass
earth_pos = get_body_barycentric('earth',t)
#print(earth_pos)
#print(type(earth_pos))

#Uncomment the line below if you want to see all the methods attached to the 'get_body_barycentric' class
#print(dir(earth_pos))

#Extracts the xyz coordinate from the above class. Note that it is still a class object, but we can do operators on it (haven't figure out how to extract info)
earth_coord = earth_pos.xyz
#print(type(earth_coord[1]))
#print(earth_coord * 3)
earth_pos_x = earth_coord[0]
print(earth_coord,earth_pos_x)

#There is also a method called 'get_body_barycentric_posvel' that we should be able to get the velocities from