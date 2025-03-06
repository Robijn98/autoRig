import sys
import maya.cmds as cmds
import importlib

sys.path.append('/home/s5725067/myRepos/autoRig/')
import rig_constants
importlib.reload(rig_constants)
from rig_constants import *

sys.path.append('/home/s5725067/myRepos/autoRig/utils/')
import controller_utils
importlib.reload(controller_utils)
from controller_utils import controller


class hand:
    def __init__(self):
        print("Initializing hand rig")

class hand:
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
                knuckle = f'{finger}{knuckle}_{JOINT}'
                FK_grp, FK_ctrl = controller.create_temp_ctrl(knuckle.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

                mat = cmds.xform(knuckle, q=True, m=True, ws=True)
                cmds.xform(FK_grp, m=mat, ws=True)

                cmds.parentConstraint(FK_ctrl, knuckle, mo=True)

                if num != 0:
                    prev_jnt = knuckles[num-1]
                    prev_ctrl  = f'{finger}{prev_jnt}_{CONTROL}'
                    cmds.parent(FK_grp, prev_ctrl)


    def fingers_attr(self):
        #create handController
        mat = cmds.xform(self.wristJnt, q=True, m=True, ws=True)
        if 'End' in self.wristJnt:
            hand_name = self.wristJnt.replace('wristEnd', 'hand')
        else:
            hand_name = self.wristJnt.replace('wrist', 'hand')

        hand_grp, hand_ctrl = controller.create_temp_ctrl(hand_name.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz'])
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
                knuckle_ctrl = f'{finger}{knuckle}_{CONTROL}'
                offset = controller.add_offset(knuckle_ctrl, suffix='OFF')

                #connect attributes
                if '_01' not in offset:
                    cmds.connectAttr(f'{hand_ctrl}.{finger}_curl', f'{offset}.rz')

    
    def fingers_rig(self):
        self.fk_fingers()
        self.fingers_attr()

