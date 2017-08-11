import math


class Cable:
    def __init__(self, label):
        self.label = label
        self.x_m = 0
        self.y_m = 0


class Circuit:

    def __init__(self, depth_to_top_m, arrangement, cable_spacing_m, outer_diameter_m):
        self.depth_to_top_m = depth_to_top_m
        self.arrangement = arrangement
        self.cable_spacing_m = cable_spacing_m
        self.outer_diameter_m = outer_diameter_m
        self.cable1 = Cable('Yellow phase')
        self.cable2 = Cable('Red phase')
        self.cable3 = Cable('Blue phase')

    def calc_spacing(self):
        if self.arrangement == 'spaced trefoil':
            pass
        elif self.arrangement == 'touching trefoil':
            self.cable_spacing_m = self.outer_diameter_m
        else:
            raise ValueError('Error: Arrangement specified as {}./n'
                             'This arrangement is not supported.'.format(str(self.arrangement)))

    def calc_coords(self):
        self.calc_spacing()
        self.cable1.x_m = 0
        self.cable1.y_m = self.depth_to_top_m + (self.outer_diameter_m / 2)
        self.cable2.x_m = self.cable1.x_m - (self.cable_spacing_m / 2)
        self.cable2.y_m = self.cable1.y_m + (math.sqrt(3) / 2) * self.cable_spacing_m
        self.cable3.x_m = self.cable1.x_m + (self.cable_spacing_m / 2)
        self.cable3.y_m = self.cable1.y_m + (math.sqrt(3) / 2) * self.cable_spacing_m


def main():
    def print_output(cable_circuit):
        for cable in (cable_circuit.cable1, cable_circuit.cable2, cable_circuit.cable3):
            print('{:12s}: x: {:6.3f}m  y: {:6.3f}m'.format(cable.label, cable.x_m, cable.y_m))

    def display_graphic_output():
        pass

    # Input parameter options
    arrangement_options = ['touching trefoil', 'spaced trefoil']

    # Init circuit
    circuit1 = Circuit(depth_to_top_m=1.5,
                       arrangement=arrangement_options[0],
                       cable_spacing_m=0,
                       outer_diameter_m=0.1)

    # Get new inputs from user and update circuit
    circuit1.depth_to_top_m = float(input("Enter depth to top of upper cable [m]: "))
    arrangement_choice = int(input("Enter 0 for touching trefoil, 1 for spaced trefoil: "))
    circuit1.arrangement = arrangement_options[arrangement_choice]
    if circuit1.arrangement == "spaced trefoil":
        circuit1.cable_spacing_m = int(input("Enter cable spacing [mm]: ")) / 1000
    circuit1.outer_diameter_m = int(input("Enter cable outer diameter [mm]: ")) / 1000

    circuit1.calc_coords()

    print_output(circuit1)
    display_graphic_output()

main()
