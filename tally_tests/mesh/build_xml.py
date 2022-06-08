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
fuel.set_density('g/cc', 4.5)
fuel.add_nuclide('U235', 1.)

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
pinrad = 0.055

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
bounds = [-1, -1, -1, 1, 1, 1]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

settings_file.export_to_xml()

###############################################################################
#                   Exporting to OpenMC tallies.xml file
###############################################################################

# Instantiate a tally mesh
mesh = openmc.RegularMesh(mesh_id=1)
mesh.dimension = [4, 4]
mesh.lower_left = [-2, -2]
mesh.width = [1, 1]

# Instantiate tally Filter
mesh_filter = openmc.MeshFilter(mesh)

# Instantiate tally Trigger
trigger = openmc.Trigger(trigger_type='rel_err', threshold=1E-2)
trigger.scores = ['all']

# Instantiate the Tally
tally = openmc.Tally(tally_id=1)
tally.filters = [mesh_filter]
tally.scores = ['total']
tally.triggers = [trigger]

# Instantiate a Tallies collection and export to XML
tallies_file = openmc.Tallies([tally])
tallies_file.export_to_xml()
