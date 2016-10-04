# cl_p.py
#
# Created:  Aug 2016, A. van Korlaar
# Modified: Aug 2016, L. Kulik

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

def cl_p(cl_alpha, geometry):
    """ output = SUAVE.Methods.Flight_Dynamics.Dynamic_Stablity.Full_Linearized_Equations.Supporting_Functions.cl_p(cl_alpha, geometry)
        Calculating the derivative of rolling moment with respect to roll rate
        Inputs:

        Outputs:

        Assumptions:

        Source:
            STABILITY, USAF. "Control Datcom." Air Force Flight Dynamics Laboratory, Wright-Patterson Air Force Base, Ohio (1972)
    """

    taper = geometry.wings['main_wing'].taper

    # Generating Stability derivative
    cl_p = -(cl_alpha/12.)*((1.+3.*taper)/(1.+taper))

    return cl_p