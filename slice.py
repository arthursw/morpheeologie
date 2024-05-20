import trimesh
import numpy as np

box_size = [50, 50, 50]
step = 5
step_z = 1

radius = 20
n_drops = 20
pos_z_up = 0
pos_z_down = -10
inject_amount = 5
plane_pause = 500 #in ms

mesh = trimesh.load('female_hand.glb', force='mesh')

def put_mesh_in_bounds(mesh, box_size):
    # origin = mesh.centroid.copy()
    # size = mesh.extents
    # for v in mesh.vertices:
    #     for i in range(3):
    #         v[i] = ((v[i] - origin[i]) / (size[i] / 2.0)) * box_size[i] / 2.0
    mesh.apply_scale(1/mesh.extents)
    mesh.apply_translation(-mesh.centroid)
    mesh.apply_scale(box_size)
    return mesh

# def create_trajetory(slice, step):
#     vertices = slice.vertices
#     current_distance = 0
#     v0 = vertices[0]
#     trajectory = [v0]
#     for v1 in vertices[1:]:
#         pos = v0.copy()
#         v = v1 - v0
#         length = np.linalg.norm(v)
#         vn = v / length
        
#         while length - current_distance > step:
#             current_step = min(length - current_distance, step)
#             pos += vn * current_step
#             current_distance += current_step
#             trajectory.append(pos)
#         current_distance += length - current_distance
        
#         v0 = v1
#     trajectory.append(v1)
#     trajectory.append(vertices[0])
#     return trajectory

def create_trajetory(slice, step):
    return slice.vertices

def slice_mesh(mesh, step_z, step, box_size):
    current_distance = 0
    trajectories = []
    while current_distance < box_size[1]:
        slice = mesh.section(plane_origin=[0, -box_size[1]/2 + current_distance, 0], plane_normal=[0,1,0])
        current_distance += step_z
        if slice:
            trajectories.append(create_trajetory(slice, step))
    return trajectories

def quad_to_tri(quad):
    return [ [quad[0], quad[1], quad[3]], [quad[1], quad[2], quad[3]] ]

def create_cube_on_vertex(v, size=0.5):
    vertices = [ [v[0]-size/2, v[1]-size/2, v[2]-size/2], 
                 [v[0]+size/2, v[1]-size/2, v[2]-size/2], 
                 [v[0]-size/2, v[1]+size/2, v[2]-size/2],
                 [v[0]+size/2, v[1]+size/2, v[2]-size/2],
                 [v[0]-size/2, v[1]-size/2, v[2]+size/2], 
                 [v[0]+size/2, v[1]-size/2, v[2]+size/2],
                 [v[0]-size/2, v[1]+size/2, v[2]+size/2],
                 [v[0]+size/2, v[1]+size/2, v[2]+size/2],  ]
    faces = quad_to_tri([0, 1, 3, 2]) + quad_to_tri([4, 5, 7, 6]) + quad_to_tri([2, 3, 7, 6]) + quad_to_tri([0, 2, 6, 4]) + quad_to_tri([1, 3, 7, 5]) + quad_to_tri([0, 1, 5, 4])
    
    return vertices, faces

def create_trajectories_cubes(trajectories):
    vertices = []
    faces = []
    for trajectory in trajectories:
        for v in trajectory:
            vs, fs = create_cube_on_vertex(v)
            for triangle in fs:
                for i, index in enumerate(triangle):
                    triangle[i] += len(vertices)
            faces += fs
            vertices += vs
    
    return trimesh.Trimesh(vertices=vertices, faces=faces)

def trajectories_to_gcode(trajectories):
    commands = ['G91', 'G0 F5000'] # Put in relative mode and set speed to 5000

    for trajectory in trajectories:
        
        for p in trajectory:
            # go to position
            commands.append(f'G0 X{p[0]:.2f} Y{p[1]:.2f}')
            # down
            commands.append(f'G0 Z{pos_z_down}')
            # inject
            commands.append(f'G0 E{inject_amount}')
            # up
            commands.append(f'G0 Z{pos_z_up}')
        # pause
        commands.append(f'G4 P{plane_pause}')
    return commands

print(mesh.extents)
print(mesh.centroid)
mesh = put_mesh_in_bounds(mesh, box_size)
# mesh.show()
trajectories = slice_mesh(mesh, step_z, step, box_size)
viz = create_trajectories_cubes(trajectories)
viz.show()

# commands = trajectories_to_gcode(trajectories)

# with open('mesh.gcode', 'w') as f:
#     for command in commands:
#         f.write(command+'\n')