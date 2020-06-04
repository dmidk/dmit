#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for the Van Ulden and Holtslag 1983 paper:
A. A. M. Holtslag and A. P. Van Ulden, "A Simple Scheme for Daytime
Estimates of the Surface Fluxes from Routine Weather Data", Journal of climate
and applied meteorology, 1983, Vol. 22, No. 4.

"""
import numpy as np
import datetime as dt

__author__ = "Kasper Hintz"
__credits__ = ["A. A. M. Holtslag", "A. P. Van Ulden"]
__version__ = "0.1"
__email__ = "kah@dmi.dk"



def rad_to_deg(rad):
    """
    Convert radians to degrees
    :param rad: radians
    :type rad: float, list
    :return: degrees
    :rtype: float or numpy array
    """
    deg = rad * 180. / np.pi
    return deg


def deg_to_rad(deg):
    """Constructor method
    """
    rad = deg * np.pi / 180.
    return rad


def solar_elevation(M, D, H, lon, lat):
    """
    Inputs
    M      ::  Month of year (1-12)
    D      ::  Day of month (1-31)
    H      ::  Hour of day in UTC
    lon    ::  Longitude in degrees

    Parameters
    SL     ::  Solar longitude
    delta  ::  Solar declination
    h      ::  hour angle

    Returns
    phi    :: solar_elevation in rad
    """

    lon = deg_to_rad(lon)
    lat = deg_to_rad(lat)

    d = 30 * (M - 1) + D

    SL = 4.871 + 0.0175 * d + 0.033 * np.sin(0.017 * d)
    delta = np.arcsin(0.398 * np.sin(SL))

    h = -lon + 0.043 * np.sin(2 * SL) - 0.033 * \
        np.sin(0.0175 * d) + 0.262 * H - np.pi

    sin_phi = np.sin(delta) * np.sin(lat) + \
        np.cos(delta) * np.cos(lat) * np.cos(h)
    phi = np.arcsin(sin_phi)
    #phi_deg = rad_to_deg(np.arcsin(sin_phi))
    return phi


def incoming_solar_radiation(phi, cloudcover):
    """
    Inputs
    phi         :: Solar elevation in rad
    cloudcover  ::  Total cloudcover in percentage (0-1)

    Returns
    K  ::  Incoming solar radiation in W/m^2
    """

    # Using constants from De Bilt measurements
    a1 = 1041  # W/m^2
    a2 = -69  # W/m^2
    # Using constants from Hamburg measurements
    b1 = -0.75
    b2 = 3.4

    K0 = a1 * np.sin(phi) + a2

    if cloudcover == 0:
        K = K0

    if cloudcover > 0:
        N = cloudcover

        if N > 1:
            N = 1
            # print('WARNING: cloudcover was above 1 - setting to 1 (100 %)')

        K = K0 * (1 + b1 * N**b2)

    return K


def net_radiation(K, cloudcover, T, albedo=0.23):
    """
    Inputs
    K          :: Incoming solar radiation
    cloudcover :: In percent (0-1)
    T          :: Temperature (Kelvin)

    Parameters:
    L_plus    :: Incoming longwave
    L_minus   :: Outgoing longwave

    Returns
    Q  ::  Net radiation in W/m^2
    """

    if cloudcover > 1:
        cloudcover = 1
    if cloudcover < 0:
        cloudcover = 0

    c1 = 5.31 * 10**(-13)  # W m**-2 K**-6
    c2 = 60  # W m**-2
    c3 = 0.12
    sigma = 5.67 * 10**(-8)  # W m**-2 K**-4 Stefan Boltzmann constant

    L_plus = c1 * T**6 + c2 * cloudcover
    #L_minus = sigma * T**4 + c3*Q

    Q = ((1 - albedo) * K + L_plus - sigma * T**4) / (1 + c3)

    return Q


def surface_energy_budget(Q, T):
    """
    Inputs
    Q  :: Net Radiation
    T  :: Temperature in Kelvin

    Returns
    H  ::  Sensible Heat Flux
    E  ::  Latent Heat Flux
    G  ::  Soil Heat Flux
    """
    cg = 0.1
    G = cg * Q

    Q_remain = Q - G

    alpha = 1  # W m**-2 (Grass Surface)
    B = 20  # W m**-2 (Grass Surface)
    gamma_s = gamma_s_table(T - 273.15)

    # Eq. 14
    H = ((1 - alpha) + gamma_s) / (1 + gamma_s) * Q_remain - B
    # Eq. 15
    E = alpha / (1 + gamma_s) * Q_remain + B

    return H, E, G


def gamma_s_table(T):
    """
    Table 5 from Holtslag and Van Ulden 1983
    Input: T in Celcius
    """
    base = 5
    Tb = base * round(T / base)
    if Tb < -5:
        Tb = -5
    if Tb > 35:
        Tb = 35

    if Tb == -5:
        gamma_s = 2.01
    if Tb == 0:
        gamma_s = 1.44
    if Tb == 5:
        gamma_s = 1.06
    if Tb == 10:
        gamma_s = 0.79
    if Tb == 15:
        gamma_s = 0.60
    if Tb == 20:
        gamma_s = 0.45
    if Tb == 25:
        gamma_s = 0.35
    if Tb == 30:
        gamma_s = 0.27
    if Tb == 35:
        gamma_s = 0.21

    return gamma_s


def momemtum_flux_and_obukhov_length(U, z, z0, T, H):
    """
    Inputs
    U  :: Wind Speed at height z
    z  :: Height of measured wind speed
    z0 :: Roughness length
    T  :: Temperature in Kelvin
    H  :: Sensible heat flux

    Returns
    u_star  ::  Friction velocity (momentum flux)
    L       ::  Obukhov length (stability parameter)

    Note: u_star and L is solved in an iterative process
    """

    k = 0.4
    g = 9.81
    rho = 1.225  # kg m**-3 (at 15 degrees)
    cp = 1004  # J * kg**-1 * K**-1

    L_init = -36

    do_proceed = True
    iter = 0
    L = L_init
    while do_proceed:
        iter += 1

        L_old = L

        x = (1 - 16 * z / L)**(1 / 4)
        x0 = (1 - 16 * z0 / L)**(1 / 4)

        phi_m_z = 2 * np.log((1 + x) / 2) + \
            np.log((1 + x**2) / 2) - 2 * np.arctan(x) + np.pi / 2
        phi_m_z0 = 2 * np.log((1 + x0) / 2) + \
            np.log((1 + x0**2) / 2) - 2 * np.arctan(x0) + np.pi / 2

        u_star = k * U * (np.log(z / z0) - phi_m_z + phi_m_z0)**(-1)

        L = - (rho * cp * T * u_star**3) / (k * g * H)

        if abs(1 - L_old / L) < 0.001:
            do_proceed = False

        if not L == L:
            do_proceed = False
            # print('OBUKHOV Length = NAN')

    return u_star, L


def vanulden_stability(dl, lat, lon, cloudcover, temperature, wspd, z, z0):
    """
    Function to collect and return and the Van Ulden
    and Holtslag functions
    Inputs
    dl             :: datetime object of current time
    lat            :: latitude in degress
    lon            :: longitude in degress
    cloudcover     :: percentage 0-1
    temperature    :: Temperature in Kelvin
    wspd           :: wind speed reference observation
    z              :: Elevation of wind measurement (10 m)
    z0             :: Roughness length
    Returns
    u_star         :: Friction velocity
    L              :: Obukhov Length
    """

    M = int(dl.strftime('%-m'))
    D = int(dl.strftime('%-d'))
    H = int(dl.strftime('%-H'))

    phi = solar_elevation(M, D, H, lon, lat)
    K = incoming_solar_radiation(phi, cloudcover)
    Q = net_radiation(K, cloudcover, temperature)

    sens_heat, lat_heat, soil_heat = surface_energy_budget(Q, temperature)

    u_star, L = momemtum_flux_and_obukhov_length(
        wspd, z, z0, temperature, sens_heat)

    return u_star, L


if __name__ == '__main__':

    dl = dt.datetime(2016, 2, 14, 12)

    lon = 10
    lat = 55

    cloudcover = 2 / 8  # Octas
    temperature = 283.15  # K
    U = 8  # m/s
    z = 10  # m
    z0 = 0.1  # m

    u_star, L = dmimet.vanulden_stability(
        dl, lat, lon, cloudcover, temperature, U, z, z0)
    print(u_star, L)
