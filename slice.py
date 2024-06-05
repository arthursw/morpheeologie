import trimesh
import numpy as np

box_size = np.array([100, 100, 100])
home_pos = np.array([150, 80, 112])

step = 5
step_z = 1

pos_z_up = 112 # 104
pos_z_down = 112 # 104
inject_amount = 1.005 # 1
vacuum_amount = -1.00 # -0.98
speed = 3000
inject_speed = 3000
plane_pause = 500 #in ms

mesh = trimesh.load('models/female_hand.glb', force='mesh')

def put_mesh_in_bounds(mesh, box_size):
    # origin = mesh.centroid.copy()
    # size = mesh.extents
    # for v in mesh.vertices:
    #     for i in range(3):
    #         v[i] = ((v[i] - origin[i]) / (size[i] / 2.0)) * box_size[i] / 2.0
    # mesh.apply_scale(1/mesh.extents)
    mesh.apply_scale(1/np.full(3, np.max(mesh.extents)))
    mesh.apply_translation(-mesh.centroid)
    mesh.apply_scale(box_size)
    # mesh.apply_translation(home_pos-box_size/2) # not working...
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

# def create_trajetory(slice, step):
#     return slice.vertices

def create_trajetory(slice, step):
    vertices = list(slice.vertices)
    v = vertices.pop()
    trajectory = [v]
    while len(trajectory) < len(slice.vertices):
        distances = [np.linalg.norm(v-vi) for vi in vertices]
        v = vertices.pop(np.argmin(distances))
        trajectory.append(v)
    return trajectory

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
    commands = [] # Put in relative mode and set speed to 5000

    xs = []
    ys = []
    zs = []
    height = 0
    
    for trajectory in trajectories:
        
        for p in trajectory:
            # go to position
            x = p[0] + home_pos[0]
            # Warning X in the 3D space becomes X in 2D, but Z in the 3D space becomes Y
            y = p[2] + home_pos[1]
            xs.append(x)
            ys.append(y)
            zs.append(pos_z_down+height)
            zs.append(pos_z_up+height)

            commands.append(f'G0 X{x:.2f} Y{y:.2f} F{speed:.2f}')
            # down
            commands.append(f'G0 Z{pos_z_down+height}')
            # inject
            commands.append(f'G0 E{inject_amount} F{inject_speed:.2f}')
            commands.append(f'G0 E{vacuum_amount} F{inject_speed:.2f}')
            # up
            commands.append(f'G0 Z{pos_z_up+height} F{speed:.2f}')

        # pause
        commands.append(f'G4 P{plane_pause}')
        height += 1
    
    print(f'xmin: {np.min(xs):.2f}, xmax: {np.max(xs):.2f}, ymin: {np.min(ys):.2f}, ymax: {np.max(ys):.2f}, zmin: {np.min(zs):.2f}, zmax: {np.max(zs):.2f}')
    return commands

mesh = put_mesh_in_bounds(mesh, box_size)
# mesh.show()
trajectories = slice_mesh(mesh, step_z, step, box_size)
# viz = create_trajectories_cubes(trajectories)
# viz.show()

commands = trajectories_to_gcode(trajectories)

with open('mesh.gcode', 'w') as f:
    for command in commands:
        f.write(command+'\n')