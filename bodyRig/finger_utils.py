import sys
import maya.cmds as cmds

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import create_tempCtrl
from general_functions import addOffset


GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'
FINGER = 'finger'

#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'

finger_knuckles = ['_00', '_01', '_02', '_03', '_end']
thumb_knuckles = ['_00', '_01', '_02', '_end']


def fk_fingers_ctrls(fingers = []):

    for finger in fingers:

        if 'thumb' in finger:
            knuckles = thumb_knuckles
        else:
            knuckles = finger_knuckles

        for num, knuckle in enumerate(knuckles):
            knuckle = f'{finger}{knuckle}_{JOINT}'
            FK_grp, FK_ctrl = create_tempCtrl(knuckle.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

            mat = cmds.xform(knuckle, q=True, m=True, ws=True)
            cmds.xform(FK_grp, m=mat, ws=True)

            cmds.parentConstraint(FK_ctrl, knuckle, mo=True)

            if num != 0:
                prev_jnt = knuckles[num-1]
                prev_ctrl  = f'{finger}{prev_jnt}_{CONTROL}'
                cmds.parent(FK_grp, prev_ctrl)


def fingers_attr(wristJnt, fingers = []):

    #create handController
    mat = cmds.xform(wristJnt, q=True, m=True, ws=True)
    if 'End' in wristJnt:
        hand_name = wristJnt.replace('wristEnd', 'hand')
    else:
        hand_name = wristJnt.replace('wrist', 'hand')

    hand_grp, hand_ctrl = create_tempCtrl(hand_name.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz'])
    cmds.xform(hand_grp, m=mat, ws=True)



    # create offsets for attributes to be connected too
    for finger in fingers:
        #create attributes
        cmds.addAttr(hand_ctrl, ln=f'{finger}_curl', at='double', k=True)



        # create offsets for attributes to be connected too
        if 'thumb' in finger:
            knuckles = thumb_knuckles
        else:
            knuckles = finger_knuckles

        for num, knuckle in enumerate(knuckles):
            knuckle_ctrl = f'{finger}{knuckle}_{CONTROL}'
            offset = addOffset(knuckle_ctrl, suffix='OFF')

            #connect attributes
            if 'A' not in offset:
                cmds.connectAttr(f'{hand_ctrl}.{finger}_curl', f'{offset}.ry')

def FK_fingers(wristJnt, fingers = []):
    fk_fingers_ctrls(fingers)
    fingers_attr(wristJnt, fingers)

