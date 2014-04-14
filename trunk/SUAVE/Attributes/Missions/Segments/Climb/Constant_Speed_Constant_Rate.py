
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# python imports
import numpy as np

# SUAVE imports
from Unknown_Throttle import Unknown_Throttle

# import units
from SUAVE.Attributes import Units
km = Units.km
hr = Units.hr
deg = Units.deg

# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------

class Constant_Speed_Constant_Rate(Unknown_Throttle):

    # ------------------------------------------------------------------
    #   Data Defaults
    # ------------------------------------------------------------------  
    
    def __defaults__(self):
        self.tag = 'Constant Mach, Constant Altitude Cruise'
        
        # --- User Inputs
        
        self.altitude_start = 1.  * km
        self.altitude_end   = 10. * km
        self.climb_rate     = 3.  * deg
        self.air_speed      = 100 * Units.m / Units.s
        
        return

    # ------------------------------------------------------------------
    #   Methods For Initialization
    # ------------------------------------------------------------------  
    
    def check_inputs(self):
        """ Segment.check():
            error checking of segment inputs
        """
        
        ## CODE
        
        return

    def initialize_conditions(self,conditions,differentials,initials=None):
        
        # initialize time and mass
        # initialize altitude, atmospheric conditions,
        # climb segments are discretized on altitude
        conditions = Unknown_Throttle.initialize_conditions(self,conditions,differentials,initials)
        
        # unpack user inputs
        air_speed   = self.air_speed
        climb_rate  = self.climb_rate
        
        # process velocity vector
        v_mag = air_speed
        v_z   = -climb_rate # z points down
        v_x   = np.sqrt( v_mag**2 - v_z**2 )
        conditions.frames.inertial.velocity_vector[:,0] = v_x
        conditions.frames.inertial.velocity_vector[:,2] = v_z
        
        # freestream conditions
        # freestream.velocity, dynamic pressure, mach number, ReL
        conditions = self.compute_freestream(conditions)
        
        return conditions
        
