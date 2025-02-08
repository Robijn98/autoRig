import sys
import maya.cmds as cmds

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import create_tempCtrl

GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'
ARM = 'arm'
LEG = 'leg'
STRETCH = 'stretchy'


#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'

def stretch_joints(joint1, joint2, joint3, ik_ctrl, side):
    cmds.select(clear=True)
    #duplicate chain
    for  jnt in [joint1, joint2, joint3]:
        mat = cmds.xform(jnt, q=True, m=True, ws=True)
        dupl_jnt = cmds.joint(n = jnt.replace(JOINT, f'scale_{JOINT}'))
        cmds.xform(dupl_jnt, m=mat, ws=True)
        cmds.makeIdentity(dupl_jnt, apply=True, r=True)



def stretchy_proporties(joint1, joint2, joint3, part, ik_ctrl, side):
    #create root ctrl

    root_grp, root_ctrl = create_tempCtrl(f'{side}_{part}_root_CTRL', lock=['sx', 'sy', 'sz'])
    mat = cmds.xform(joint1, q=True, m=True, ws=True)
    cmds.xform(root_grp, m=mat, ws=True)


    #measure distance between the limbs
    joint1_stretch = joint1.replace(JOINT, f'scale_{JOINT}')
    joint2_stetch = joint2.replace(JOINT, f'scale_{JOINT}')
    joint3_stretch = joint3.replace(JOINT, f'scale_{JOINT}')


    dis_upper = cmds.createNode('distanceBetween', n=f'{side}_upper_dist')
    dis_lower = cmds.createNode('distanceBetween', n=f'{side}_lower_dist')

    cmds.connectAttr(f'{joint1_stretch}.worldMatrix[0]', f'{dis_upper}.inMatrix1')
    cmds.connectAttr(f'{joint2_stetch}.worldMatrix[0]', f'{dis_upper}.inMatrix2')

    cmds.connectAttr(f'{joint2_stetch}.worldMatrix[0]', f'{dis_lower}.inMatrix1')
    cmds.connectAttr(f'{joint3_stretch}.worldMatrix[0]', f'{dis_lower}.inMatrix2')

    doubleLin = cmds.createNode('addDoubleLinear', n=f'{side}_fullDist')

    cmds.connectAttr(f'{dis_upper}.distance', f'{doubleLin}.input1')
    cmds.connectAttr(f'{dis_lower}.distance', f'{doubleLin}.input2')

    fullDist_distance = cmds.getAttr(f'{doubleLin}.output')

    #measure distance to the IK_Ctrl
    loc_end = cmds.spaceLocator(n=f'{side}_{part}_stretchEnd')
    cmds.hide(loc_end)
    mat = cmds.xform(ik_ctrl, q=True, m=True, ws=True)
    cmds.xform(loc_end, m=mat, ws=True)
    cmds.parent(loc_end, ik_ctrl)

    dis_stretch = cmds.createNode('distanceBetween', n=f'{side}_stretchDist1')
    cmds.connectAttr(f'{side}_{part}_root_CTRL.worldMatrix[0]', f'{dis_stretch}.inMatrix1')
    cmds.connectAttr(f'{loc_end[0]}.worldMatrix[0]', f'{dis_stretch}.inMatrix2')
    dis_stretch_distance = cmds.getAttr(f'{dis_stretch}.distance')


    #condition to check if IK is longer than ge
    con = cmds.createNode('condition', n=f'{side}_condition')
    cmds.connectAttr(f'{dis_stretch}.distance', f'{con}.firstTerm')
    cmds.connectAttr(f'{doubleLin}.output', f'{con}.secondTerm')


    multDiv = cmds.createNode('multiplyDivide', n = f'{side}_multi')
    cmds.connectAttr(f'{con}.outColorR', f"{joint1.replace(JOINT, f'IK_JNT')}.scaleX")
    cmds.connectAttr(f'{con}.outColorR', f"{joint2.replace(JOINT, f'IK_JNT')}.scaleX")

    #cmds.connectAttr(f'{con}.outColorR', f'{side}_shoulder_IK_JNT.scaleX')
    #cmds.connectAttr(f'{con}.outColorR', f"{side}_elbow_IK_JNT.scaleX")


    cmds.connectAttr(f'{dis_stretch}.distance', f'{multDiv}.input1X')
    cmds.connectAttr(f'{doubleLin}.output', f'{multDiv}.input2X')
    cmds.setAttr(f'{multDiv}.operation', 2)

    #connect the scale to the joints
    cmds.setAttr(f'{con}.operation', 2)
    cmds.connectAttr(f'{multDiv}.outputX', f'{con}.colorIfTrueR')


    #on and off switch
    cmds.addAttr(ik_ctrl, ln='stretch',  at='enum', en='off:stretch:squash', k=True)

    con_stretch = cmds.createNode('condition')

    cmds.connectAttr(f'{ik_ctrl}.stretch', f'{con_stretch}.firstTerm')
    cmds.setAttr(f'{con_stretch}.colorIfTrueR', 0)
    cmds.setAttr(f'{con_stretch}.colorIfFalseR', 2)

    con_squash = cmds.createNode('condition')

    cmds.connectAttr(f'{ik_ctrl}.stretch', f'{con_squash}.firstTerm')
    cmds.setAttr(f'{con_squash}.colorIfTrueR', 0)
    cmds.setAttr(f'{con_squash}.colorIfFalseR', 4)

    con_off = cmds.createNode('condition')

    cmds.connectAttr(f'{con_squash}.outColorR', f'{con_off}.colorIfTrueR')
    cmds.connectAttr(f'{con_stretch}.outColorR', f'{con_off}.colorIfFalseR')

    cmds.connectAttr(f'{ik_ctrl}.stretch', f'{con_off}.firstTerm')


    cmds.setAttr(f'{con_off}.secondTerm', 2)
    cmds.connectAttr(f'{con_off}.outColorR', f'{con}.operation')




# #execute
# stretch_joints('L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT', 'L_IK_wrist_CTRL', LEFT)
# stretchy_proporties('L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT', ARM, 'L_IK_wrist_CTRL', LEFT)

# stretch_joints('R_shoulder_JNT', 'R_elbow_JNT', 'R_wrist_JNT', 'R_IK_wrist_CTRL', RIGHT)
# stretchy_proporties('R_shoulder_JNT', 'R_elbow_JNT', 'R_wrist_JNT', ARM, 'R_IK_wrist_CTRL', RIGHT)

# stretch_joints('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT', 'L_IK_ankle_CTRL', LEFT)
# stretchy_proporties('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT',LEG, 'L_IK_ankle_CTRL', LEFT)

# stretch_joints('R_hip_JNT', 'R_knee_JNT', 'R_ankle_JNT', 'R_IK_ankle_CTRL', RIGHT)
# stretchy_proporties('R_hip_JNT', 'R_knee_JNT', 'R_ankle_JNT',LEG, 'R_IK_ankle_CTRL', RIGHT)