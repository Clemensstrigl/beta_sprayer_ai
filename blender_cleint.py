import bpy
import socket
import json
import time
from bpy.app.handlers import persistent
from mathutils import Matrix, Vector


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Simulation timestep
timestep = 0.1

@persistent
def connect_to_server():
    """Connects to the server and returns a socket object."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to server.")
            return s
        except ConnectionRefusedError:
            print("Connection refused. Trying again in 1 second...")
            time.sleep(1)
            return connect_to_server()  # Retry connection

@persistent
def send_and_receive_data(conn, data):
    """Sends data to the server and receives a response."""
    conn.sendall(json.dumps(data).encode('utf-8'))
    response = conn.recv(1024).decode('utf-8')
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("Error decoding JSON data:", response)
        return None
    
def connect_and_send(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to server.")
            s.sendall(json.dumps(data).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            try:
                rtr =  json.loads(response)
                s.close()
                return rtr
            except json.JSONDecodeError:
                print("Error decoding JSON data:", response)
                return None
        except ConnectionRefusedError:
            print("Connection refused. Trying again in 1 second...")
            time.sleep(1)
            return connect_to_server()  # Retry connection


@persistent
def run_simulation(scene, depsgraph):
    """Main simulation loop."""

    if scene.frame_current % 5 != 0:
        return

    # conn = None

    # if not conn:
    #     conn = connect_to_server()
    #     print(conn)

    # Get the cube object
    #cube = bpy.data.objects["MyCube"]["MyCube"]
    #cube = bpy.data.objects["MyCube"]["MyCube"].evaluated_get(depsgraph)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["MyCube"].select_set(True)

    editorLoc = bpy.data.objects["MyCube"].location
    x,y,z = bpy.data.objects["MyCube"].location


    # Get the current cube's location
    cube_data = {
        "x": x,
        "y": y,
        "z": z,
        # Add other relevant data as needed
    }

    # Send the current data to the server
    #new_data = send_and_receive_data(conn, cube_data)
    
    new_data = connect_and_send(cube_data)
    print("New data: ",new_data)
    if new_data:
        print("X: ", bpy.data.objects["MyCube"].location.x)
        print("Y: ", bpy.data.objects["MyCube"].location.y)
        print("Z: ", bpy.data.objects["MyCube"].location.z)
        x_new = new_data.get("x", bpy.data.objects["MyCube"].location.x)
        y_new = new_data.get("y", bpy.data.objects["MyCube"].location.y)
        z_new = new_data.get("z", bpy.data.objects["MyCube"].location.z)
        print("X: ", bpy.data.objects["MyCube"].location.x)
        print("Y: ", bpy.data.objects["MyCube"].location.y)
        print("Z: ", bpy.data.objects["MyCube"].location.z)
        #bpy.data.objects["MyCube"].location = Vector((0,0,0)) #this works, sets object to 0,0,0


        bpy.data.objects["MyCube"].location = Vector((x_new,y_new,z_new))
        
        bpy.ops.object.transform_apply(location=True)
        #bpy.context.view_layer.update()


   

    # If the server responds with new data, update the cube
 
    #Advance the simulation by one timestep (adjust based on your physics)
    #scene.frame_set(scene.frame_current + 1) 

    #Wait for the next timestep (optional for smoother simulation)
    #time.sleep(timestep)

def main():
   
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 100
    bpy.context.scene.rigidbody_world.enabled = True
    bpy.context.scene.rigidbody_world.substeps_per_frame = 500
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_post.append(run_simulation)
    

    # Create a cube if it doesn't exist (replace with your own scene setup)
    if "MyCube" not in bpy.data.objects:
        bpy.ops.mesh.primitive_cube_add(size=1,location=(0, 0, 5), scale=(1, 1, 1))
        bpy.context.object.name = "MyCube"
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.type = 'ACTIVE'
        bpy.context.object.rigid_body.mass = 2
        bpy.context.object.rigid_body.collision_shape = 'CYLINDER'
        bpy.context.object.rigid_body.friction = 0.504695
        bpy.context.object.rigid_body.restitution = 0.6
        bpy.context.object.rigid_body.use_margin = True
        bpy.context.object.rigid_body.collision_margin = 0
        bpy.context.object.rigid_body.linear_damping = 0.35
        bpy.context.object.rigid_body.angular_damping = 0.6
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "Floor"
        bpy.ops.transform.resize(value=(20.00, 20.00, 20.00), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.type = 'PASSIVE'
        bpy.context.object.rigid_body.collision_shape = 'MESH'
        bpy.context.object.rigid_body.friction = 0.5
        bpy.context.object.rigid_body.collision_margin = 0





    # Enable physics for the cube
    cube = bpy.data.objects["MyCube"]
    #cube.rigid_body.type = 'ACTIVE'




    bpy.ops.ptcache.bake_all(bake=True) 
    #bpy.ops.render.render()

if __name__ == "__main__":
    main()












