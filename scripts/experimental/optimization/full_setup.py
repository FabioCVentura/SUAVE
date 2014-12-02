# full_setup.py
# 
# Created:  SUave Team, Aug 2014
# Modified: 

""" setup file for a mission with a 737
"""


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Attributes import Units

import numpy as np
import pylab as plt

import copy, time

from SUAVE.Structure import (
Data, Container, Data_Exception, Data_Warning,
)

# ----------------------------------------------------------------------
#   Vehicle Setup
# ----------------------------------------------------------------------

def full_setup():

    vehicle  = vehicle_setup()
    configs  = configs_setup(vehicle)
    analyses = analyses_setup(configs)
    mission  = mission_setup(analyses)
    
    return vehicle, configs, analyses, mission


# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------

def vehicle_setup():
    
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    
    
    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'Boeing 737-800'    
    
    
    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    

    # mass properties
    vehicle.mass_properties.max_takeoff               = 79015.8   # kg
    vehicle.mass_properties.operating_empty           = 62746.4   # kg
    vehicle.mass_properties.takeoff                   = 79015.8   # kg
    ## vehicle.mass_properties.max_zero_fuel             = 0.9 * vehicle.mass_properties.max_takeoff 
    vehicle.mass_properties.cargo                     = 10000.  * Units.kilogram   
    
    vehicle.mass_properties.center_of_gravity         = [60 * Units.feet, 0, 0]  # Not correct
    vehicle.mass_properties.moments_of_inertia.tensor = [[10 ** 5, 0, 0],[0, 10 ** 6, 0,],[0,0, 10 ** 7]] # Not Correct
    
    # envelope properties
    vehicle.envelope.ultimate_load = 3.5
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area         = 124.862       
    vehicle.passengers             = 170
    vehicle.systems.control        = "fully powered" 
    vehicle.systems.accessories    = "medium range"
    
    
    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------        
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Main Wing'
    
    wing.aspect_ratio            = 10.18
    wing.sweep                   = 25 * Units.deg
    wing.thickness_to_chord      = 0.1
    wing.taper                   = 0.16
    wing.span_efficiency         = 0.9
    
    wing.spans.projected         = 35.66    
    
    wing.chords.root             = 6.81
    wing.chords.tip              = 1.09
    wing.chords.mean_aerodynamic = 12.5
    
    wing.areas.reference         = 124.862 
    ## wing.areas.wetted            = 2.0 * wing.areas.reference
    ## wing.areas.exposed           = 0.8 * wing.areas.wetted
    ## wing.areas.affected          = 0.6 * wing.areas.wetted
    
    wing.twists.root             = 3.0 * Units.degrees
    wing.twists.tip              = 3.0 * Units.degrees
    
    wing.origin                  = [20,0,0]
    wing.aerodynamic_center      = [3,0,0] 
    
    wing.vertical                = False
    wing.symmetric               = True
    
    wing.dynamic_pressure_ratio  = 1.0
    
    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------        
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------        
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Horizontal Stabilizer'
    
    wing.aspect_ratio            = 6.16      #
    wing.sweep                   = 30 * Units.deg
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.4
    wing.span_efficiency         = 0.9
    
    wing.spans.projected         = 14.146      #

    wing.chords.root             = 3.28
    wing.chords.tip              = 1.31    
    wing.chords.mean_aerodynamic = 8.0

    wing.areas.reference         = 32.488    #
    ## wing.areas.wetted            = 2.0 * wing.areas.reference
    ## wing.areas.exposed           = 0.8 * wing.areas.wetted
    ## wing.areas.affected          = 0.6 * wing.areas.wetted
    
    wing.twists.root             = 3.0 * Units.degrees
    wing.twists.tip              = 3.0 * Units.degrees  
    
    wing.origin                  = [50,0,0]
    wing.aerodynamic_center      = [2,0,0]
    
    wing.vertical                = False 
    wing.symmetric               = True
    
    wing.dynamic_pressure_ratio  = 0.9  
    
    # add to vehicle
    vehicle.append_component(wing)
    
    
    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Vertical Stabilizer'    
    
    wing.aspect_ratio            = 1.91      #
    wing.sweep                   = 25 * Units.deg
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.25
    wing.span_efficiency         = 0.9
    
    wing.spans.projected         = 7.877      #    

    wing.chords.root             = 6.60
    wing.chords.tip              = 1.65
    wing.chords.mean_aerodynamic = 8.0
    
    wing.areas.reference         = 32.488    #
    ## wing.areas.wetted            = 2.0 * wing.areas.reference
    ## wing.areas.exposed           = 0.8 * wing.areas.wetted
    ## wing.areas.affected          = 0.6 * wing.areas.wetted
    
    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees  
    
    wing.origin                  = [50,0,0]
    wing.aerodynamic_center      = [2,0,0]    
    
    wing.vertical                = True 
    wing.symmetric               = False
    wing.t_tail                  = False
    
    wing.dynamic_pressure_ratio  = 1.0
        
    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------
    
    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'Fuselage'
    
    #fuselage.number_coach_seats    = vehicle.passengers
    fuselage.seats_abreast         = 6
    fuselage.seat_pitch            = 1
    
    fuselage.fineness.nose         = 1.6
    fuselage.fineness.tail         = 2.
    
    fuselage.lengths.nose          = 6.4
    fuselage.lengths.tail          = 8.0
    fuselage.lengths.cabin         = 44.0
    fuselage.lengths.total         = 58.4    
    fuselage.lengths.fore_space    = 6.
    fuselage.lengths.aft_space     = 5.    
    
    fuselage.width                 = 4.
    
    fuselage.heights.maximum       = 4.    #
    fuselage.heights.at_quarter_length          = 4. # Not correct
    fuselage.heights.at_three_quarters_length   = 4. # Not correct
    fuselage.heights.at_wing_root_quarter_chord = 4. # Not correct

    fuselage.areas.side_projected  = 4.* 59.8 #  Not correct
    fuselage.areas.wetted          = 688.64
    fuselage.areas.front_projected = 12.57
    
    fuselage.effective_diameter    = 4.0
    
    fuselage.differential_pressure = 10**5 * Units.pascal    # Maximum differential pressure
    
    # add to vehicle
    vehicle.append_component(fuselage)
    
        
    # ------------------------------------------------------------------
    #   Turbofan Network
    # ------------------------------------------------------------------    
    
    #instantiate the gas turbine network
    turbofan = SUAVE.Components.Energy.Networks.Turbofan_Network()
    turbofan.tag = 'turbo_fan'
    
    # setup
    turbofan.number_of_engines = 2.0
    turbofan.design_thrust     = 24000.0
    turbofan.engine_length     = 2.5
    turbofan.nacelle_diameter  = 1.580
    
    # working fluid
    turbofan.working_fluid = SUAVE.Attributes.Gases.Air()
    
    
    # ------------------------------------------------------------------
    #   Component 1 - Ram
    
    # to convert freestream static to stagnation quantities
    
    # instantiate
    ram = SUAVE.Components.Energy.Converters.Ram()
    ram.tag = 'ram'
    
    # add to the network
    turbofan.append(ram)


    # ------------------------------------------------------------------
    #  Component 2 - Inlet Nozzle
    
    # instantiate
    inlet_nozzle = SUAVE.Components.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag = 'inlet_nozzle'
    
    # setup
    inlet_nozzle.polytropic_efficiency = 0.98
    inlet_nozzle.pressure_ratio        = 0.98
    
    # add to network
    turbofan.append(inlet_nozzle)
    
    
    # ------------------------------------------------------------------
    #  Component 3 - Low Pressure Compressor
    
    # instantiate 
    compressor = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag = 'low_pressure_compressor'

    # setup
    compressor.polytropic_efficiency = 0.91
    compressor.pressure_ratio        = 1.14    
    
    # add to network
    turbofan.append(compressor)

    
    # ------------------------------------------------------------------
    #  Component 4 - High Pressure Compressor
    
    # instantiate
    compressor = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag = 'high_pressure_compressor'
    
    # setup
    compressor.polytropic_efficiency = 0.91
    compressor.pressure_ratio        = 13.415    
    
    # add to network
    turbofan.append(compressor)


    # ------------------------------------------------------------------
    #  Component 5 - Low Pressure Turbine
    
    # instantiate
    turbine = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag='low_pressure_turbine'
    
    # setup
    turbine.mechanical_efficiency = 0.99
    turbine.polytropic_efficiency = 0.93     
    
    # add to network
    turbofan.append(turbine)
    
      
    # ------------------------------------------------------------------
    #  Component 6 - High Pressure Turbine
    
    # instantiate
    turbine = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag='high_pressure_turbine'

    # setup
    turbine.mechanical_efficiency = 0.99
    turbine.polytropic_efficiency = 0.93     
    
    # add to network
    turbofan.append(turbine)
      
    
    # ------------------------------------------------------------------
    #  Component 7 - Combustor
    
    # instantiate    
    combustor = SUAVE.Components.Energy.Converters.Combustor()   
    combustor.tag = 'combustor'
    
    # setup
    combustor.efficiency                = 0.99 
    combustor.alphac                    = 1.0     
    combustor.turbine_inlet_temperature = 1450
    combustor.pressure_ratio            = 0.95
    combustor.fuel_data                 = SUAVE.Attributes.Propellants.Jet_A()    
    
    # add to network
    turbofan.append(combustor)

    
    # ------------------------------------------------------------------
    #  Component 8 - Core Nozzle
    
    # instantiate
    nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    nozzle.tag = 'core_nozzle'
    
    # setup
    nozzle.polytropic_efficiency = 0.95
    nozzle.pressure_ratio        = 0.99    
    
    # add to network
    turbofan.append(nozzle)


    # ------------------------------------------------------------------
    #  Component 9 - Fan Nozzle
    
    # instantiate
    nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    nozzle.tag = 'fan_nozzle'

    # setup
    nozzle.polytropic_efficiency = 0.95
    nozzle.pressure_ratio        = 0.99    
    
    # add to network
    turbofan.append(nozzle)
    
    
    # ------------------------------------------------------------------
    #  Component 10 - Fan
    
    # instantiate
    fan = SUAVE.Components.Energy.Converters.Fan()   
    fan.tag = 'fan'

    # setup
    fan.polytropic_efficiency = 0.93
    fan.pressure_ratio        = 1.7    
    
    # add to network
    turbofan.append(fan)
    
    
    # ------------------------------------------------------------------
    #  Component 10 - Thrust
    
    # to compute thrust
    
    # instantiate
    thrust = SUAVE.Components.Energy.Processes.Thrust()       
    thrust.tag ='thrust'
    
    # setup
    thrust.bypass_ratio                       = 5.4
    thrust.compressor_nondimensional_massflow = 49.7272495725
    thrust.reference_temperature              = 288.15
    thrust.reference_pressure                 = 1.01325*10**5
    thrust.number_of_engines                  = turbofan.number_of_engines   
    
    # add to network
    turbofan.thrust = thrust
    
    
    # add turbofan to vehicle
    vehicle.propulsors.append(turbofan)
    
    # done!!
    return vehicle


# ----------------------------------------------------------------------
#   Define the Configurations
# ----------------------------------------------------------------------

def configs_setup(vehicle):
    
    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------
    
    configs = SUAVE.Components.Configs.Config.Container()
    
    base_config = SUAVE.Components.Configs.Config(vehicle)
    base_config.tag = 'base'
    configs.append(base_config)
    
    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------
    
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'cruise'
    
    configs.append(config)
    
    
    # ------------------------------------------------------------------
    #   Takeoff Configuration
    # ------------------------------------------------------------------
    
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'takeoff'
    
    config.wings['Main Wing'].flaps.angle = 20. * Units.deg
    config.wings['Main Wing'].slats.angle = 25. * Units.deg
    
    config.V2_VS_ratio = 1.21
    config.maximum_lift_coefficient = 2.
    
    configs.append(config)
    
    
    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'landing'
    
    config.wings['Main Wing'].flaps_angle = 30. * Units.deg
    config.wings['Main Wing'].slats_angle = 25. * Units.deg

    config.Vref_VS_ratio = 1.23
    config.maximum_lift_coefficient = 2.
    
    ## config.mass_properties.landing = 0.85 * vehicle.mass_properties.takeoff
    
    configs.append(config)
    
    
    # done!
    return configs


# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):
    
    analyses = SUAVE.Analyses.Analysis.Container()
    
    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis
        
    # adjust analyses for configs
    
    # takeoff_analysis
    analyses.takeoff.aerodynamics.drag_coefficient_increment = 0.1000
    
    # landing analysis
    aerodynamics = analyses.landing.aerodynamics
    aerodynamics = SUAVE.Analyses.Analysis(aerodynamics) #Aerodynamics.High_Lift_Zero(aero)
    aerodynamics.tag = 'aerodynamics'
    analyses.landing.aerodynamics = aerodynamics
    
    return analyses
    
    
def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = SUAVE.Analyses.Vehicle()
    
    # ------------------------------------------------------------------
    #  Basic Geometry Relations
    sizing = SUAVE.Analyses.Sizing.Sizing()
    sizing.features = vehicle
    analyses.append(sizing)
    
    # ------------------------------------------------------------------
    #  Weights - Andrew
    weights = SUAVE.Analyses.Weights.Weights()
    weights.features = vehicle
    analyses.append(weights)    
    
    # ------------------------------------------------------------------
    #  Aerodynamics Analysis - Anil, MacDonald
    aerodynamics = SUAVE.Analyses.Aerodynamics.Aerodynamics()
    aerodynamics.features = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)
    
    # ------------------------------------------------------------------
    #  Stability Analysis - Momose
    stability = SUAVE.Analyses.Stability.Stability()
    stability.features = vehicle
    analyses.append(stability)
    
    # ------------------------------------------------------------------
    #  Propulsion Analysis - Emilio
    propulsion = SUAVE.Analyses.Propulsion.Propulsion()
    propulsion.features = vehicle    
    analyses.append(propulsion)
    
    # done!
    return analyses    

#: def analyses_setup()


# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
    
def mission_setup(analyses):
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    
    mission = SUAVE.Analyses.Missions.Mission()
    mission.tag = 'the_mission'
    
    # atmospheric model
    planet     = SUAVE.Attributes.Planets.Earth()
    atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Missions.Segments
    
    # base segment
    base_segment = Segments.Segment()
    base_segment.analyses.planet     = planet
    base_segment.analyses.atmosphere = atmosphere
    
    
    # ------------------------------------------------------------------
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------
    
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1"
    
    segment.analyses.extend( analyses.takeoff )
    
    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 3.0   * Units.km
    segment.air_speed      = 125.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']
    
    # add to misison
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Speed, constant segment angle 
    # ------------------------------------------------------------------    
    
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end   = 8.0   * Units.km
    segment.air_speed      = 190.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']
    
    # add to mission
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------
    #   Third Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    
    
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end = 10.668 * Units.km
    segment.air_speed    = 226.0  * Units['m/s']
    segment.climb_rate   = 3.0    * Units['m/s']
    
    # add to mission
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------    
    
    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.air_speed  = 230.412 * Units['m/s']
    segment.distance   = 3933.65 * Units.km
        
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------    
    #   First Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------    
    
    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_1"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end = 5.0   * Units.km
    segment.air_speed    = 170.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']
    
    # add to mission
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------    
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------    

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_2"

    segment.analyses.extend( analyses.landing )
    
    segment.altitude_end = 0.0   * Units.km
    segment.air_speed    = 145.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']

    # append to mission
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------    
    #   Mission definition complete    
    # ------------------------------------------------------------------
    
    return mission


if __name__ == '__main__':
    full_setup()
    
    
    
    
    ## ------------------------------------------------------------------
    ##   TESTS
    ## ------------------------------------------------------------------
    
    #print configs.takeoff
    
    #local_wings = configs.takeoff.wings
    
    #print local_wings['Main Wing'].sweep
    
    #configs.base.wings['Main Wing'].sweep = 9000
    
    #configs.takeoff.pull_base()
    
    #print local_wings['Main Wing'].sweep    