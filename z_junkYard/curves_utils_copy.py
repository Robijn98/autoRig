import maya.cmds as cmds
import json
import os

def get_ctrls(master_group):
    all_children = cmds.listRelatives(master_group, allDescendents =True)
    all_ctrls = []
    for child in all_children:
        if "CTRL" in child:
            if "Shape" not in child and "OFF" not in child:
                all_ctrls.append(child)
        
    return all_ctrls



def extract_curve_data(ctrls = []):
    curves_data = []
    print(f"Extracting data for {len(ctrls)} curves")
    
    for ctrl in ctrls:
        print(f"Extracting data for {ctrl}")
        

        #in case of multiple shapes do a for loop
        shapes = cmds.listRelatives(ctrl, shapes=True)
        if not shapes:
            print(f"Curve '{ctrl}' has no shapes.")
            return None

        for shape in shapes:
            #connect a curveinfo node
            curve_info = cmds.createNode("curveInfo")
            cmds.connectAttr(f"{shape}.worldSpace[0]", f"{curve_info}.inputCurve", f=True)

            #get the curve knots
            knots = cmds.getAttr(f"{curve_info}.knots")

            #get degree
            degree = cmds.getAttr(f"{shape}.degree")

            # Get CV positions
            num_cvs = cmds.getAttr(f"{curve_info}.controlPoints", size=True)
            cv_positions = [cmds.getAttr(f"{curve_info}.controlPoints[{i}]")[0] for i in range(num_cvs)]

            # Get color
            color = None  # Default to None in case it's not set
            if cmds.getAttr(f"{shape}.overrideEnabled"):
                if cmds.getAttr(f"{shape}.overrideRGBColors"):
                    r = cmds.getAttr(f"{shape}.overrideColorR")
                    g = cmds.getAttr(f"{shape}.overrideColorG")
                    b = cmds.getAttr(f"{shape}.overrideColorB")
                    color = [r, g, b]
                else:
                    color = cmds.getAttr(f"{shape}.overrideColor")

            #remove curveinfo
            cmds.delete(curve_info)

            # Package the data
            curve_data = {
                "name": ctrl,
                "points": cv_positions,
                "degree": degree,
                "knots": knots,
                "color": color
            }

            # Add to list
            curves_data.append(curve_data)       

    return curves_data



def save_curve_to_json(master_group, file = "curve_data.json"):
    #create file in cache
    project_path = os.getcwd()
    file_path = os.path.join(project_path, file)
    
    with open(file_path, "w") as f:
        ctrls = get_ctrls(master_group)
        curve_data = extract_curve_data(ctrls)
        json.dump(curve_data, f, indent = 1)
        print(f"Curve data saved to {file_path}")

                    


def replace_curves(master_group, file = "curve_data.json"):
    project_path = os.getcwd()
    file_path = os.path.join(project_path, file)

    with open(file_path, "r") as f:
        curve_data = json.load(f)

    ctrls = get_ctrls(master_group)   
    ctrls = ["L_IK_wrist_CTRL", "R_IK_wrist_CTRL"]

    print(f"Replacing {len(ctrls)} curves")

    for ctrl in ctrls:
        shapes = cmds.listRelatives(ctrl, shapes=True)

        if not shapes:
            print(f"WARNING: No shapes found for {ctrl}")
        else:
            for shape in shapes:
                cmds.delete(shape)

            for data in curve_data:
                if data["name"] == ctrl:
                    curve = cmds.curve(d = data["degree"], p = data["points"], k= data["knots"][0], n = data["name"] + "_TEMP")

                    #parent the curve to the ctrl, maintainin the offset
                    newShape = cmds.listRelatives(curve, shapes=True)[0]

                    # #move the shape to 0,0,0
                    # cmds.CenterPivot(curve)
                    # cmds.move(0,0,0, curve,  rpr =True)
                    # cmds.makeIdentity(curve, a=True, t=True, r=True, s=True, n=False, pn=True)
                    # cmds.parent(newShape, ctrl, r=True, s=True)

                    if data["color"]:
                        cmds.setAttr(f"{newShape}.overrideEnabled", 1)
                        cmds.setAttr(f"{newShape}.overrideRGBColors", 1)
                        cmds.setAttr(f"{newShape}.overrideColorR", data["color"][0])
                        cmds.setAttr(f"{newShape}.overrideColorG", data["color"][1])
                        cmds.setAttr(f"{newShape}.overrideColorB", data["color"][2])





def create_curve(file = "curve_data.json"):
    project_path = os.getcwd()
    file_path = os.path.join(project_path, file)

    with open(file_path, "r") as f:
        curve_data = json.load(f)
        for data in curve_data:
            print(f"knots: {data['knots']}")
            print(f"points: {data['points']}")
            curve = cmds.curve(d = data["degree"], p = data["points"], k= data["knots"][0], n = data["name"] + "_TEMP")
            if data["color"]:
                cmds.setAttr(f"{curve}.overrideEnabled", 1)
                cmds.setAttr(f"{curve}.overrideRGBColors", 1)
                cmds.setAttr(f"{curve}.overrideColorR", data["color"][0])
                cmds.setAttr(f"{curve}.overrideColorG", data["color"][1])
                cmds.setAttr(f"{curve}.overrideColorB", data["color"][2])



def main():
    #save_curve_to_json("master_GRP", file = "curve_data.json")
    replace_curves("master_GRP", file = "curve_data.json")