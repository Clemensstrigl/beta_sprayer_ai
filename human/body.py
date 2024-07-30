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
            {"name": "head", "radius": 0.0625*self.height, "location": (0, 0, 0.9375*self.height), "active": False},
            #{"name": "neck", "radius": 0.03, "height": 0.3, "location": (0, 0, 1.8)},
            {"name": "chest", "radius": 0.1*self.height, "location": (0, 0, 0.7708*self.height),"active": False},
            {"name": "stomach", "radius": 0.075*self.height, "location": (0, 0, 0.595*self.height)},
            {"name": "hips", "radius": 0.05*self.height, "height": 0.15*self.height, "location": (0, 0, 0.4708*self.height),              "rotation": (0, 1.5708, 0)},
            {"name": "collar", "radius": 0.0375*self.height, "height": 0.2*self.height, "location": (0, 0, 0.8125*self.height),      "rotation": (0, 1.5708, 0)},
            #{"name": "collar_R", "radius": 0.0375*self.height, "height": 0.1*self.height, "location": (0.05*self.height, 0, 0.8125*self.height),       "rotation": (0, 1.5708, 0)},
            {"name": "upper_arm_L", "radius": 0.03*self.height, "height": 0.1875*self.height + ape_index_addon, "location": (-0.1938*self.height - ape_index_center_offset, 0, 0.8125*self.height),  "rotation": (0, 1.5708, 0)},
            {"name": "upper_arm_R", "radius": 0.03*self.height, "height": 0.1875*self.height + ape_index_addon, "location": (0.1938*self.height+ ape_index_center_offset, 0, 0.8125*self.height),   "rotation": (0, 1.5708, 0)},
            {"name": "lower_arm_L", "radius": 0.029*self.height, "height": 0.1667*self.height + ape_index_addon, "location": (-0.3708*self.height- ape_index_addon -ape_index_center_offset, 0, 0.8125*self.height),    "rotation": (0, 1.5708, 0)},
            {"name": "lower_arm_R", "radius": 0.029*self.height, "height": 0.1667*self.height + ape_index_addon, "location": (0.3708*self.height+ ape_index_addon + ape_index_center_offset, 0, 0.8125*self.height),     "rotation": (0, 1.5708, 0)},
            {"name": "hand_L", "radius": 0.03*self.height,  "location": (-0.4708*self.height- ape_index_addon*2, 0, 0.8125*self.height),                       "rotation": (0, 1.5708, 0)},
            {"name": "hand_R", "radius": 0.03*self.height,  "location": (0.4708*self.height+ ape_index_addon*2, 0, 0.8125*self.height),                        "rotation": (0, 1.5708, 0)},
            {"name": "upper_leg_L", "radius": 0.03*self.height, "height": 0.2083*self.height, "location": (-0.0417*self.height, 0, 0.325*self.height)},
            {"name": "upper_leg_R", "radius": 0.03*self.height, "height": 0.2083*self.height, "location": (0.0417*self.height, 0, 0.325*self.height)},
            {"name": "lower_leg_L", "radius": 0.029*self.height, "height": 0.1667*self.height, "location": (-0.0417*self.height, 0, 0.1375*self.height)},
            {"name": "lower_leg_R", "radius": 0.029*self.height, "height": 0.1667*self.height, "location": (0.0417*self.height, 0, 0.1375*self.height)},
            {"name": "foot_L", "radius": 0.03*self.height,  "location": (-0.0417*self.height, 0, 0.03*self.height)},
            {"name": "foot_R", "radius": 0.03*self.height,  "location": (0.0417*self.height, 0, 0.03*self.height)},
        ]
    
    def get_segment_attr(self, segment, attr):
        for s in self.body_segments:
            if segment in s["name"]:
                if attr in s.keys():
                    return s[attr]
                elif attr == "height":
                    return s["radius"]*2
                return None

    def create_body(self,):
        body_parts = {}
        
       

        
        

        
        # Create pipes for each body segment
        for segment in self.body_segments:
            rotation = segment.get("rotation", (0, 0, 0))
            if "height" in segment:
                body_parts[segment["name"]] = self.create_pipe(segment["name"], segment["radius"], segment["height"], segment["location"], rotation)
            else:
                body_parts[segment["name"]] = self.create_sphere(segment["name"], segment["radius"], segment["location"], rotation)

            
        return body_parts
    
    def get_obj_loc(self, obj_name):
        if "collar" in obj_name:
            if "L" in obj_name:
                loc = list(self.get_segment_attr("collar", "location"))
                loc[0] = loc[0] - self.get_segment_attr("collar", "height")/2
                return tuple(loc)
            if "R" in obj_name:
                loc = list(self.get_segment_attr("collar", "location"))
                loc[0] = loc[0] + self.get_segment_attr("collar", "height")/2
                return tuple(loc)
            return self.get_segment_attr("collar", "location")
        if "hips" in obj_name:
            if "L" in obj_name:
                loc = list(self.get_segment_attr("hips", "location"))
                loc[0] = list(self.get_segment_attr("lower_leg_L", "location"))[0]
                return tuple(loc)
            if "R" in obj_name:
                loc = list(self.get_segment_attr("hips", "location"))
                loc[0] = list(self.get_segment_attr("lower_leg_R", "location"))[0]
                return tuple(loc)
            return self.get_segment_attr("hips", "location")

        return self.get_segment_attr(obj_name, "location")
        
            

        
    def add_armature(self, body_parts):
        bpy.ops.object.armature_add()
        armature = bpy.context.object
        armature.name = 'Armature'
        
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        edit_bones = armature.data.edit_bones
        
        # Define bones and their connections
        bones_data = [
            #("chest", None),
            
            ("chest", "stomach"),
            ("stomach", "hips"),
            ("collar", "chest"),
            ("head", "collar"),

            ("collar_L", "collar"),
            ("collar_R", "collar"),
            ("collar", "chest"),
            ("upper_arm_L", "collar_L"),
            ("upper_arm_R", "collar_L"),
            ("lower_arm_L", "upper_arm_L"),
            ("lower_arm_R", "upper_arm_R"),
            ("hand_L", "lower_arm_L"),
            ("hand_R", "lower_arm_R"),
            ("hips_L", "hips"),
            ("hips_R", "hips"),
            ("upper_leg_L", "hips_L"),
            ("upper_leg_R", "hips_R"),
            ("lower_leg_L", "upper_leg_L"),
            ("lower_leg_R", "upper_leg_R"),
            ("foot_L", "lower_leg_L"),
            ("foot_R", "lower_leg_R"),
        ]










        
        for bone_name, parent_name in bones_data:
            bone = edit_bones.new(bone_name)
            parent_loc = list(self.get_obj_loc(parent_name))
            child_loc = list(self.get_obj_loc(bone_name))
            bone_length = self.get_segment_attr(bone_name, "height")


            if "collar" in parent_name:
                if "collar_L" in bone_name:
                    child_loc[0] = body_parts[parent_name].location[0] - self.get_segment_attr(parent_name, "height")/2
                    bone_length = self.get_segment_attr(parent_name, "height")/2

                elif "collar_R" in bone_name:
                    child_loc[0] = body_parts[parent_name].location[0] + self.get_segment_attr(parent_name, "height")/2
                    bone_length = self.get_segment_attr(parent_name, "height")/2

                elif "arm_L" in bone_name:
                    parent_loc[0] = body_parts["collar"].location[0] - self.get_segment_attr("collar", "height")/2
                    child_loc[0] = body_parts[bone_name].location[0] - self.get_segment_attr(bone_name, "height")/2

                elif "arm_R" in bone_name:
                    parent_loc[0] = body_parts["collar"].location[0] + self.get_segment_attr("collar", "height")/2
                    child_loc[0] = body_parts[bone_name].location[0] + self.get_segment_attr(bone_name, "height")/2

            

                    
            elif "hips" in parent_name:
                if "hips_L" in bone_name:

                    child_loc[0] = self.get_segment_attr("upper_leg_L","location")[0]
                    bone_length = self.get_segment_attr(parent_name, "height")/2 + self.get_segment_attr("upper_leg_L", "radius")/2

                elif "hips_R" in bone_name:
                    child_loc[0] = self.get_segment_attr("upper_leg_R","location")[0]
                    bone_length = self.get_segment_attr(parent_name, "height")/2 + self.get_segment_attr("upper_leg_L", "radius")/2
                
                elif "leg_L" in bone_name:
                    print(bone_name)
                    child_loc[2] = child_loc[2] - self.get_segment_attr(bone_name, "height")/2

                elif "leg_R" in bone_name:
                    child_loc[2] = child_loc[2] - self.get_segment_attr(bone_name, "height")/2


            elif 'leg' in parent_name:
                child_loc = body_parts[bone_name].location
                parent_loc[2] = parent_loc[2] - self.get_segment_attr(parent_name, "height")/2
                child_loc[2] = child_loc[2] - self.get_segment_attr(bone_name, "height")/2

            elif 'arm' in parent_name:
                child_loc = body_parts[bone_name].location
                parent_loc[0] = parent_loc[0] - self.get_segment_attr(parent_name, "height")/2
                child_loc[0] = child_loc[0] - self.get_segment_attr(bone_name, "height")/2

            print(bone_name)
            bone.length = bone_length
            bone.head = tuple(parent_loc)
            if child_loc:
                bone.tail = tuple(child_loc)
            
         
            
            if parent_name in edit_bones:
                bone.parent = edit_bones[parent_name]
            
        

        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Parent each body part to its corresponding bone and hide the body parts
        for bone_name, body_part in body_parts.items():
            print(bone_name, body_part.name)
            bpy.context.view_layer.objects.active = body_part
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)
            bpy.ops.object.hide_viewport = True  # Hide body parts
        
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