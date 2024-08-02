import bpy



class Body():

    def __init__(self, gender, height, apeindex, weight, canDoPullup=False, canDoPistleSquat=False):
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        self.gender = gender
        self.height = height
        self.apeindex = apeindex
        self.weight = weight
        self.canDoPullup = canDoPullup
        self.canDoPistleSquat = canDoPistleSquat
        self.body_segments = self.def_segments()
        self.body_parts = self.create_body()
        self.skeleton = self.add_armature(self.body_parts)


    def create_pipe(self,name, radius, height, location, rotation=(0, 0, 0)):
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=location, rotation=rotation)
        pipe = bpy.context.object
        pipe.name = name
        return pipe
    
    def create_sphere(self,name, radius, location, rotation=(0, 0, 0)):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, location=location, rotation=rotation)
        sphere = bpy.context.object
        sphere.name = name
        return sphere
    
    def def_segments(self,):
        ape_index_addon = self.apeindex/4
        ape_index_center_offset = ape_index_addon/2


        return [
            {"name": "head", "weight":0.0826 *self.weight,    "radius": 0.0625*self.height, "location": [0, 0, 0.9375*self.height], "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "chest", "weight":0.21 *self.weight,"radius": 0.1*self.height, "location": [0, 0, 0.7708*self.height], "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "stomach", "weight":0.131 *self.weight,  "radius": 0.075*self.height, "location": [0, 0, 0.595*self.height], "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "hips", "weight":0.137 *self.weight, "radius": 0.05*self.height, "height": 0.15*self.height, "location": [0, 0, 0.4708*self.height],"rotation": (0, 1.5708, 0), "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "upper_arm_L", "weight":0.0325 *self.weight, "radius": 0.03*self.height, "height": 0.1875*self.height + ape_index_addon, "location": [-0.1938*self.height - ape_index_center_offset, 0, 0.8125*self.height],  "rotation": (0, 1.5708, 0), "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "upper_arm_R", "weight":0.0325 *self.weight,"radius": 0.03*self.height, "height": 0.1875*self.height + ape_index_addon, "location": [0.1938*self.height+ ape_index_center_offset, 0, 0.8125*self.height],   "rotation": (0, 1.5708, 0), "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "lower_arm_L", "weight":0.0187 *self.weight, "radius": 0.029*self.height, "height": 0.1667*self.height + ape_index_addon, "location": [-0.3708*self.height- ape_index_addon -ape_index_center_offset, 0, 0.8125*self.height],    "rotation": (0, 1.5708, 0), "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "lower_arm_R", "weight":0.0187 *self.weight,"radius": 0.029*self.height, "height": 0.1667*self.height + ape_index_addon, "location": [0.3708*self.height+ ape_index_addon + ape_index_center_offset, 0, 0.8125*self.height],     "rotation": (0, 1.5708, 0), "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "hand_L", "weight":0.0065 *self.weight,"radius": 0.03*self.height,  "location": [-0.4708*self.height- ape_index_addon*2, 0, 0.8125*self.height],"rotation": (0, 1.5708, 0), "is_joint": False, "parent": ["lower_arm_L"], "has_rigid_body": False, "has_rigid_body": False, "active": "ACTIVE"},
            {"name": "hand_R", "weight":0.0065 *self.weight,"radius": 0.03*self.height,  "location": [0.4708*self.height+ ape_index_addon*2, 0, 0.8125*self.height], "rotation": (0, 1.5708, 0), "is_joint": False, "parent": ["lower_arm_R"], "has_rigid_body": False, "has_rigid_body": False, "active": "ACTIVE"},
            {"name": "upper_leg_L", "weight":0.105 *self.weight,"radius": 0.03*self.height, "height": 0.2083*self.height, "location": [-0.0417*self.height, 0, 0.325*self.height], "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "upper_leg_R", "weight":0.105 *self.weight, "radius": 0.03*self.height, "height": 0.2083*self.height, "location": [0.0417*self.height, 0, 0.325*self.height], "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "lower_leg_L", "weight":0.0475 *self.weight,"radius": 0.029*self.height, "height": 0.1667*self.height, "location": [-0.0417*self.height, 0, 0.1375*self.height], "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "lower_leg_R", "weight":0.0475 *self.weight,"radius": 0.029*self.height, "height": 0.1667*self.height, "location": [0.0417*self.height, 0, 0.1375*self.height], "is_joint": False, "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "foot_L", "weight":0.0143 *self.weight,"radius": 0.03*self.height,  "location": [-0.0417*self.height, 0, 0.03*self.height], "is_joint": False, "parent": ["lower_leg_L"], "has_rigid_body": False, "active": "ACTIVE"},
            {"name": "foot_R", "weight":0.0143*self.weight,"radius": 0.03*self.height,  "location": [0.0417*self.height, 0, 0.03*self.height], "is_joint": False, "parent": ["lower_leg_R"], "has_rigid_body": False, "active": "ACTIVE"},

           


            {"name": "neck","weight":0.02 *self.weight, "radius": 0.0375*self.height, "location": [0, 0, 0.875*self.height], "is_joint": True,"virtical": True, "parent": ["chest", "head"], "connecting_joint": "head", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "lumb_1","weight":0.02 *self.weight, "radius": 0.0375*self.height, "location": [0, 0, 0.67*self.height], "is_joint": True,"virtical": True, "parent": ["stomach", "chest"], "connecting_joint": "neck", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "lumb_2","weight":0.02 *self.weight, "radius": 0.0375*self.height, "location": [0, 0, 0.5208*self.height], "is_joint": True,"virtical": True, "parent": ["hips", "stomach"], "connecting_joint": "lumb_1", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "lumb_3","weight":0.02 *self.weight, "radius": 0.0375*self.height, "location": [0, 0, 0.4208*self.height], "is_joint": True,"virtical": True, "connecting_joint": "lumb_2", "has_rigid_body": True, "active": "ACTIVE"},

            

            {"name": "collar_L", "weight":0.02 *self.weight, "radius": 0.0375*self.height, "location": [-0.1*self.height, 0, 0.8125*self.height], "is_joint": True, "virtical": False,"parent": ["chest", "upper_arm_L"], "connecting_joint": "elbow_L", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "collar_R", "weight":0.02 *self.weight, "radius": 0.0375*self.height, "location":[0.1*self.height, 0, 0.8125*self.height], "is_joint": True, "virtical": False,"parent": ["chest", "upper_arm_R"], "connecting_joint": "elbow_R", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "elbow_L", "weight":0.0325 *self.weight, "radius": 0.0375*self.height,  "location": [-0.2874*self.height - ape_index_addon, 0, 0.8125*self.height], "is_joint": True , "virtical": False,"parent": ["upper_arm_L", "lower_arm_L"], "connecting_joint": "hand_L", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "elbow_R", "weight":0.0325 *self.weight,"radius": 0.0375*self.height, "location": [0.2874*self.height+ ape_index_addon, 0, 0.8125*self.height],  "is_joint": True, "virtical": False,"parent": ["upper_arm_R", "lower_arm_R"], "connecting_joint": "hand_R", "has_rigid_body": True, "active": "ACTIVE"},
            #{"name": "wrist_L", "weight":0.0325 *self.weight,"radius": 0.0375*self.height, "location": [-0.4541*self.height+ ape_index_addon*2, 0, 0.8125*self.height],  "is_joint": True, "virtical": False,"parent": ["lower_arm_L", "hand_L"], "connecting_joint": "hand_R", "has_rigid_body": False, "active": "ACTIVE"},
            #{"name": "wrist_R", "weight":0.0325 *self.weight,"radius": 0.0375*self.height, "location": [0.4541*self.height+ ape_index_addon*2, 0, 0.8125*self.height],  "is_joint": True, "virtical": False,"parent": ["lower_arm_R", "hand_R"], "connecting_joint": "hand_R", "has_rigid_body": False, "active": "ACTIVE"},



            {"name": "hip_L", "weight":0.105 *self.weight,"radius": 0.0375*self.height, "location": [-0.0417*self.height, 0, 0.4291*self.height],"is_joint": True,"virtical": True,"parent": ["hips", "upper_leg_L"], "connecting_joint": "knee_L", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "hip_R", "weight":0.105 *self.weight, "radius": 0.0375*self.height, "location": [0.0417*self.height, 0, 0.4291*self.height],"is_joint": True,"virtical": True, "parent": ["hips", "upper_leg_R"], "connecting_joint": "knee_R", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "knee_L", "weight":0.105 *self.weight,"radius": 0.0375*self.height, "location": [-0.0417*self.height, 0, 0.2209*self.height],"is_joint": True,"virtical": True,"parent": ["upper_leg_L", "lower_leg_L"], "connecting_joint": "foot_L", "has_rigid_body": True, "active": "ACTIVE"},
            {"name": "knee_R", "weight":0.105 *self.weight, "radius": 0.0375*self.height, "location": [0.0417*self.height, 0, 0.2208*self.height],"is_joint": True,"virtical": True, "parent": ["upper_leg_R", "lower_leg_R"], "connecting_joint": "foot_R", "has_rigid_body": True, "active": "ACTIVE"},

        ]
    
    def get_segment_attr(self, segment, attr):
        for s in self.body_segments:
            if segment in s["name"]:
                if attr in s.keys():
                    return s[attr]
                elif attr == "height":
                    return s["radius"]*2
                return None
        return None
    
    def get_joint_parent(self, child):
        for s in self.body_segments:
            if not s["is_joint"]:
                continue
            if s["connecting_joint"] == child:
                return s["name"]
        
        return None

    def create_body(self,):
        body_parts = {}

        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, -1.5), scale=(10, 10, 1))
        bpy.context.object.scale[0] = 10
        bpy.context.object.scale[1] = 10

        bpy.ops.rigidbody.object_add(type="PASSIVE")

        
       
        
        # Create pipes for each body segment
        for segment in self.body_segments:
            rotation = segment.get("rotation", (0, 0, 0))
            if "height" in segment:
                body_parts[segment["name"]] = self.create_pipe(segment["name"], segment["radius"], segment["height"], segment["location"], rotation)
            else:
                body_parts[segment["name"]] = self.create_sphere(segment["name"], segment["radius"], segment["location"], rotation)
            
            if segment["has_rigid_body"]:
                bpy.ops.rigidbody.object_add(type=segment["active"])
            


            
        return body_parts
    

            

        
    def add_armature(self, body_parts):
        bpy.ops.object.armature_add(enter_editmode=False)
        armature = bpy.context.object
        armature.name = 'Armature'
        print(type(armature.data.bones))
        

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        edit_bones = armature.data.edit_bones
    

        
        for segment in self.body_segments:

            if not segment["is_joint"]:
                continue

            seg_name = segment["name"]
            print("Joint Name: " + seg_name)
            seg_loc = self.get_segment_attr(seg_name, "location")




            bone = edit_bones.new(seg_name)
            bone.head = seg_loc
            print("Bone name: " + bone.name)

            connecting_segment_name = self.get_segment_attr(seg_name, "connecting_joint")
            print(seg_name, connecting_segment_name)
            connecting_segment_loc = self.get_segment_attr(connecting_segment_name, "location")

            obser_indx = 0

            if self.get_segment_attr(seg_name, "virtical"):
                obser_indx = 2

            if not self.get_segment_attr(connecting_segment_name, "is_joint"):
                multiplier = 1
                if seg_loc[obser_indx] > connecting_segment_loc[obser_indx]:
                    multiplier = -1
                

                connecting_segment_loc[obser_indx] = connecting_segment_loc[obser_indx] + multiplier * self.get_segment_attr(connecting_segment_name, "radius")

            bone.tail = connecting_segment_loc
            #bone.length = abs(seg_loc[obser_indx] - connecting_segment_loc[obser_indx])
            
            
         
            
        for segment in self.body_segments:
            if not segment["is_joint"]:
                continue
            
            seg_name = segment["name"]


            parent_name = self.get_joint_parent(seg_name)
            if parent_name:
                edit_bones[seg_name].parent = edit_bones[parent_name]    
        

        for b in armature.data.edit_bones:
           print(b)
           if "Bone" in b.name:
               armature.data.edit_bones.remove(b)

        bpy.ops.object.mode_set(mode='OBJECT') # Exit edit mode after parenting




        # Parent each body part to its corresponding bone and hide the body parts
        for bone_name, body_part in body_parts.items():
            if not self.get_segment_attr(body_part.name, "is_joint"):
                continue
            print(bone_name, body_part.name)
            body_part.select_set(True)
            bpy.context.view_layer.objects.active = armature
            
            armature.data.bones.active = armature.data.bones[bone_name]

            bpy.ops.object.mode_set(mode='EDIT')

            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

            #offset = None

            # # Create or get the vertex group
            # if bone_name not in body_part.vertex_groups:
            #     body_part.vertex_groups.new(name=bone_name)
            # vertex_group = body_part.vertex_groups[bone_name]
            # # Assign weight 1.0 to all vertices
            # percentage_per_vertex = 1/len(body_part.data.vertices)
            # print("Percentage weight per vertex: %f" % percentage_per_vertex)
            # for v in body_part.data.vertices:
            #     vertex_group.add([v.index], percentage_per_vertex * self.get_segment_attr(body_part.name, "weight"), 'REPLACE')


            # if offset:
            #     bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
            #     empty = bpy.context.object
            #     empty.name = "OffsetEmpty" 
            #     # Position the empty (Adjust offset as needed)
            #     empty.location = bone_to_parent_to.head + (0, 0, -0.5)  
            #     # Parent the empty to the bone
            #     bpy.context.view_layer.objects.active = empty
            #     bpy.ops.object.parent_set(type='BONE', keep_transform=True)
            #     # Parent the object to the empty
            #     bpy.context.view_layer.objects.active = bpy.data.objects["TubeMesh"]
            #     bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)



            bpy.ops.object.mode_set(mode='OBJECT') # Exit edit mode after parenting
            bpy.ops.object.select_all(action='DESELECT') #deselect all objects
        

        for bone_name, body_part in body_parts.items():
                bpy.context.view_layer.objects.active = body_part
                #bpy.ops.object.hide_viewport = True  # Hide body parts

                is_joint = self.get_segment_attr(body_part.name, "is_joint")
                parent_obj_names = self.get_segment_attr(body_part.name, "parent")
                has_rigid_body = self.get_segment_attr(body_part.name, "has_rigid_body")



                # if is_joint:

                #     bpy.ops.object.constraint_add(type='CHILD_OF')
                #     bpy.context.object.constraints["Child Of"].target = bpy.data.objects["Armature"]
                #     bpy.context.object.constraints["Child Of"].subtarget = bone_name
                #     bpy.ops.constraint.childof_clear_inverse(constraint="Child Of", owner='OBJECT')
                #     bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='OBJECT')


                if parent_obj_names and is_joint:
                    body_part.select_set(True)

                    
                    bpy.ops.rigidbody.constraint_add()
                    bpy.context.object.rigid_body_constraint.type = 'GENERIC'


                    bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects[parent_obj_names[0]]
                    bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects[parent_obj_names[1]]
                    bpy.context.object.rigid_body_constraint.use_limit_ang_x = True
                    bpy.context.object.rigid_body_constraint.use_limit_ang_y = True
                    bpy.context.object.rigid_body_constraint.use_limit_ang_z = True

                    bpy.context.object.rigid_body_constraint.limit_ang_x_lower = 0
                    bpy.context.object.rigid_body_constraint.limit_ang_x_upper = 360
                    bpy.context.object.rigid_body_constraint.limit_ang_y_lower = 0
                    bpy.context.object.rigid_body_constraint.limit_ang_y_upper = 360
                    bpy.context.object.rigid_body_constraint.limit_ang_z_lower = 0
                    bpy.context.object.rigid_body_constraint.limit_ang_z_upper = 360

                    bpy.context.object.rigid_body_constraint.use_limit_lin_x = True
                    bpy.context.object.rigid_body_constraint.use_limit_lin_y = True
                    bpy.context.object.rigid_body_constraint.use_limit_lin_z = True
                    bpy.context.object.rigid_body_constraint.limit_lin_x_lower = 0
                    bpy.context.object.rigid_body_constraint.limit_lin_x_upper = 0
                    bpy.context.object.rigid_body_constraint.limit_lin_y_lower = 0
                    bpy.context.object.rigid_body_constraint.limit_lin_y_upper = 0
                    bpy.context.object.rigid_body_constraint.limit_lin_z_lower = 0
                    bpy.context.object.rigid_body_constraint.limit_lin_z_upper = 0






                elif not has_rigid_body and not is_joint:
                    
                    bpy.ops.rigidbody.constraint_add()
                    bpy.context.object.rigid_body_constraint.type = 'POINT'

                    bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects[parent_obj_names[0]]
                    bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects[body_part.name]
                    # bpy.context.object.rigid_body_constraint.use_limit_ang_x = True
                    # bpy.context.object.rigid_body_constraint.use_limit_ang_y = True
                    # bpy.context.object.rigid_body_constraint.use_limit_ang_z = True

                    # bpy.context.object.rigid_body_constraint.limit_ang_x_lower = 0
                    # bpy.context.object.rigid_body_constraint.limit_ang_x_upper = 0
                    # bpy.context.object.rigid_body_constraint.limit_ang_y_lower = 0
                    # bpy.context.object.rigid_body_constraint.limit_ang_y_upper = 0
                    # bpy.context.object.rigid_body_constraint.limit_ang_z_lower = 0
                    # bpy.context.object.rigid_body_constraint.limit_ang_z_upper = 0

                    # bpy.context.object.rigid_body_constraint.use_limit_lin_x = True
                    # bpy.context.object.rigid_body_constraint.use_limit_lin_y = True
                    # bpy.context.object.rigid_body_constraint.use_limit_lin_z = True
                    # bpy.context.object.rigid_body_constraint.limit_lin_x_lower = 0
                    # bpy.context.object.rigid_body_constraint.limit_lin_x_upper = 0
                    # bpy.context.object.rigid_body_constraint.limit_lin_y_lower = 0
                    # bpy.context.object.rigid_body_constraint.limit_lin_y_upper = 0
                    # bpy.context.object.rigid_body_constraint.limit_lin_z_lower = 0
                    # bpy.context.object.rigid_body_constraint.limit_lin_z_upper = 0




        




                



                bpy.ops.object.select_all(action='DESELECT') #deselect all objects


        

        return armature

    def lock_part(self, part_name):
        part = bpy.data.objects[part_name]
        part.rigid_body.kinematic = True

    def unlock_part(self, part_name):
        part = bpy.data.objects[part_name]
        part.rigid_body.kinematic = False

    def lock_hands_and_feet(self, body_parts):
        self.lock_part(body_parts["hand_L"].name)
        self.lock_part(body_parts["hand_R"].name)
        self.lock_part(body_parts["foot_L"].name)
        self.lock_part(body_parts["foot_R"].name)

    def unlock_hands_and_feet(self, body_parts):
        self.unlock_part(body_parts["hand_L"].name)
        self.unlock_part(body_parts["hand_R"].name)
        self.unlock_part(body_parts["foot_L"].name)
        self.unlock_part(body_parts["foot_R"].name)

    def set_joint_roll(self, pivot_name, roll_angle):
        pivot = bpy.data.objects[pivot_name]
        pivot.rotation_euler[2] = roll_angle

def main():
    # Ensure correct context
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    # Delete all mesh objects
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    bpy.context.scene.frame_end = 50

    
    body = Body(False, 1.86, 0., 86, canDoPullup=True, canDoPistleSquat=True)
    
    
    # Example usage
    #lock_hands_and_feet(body_parts)
    # Unlock hands and feet later if needed
    # unlock_hands_and_feet(body_parts)

    # Set roll angle for a joint
    # set_joint_roll("torso_head_pivot", 1.5708)  # Example to set roll to 90 degrees



    #register update function with blender callback: https://docs.blender.org/api/current/bpy.app.handlers.html#note-on-altering-data
    #bpy.app.handlers.frame_change_post.append(function name)
    #need to add (@persistent) before function else socket file will be closed


if __name__ == "__main__":
    main()



#apply force to specific object in scene

# import bpy

# # Get the force field object
# force_field = bpy.data.objects["ForceField"]

# # Get the objects you want to target
# cube1 = bpy.data.objects["Cube1"]
# cube2 = bpy.data.objects["Cube2"]

# # Create a list of the target objects
# target_objects = [cube1, cube2]

# # Iterate through the force field's influence objects
# for influence_obj in force_field.force_field.influences:
#     # Check if the influence object is in the target list
#     if influence_obj.object in target_objects:
#         # Keep the influence
#         influence_obj.use_influence = True
#     else:
#         # Remove the influence
#         influence_obj.use_influence = False


# import bpy

# # Create a new collection (if needed)
# new_collection = bpy.data.collections.new("ForceFieldTargets")
# bpy.context.scene.collection.children.link(new_collection)

# # Get the objects you want to target
# cube1 = bpy.data.objects["Cube1"]
# cube2 = bpy.data.objects["Cube2"]

# # Add the objects to the collection
# new_collection.objects.link(cube1)
# new_collection.objects.link(cube2)

# # Get the force field object
# force_field = bpy.data.objects["ForceField"]

# # Set the force field's target collection
# force_field.force_field.collections = [new_collection]


# import bpy

# def setup_force_fields():
#     """Sets up force fields for each group."""
#     groups = {
#         "GroupA": ["Cube1", "Cube2", "Cube3"],
#         "GroupB": ["Sphere1", "Sphere2"],
#         "GroupC": ["Plane1", "Plane2"]
#     }

#     for group_name, object_names in groups.items():
#         # Create a force field if it doesn't exist
#         force_field_name = f"ForceField_{group_name}"
#         if force_field_name not in bpy.data.objects:
#             bpy.ops.object.force_field_add(type='FORCE', enter_editmode=False, align='WORLD', location=(0, 0, 0))
#             bpy.context.object.name = force_field_name

#         # Get the force field object
#         force_field = bpy.data.objects[force_field_name]

#         # Get the collection
#         collection = bpy.data.collections.get(group_name)
#         if not collection:
#             print(f"Error: Collection '{group_name}' not found.")
#             continue

#         # Set the force field's target collection
#         force_field.force_field.collections = [collection] 

#         # Get the objects for the group
#         for object_name in object_names:
#             object = bpy.data.objects.get(object_name)
#             if object:
#                 collection.objects.link(object) 

# setup_force_fields()

#add 249 to force to cancel out gravity for some reason

#https://blender.stackexchange.com/questions/266877/how-can-i-get-the-rotation-value-of-an-object-after-physics-simulation-without-k
#after baking, we can set the Frame suing frame_set to what every next frame to get the final position for the next simulation iteration