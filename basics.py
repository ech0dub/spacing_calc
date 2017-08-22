import math

# Inputs
outer_diameter_mm = 100  # mm
outer_diameter_m = outer_diameter_mm / 1000
depth_to_top_m = 1.5
arrangement_options = ['touching trefoil', 'spaced trefoil']
arrangement_selection = arrangement_options[0]
if arrangement_selection == 'spaced trefoil':
    cable_spacing_mm = 300
    cable_spacing_m = cable_spacing_mm / 1000
else:
    cable_spacing_m = outer_diameter_m

# Outputs
cable_1_x = 0
cable_1_y = depth_to_top_m + (outer_diameter_m / 2)
cable_2_x = cable_1_x - (cable_spacing_m / 2)
cable_2_y = cable_1_y + (math.sqrt(3) / 2) * cable_spacing_m
cable_3_x = cable_1_x + (cable_spacing_m / 2)
cable_3_y = cable_1_y + (math.sqrt(3) / 2) * cable_spacing_m

for output in [[cable_1_x, cable_1_y],
               [cable_2_x, cable_2_y],
               [cable_3_x, cable_3_y]]:
    print('x: {:6.3f}m  y: {:6.3f}m'.format(output[0], output[1]))

