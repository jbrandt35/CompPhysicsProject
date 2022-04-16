from Equations import *
import numpy as np
from scipy.linalg import lu_factor, lu_solve


def get_orbit_params(objects):
    for object in objects:
        #extract orbit from object instance
        orbit = object.position_history
        #Project data into ecliptic - remove this line when doing 3D comparisons

        plane = fit_plane(orbit)
        inclination = get_inclination(plane)

        data = []
        new_basis = gram_schmidt(get_plane_basis(plane))
        lu, piv = lu_factor(new_basis)
        for point in orbit:
            transformed_point = lu_solve((lu, piv), point)
            data.append(transformed_point)

        data = project_into_ecliptic(data)
        ellipse = fit_ellipse(data)
        semi_major_axis, semi_minor_axis, theta, eccentricity = get_ellipse_params(ellipse)

        object.semi_major = semi_major_axis
        object.semi_minor = semi_minor_axis
        object.eccentricity = eccentricity
        object.rotation = theta
        object.inclination = inclination


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

    eccentricity = np.sqrt(1 - (b / a) ** 2)

    return (a, b, theta, eccentricity)


def fit_plane(orbit):

    #Find the coefficients A,B of the form Ax + By = -z to fit a plane passing through the origin to the data

    x, y, z = split_xyz(orbit) / constants.au.value

    A = np.column_stack((x,y))
    b = -z

    coefficients = np.append(np.linalg.lstsq(A, b, rcond=None)[0], 1.0)

    return coefficients


def get_inclination(coefficients):

    A, B, C = coefficients

    N = np.array([A, B, C])
    n = N / magnitude(N)

    cos_i = np.abs(n[2])

    return np.degrees(np.arccos(cos_i))


def fit_ellipse(orbit):
    x, y = get_x(orbit) / constants.au.value, get_y(orbit) / constants.au.value

    b = -(x ** 2)
    A = np.column_stack((y ** 2, x * y, x, y, np.ones(len(x))))

    coefficients = np.linalg.lstsq(A, b, rcond=None)[0]

    return coefficients


def gram_schmidt(A):
    Q, R = np.linalg.qr(A)
    return Q


def get_plane_basis(coefficients):
    A, B, C = coefficients

    v1 = np.array([A, B, C])
    v2 = np.array([-B/A, 1, 0])
    v3 = np.array([-C/A, 0, 1])

    return np.column_stack((v2, v3, v1))


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


def get_z(data):
    z = []
    for i in range(len(data)):
        z.append(data[i][2])
    return np.array(z, float)


def split_xyz(data):
    x = get_x(data)
    y = get_y(data)
    z = get_z(data)

    return np.array(x), np.array(y), np.array(z)


#Cuts off z-coordinate
def project_into_ecliptic(data):
    projection = []
    for i in range(len(data)):
        projection.append(data[i][0:2])
    return projection


def get_match(sim_properties, real_properties):

    average_percent_error = np.average(np.abs(sim_properties - real_properties) / real_properties)

    return 1 - average_percent_error


