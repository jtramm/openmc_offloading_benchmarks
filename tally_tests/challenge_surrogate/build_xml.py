import openmc

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 20
inactive = 10
particles = 10000


###############################################################################
#                 Exporting to OpenMC materials.xml file
###############################################################################

# Instantiate some Materials and register the appropriate Nuclides
fuel = openmc.Material(name='fuel')
fuel.set_density('g/cc', 10.29769)
fuel.add_nuclide('U235', 0.01)
fuel.add_nuclide('U238', 0.99)
fuel.add_nuclide('O16', 2.0)

moderator = openmc.Material(name='moderator')
moderator.set_density('g/cc', 1.0)
moderator.add_element('H', 2.)
moderator.add_element('O', 1.)
moderator.add_s_alpha_beta('c_H_in_H2O')

# Instantiate a Materials collection and export to XML
materials_file = openmc.Materials([moderator, fuel])
materials_file.export_to_xml()


###############################################################################
#                 Exporting to OpenMC geometry.xml file
###############################################################################

pitch=1.26
pinrad = 0.56

# Instantiate Surfaces
left  = openmc.XPlane(x0=-pitch, boundary_type='reflective')
right = openmc.XPlane(x0=pitch,  boundary_type='reflective')
down  = openmc.YPlane(y0=-pitch, boundary_type='reflective')
up    = openmc.YPlane(y0=pitch,  boundary_type='reflective')

ring = openmc.ZCylinder(r=pinrad)

fuel_cell = openmc.Cell(region=-ring, fill=fuel)
mod_cell  = openmc.Cell(region=+ring, fill=moderator)
all_mod   = openmc.Cell(fill=moderator)

pincell = openmc.Universe(cells=[fuel_cell,mod_cell])
modcell = openmc.Universe(cells=[all_mod])

pattern = [[pincell, pincell],[pincell, modcell]]
lattice = openmc.RectLattice()
lattice.lower_left=[-pitch, -pitch]
lattice.universes=pattern
lattice.pitch=[pitch,pitch]

reactor_cell = openmc.Cell(fill=lattice, region=+left & -right & +down & -up)

geometry = openmc.Geometry([reactor_cell])
geometry.export_to_xml()

###############################################################################
#                   Exporting to OpenMC settings.xml file
###############################################################################

# Instantiate a Settings object, set all runtime parameters, and export to XML
settings_file = openmc.Settings()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-pitch, -pitch, -pitch, pitch, pitch, pitch]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

settings_file.export_to_xml()

###############################################################################
#                   Exporting to OpenMC tallies.xml file
###############################################################################

# Instantiate an axial mesh
mesh = openmc.RegularMesh()
mesh.ndimension = 3
mesh.dimension = [1,1,2]
mesh.lower_left = [-pitch, -pitch,-1000.0]
mesh.width = [2*pitch, 2*pitch, 1000.0]

# Instantiate tally Filter
mesh_filter = openmc.MeshFilter(mesh)

cell_instance_filter = openmc.DistribcellFilter(fuel_cell)

# Instantiate the Tally
tally = openmc.Tally()
tally.filters = [mesh_filter,cell_instance_filter]
tally.scores = ['total', 'fission','absorption','scatter','(n,gamma)', '(n,2n)']

# Instantiate a Tallies collection and export to XML
tallies_file = openmc.Tallies([tally])
tallies_file.export_to_xml()

###############################################################################
#                   Exporting to OpenMC plots.xml file
###############################################################################

plot = openmc.Plot()
plot.origin = [0, 0,0]
plot.width = [2*pitch, 2*pitch]
plot.pixels = [500, 500]
plot.color_by = 'material'

# Instantiate a Plots collection and export to XML
plot_file = openmc.Plots([plot])
plot_file.export_to_xml()
