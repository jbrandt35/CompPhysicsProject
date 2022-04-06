from Equations import *


def get_orbit_params(objects):
    for object in objects:
        #extract orbit from object instance
        orbit = object.position_history
        #Project data into ecliptic - remove this line when doing 3D comparisons
        data = project_into_ecliptic(orbit)

        x, y = get_x(data)/constants.au.value, get_y(data)/constants.au.value

        b = -(x**2)
        A = np.column_stack((y**2, x*y, x, y, np.ones(len(x))))

        coefficients = np.linalg.lstsq(A, b, rcond=None)[0]

        semi_major_axis, semi_minor_axis, theta = get_ellipse_params(coefficients)

        eccentricity = np.sqrt(1 - (semi_minor_axis/semi_major_axis)**2)

        object.semi_major = semi_major_axis
        object.semi_minor = semi_minor_axis
        object.eccentricity = eccentricity
        object.rotation = theta



def get_ellipse_params(coefficients):

    A = 1
    (C, B, D, E, F) = coefficients

    #a
    first_term = A * (E ** 2) + C * (D ** 2) - B*D*E + (B**2 - 4 * A * C) * F
    second_term = (A + C) + ((A - C) ** 2 + B**2)**(1/2)
    denominator = B**2 - 4 * A * C
    a = -(2 * first_term * second_term)**(1/2) / denominator

    #b
    second_term = (A + C) - ((A - C) ** 2 + B**2)**(1/2)
    b = -(2 * first_term * second_term) ** (1/2) / denominator

    if B != 0.0:
        theta = np.degrees(np.arctan((1/B) * (C - A - np.sqrt((A-C)**2 + B**2))))
    elif B == 0.0 and A < C:
        theta = 0
    elif B == 0.0 and A > C:
        theta = 90

    return (a, b, theta)


def get_x(data):
    x = []
    for i in range(len(data)):
        x.append(data[i][0])
    return np.array(x, float)


def get_y(data):
    y = []
    for i in range(len(data)):
        y.append(data[i][1])
    return np.array(y, float)


#Cuts off z-coordinate
def project_into_ecliptic(data):
    projection = []
    for i in range(len(data)):
        projection.append(data[i][0:2])
    return projection
