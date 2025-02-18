import sys
import maya.cmds as cmds
from controller import create_temp_ctrl
from controller import add_offset

class hand:

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

    def __init__(self, wristJnt, fingers = []):
        self.wristJnt = wristJnt
        self.fingers = fingers

    
    def fk_fingers(self):
        for finger in self.fingers:

            if 'thumb' in finger:
                knuckles = self.thumb_knuckles
            else:
                knuckles = self.finger_knuckles

            for num, knuckle in enumerate(knuckles):
                knuckle = f'{finger}{knuckle}_{self.JOINT}'
                FK_grp, FK_ctrl = create_temp_ctrl(knuckle.replace(self.JOINT, self.CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

                mat = cmds.xform(knuckle, q=True, m=True, ws=True)
                cmds.xform(FK_grp, m=mat, ws=True)

                cmds.parentConstraint(FK_ctrl, knuckle, mo=True)

                if num != 0:
                    prev_jnt = knuckles[num-1]
                    prev_ctrl  = f'{finger}{prev_jnt}_{self.CONTROL}'
                    cmds.parent(FK_grp, prev_ctrl)


    def fingers_attr(self):
        #create handController
        mat = cmds.xform(self.wristJnt, q=True, m=True, ws=True)
        if 'End' in self.wristJnt:
            hand_name = self.wristJnt.replace('wristEnd', 'hand')
        else:
            hand_name = self.wristJnt.replace('wrist', 'hand')

        hand_grp, hand_ctrl = create_temp_ctrl(hand_name.replace(self.JOINT, self.CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz'])
        cmds.xform(hand_grp, m=mat, ws=True)

        # create offsets for attributes to be connected too
        for finger in self.fingers:
            #create attributes
            cmds.addAttr(hand_ctrl, ln=f'{finger}_curl', at='double', k=True)

            # create offsets for attributes to be connected too
            if 'thumb' in finger:
                knuckles = self.thumb_knuckles
            else:
                knuckles = self.finger_knuckles

            for num, knuckle in enumerate(knuckles):
                knuckle_ctrl = f'{finger}{knuckle}_{self.CONTROL}'
                offset = add_offset(knuckle_ctrl, suffix='OFF')

                #connect attributes
                if '_01' not in offset:
                    cmds.connectAttr(f'{hand_ctrl}.{finger}_curl', f'{offset}.ry')

    
    def FK_fingers(self):
        self.fk_fingers()
        self.fingers_attr()

# fk_fingers('L_wristJNT', ['L_index', 'L_middle', 'L_ring', 'L_pinky', 'L_thumb'])
