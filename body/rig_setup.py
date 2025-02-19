
import sys
import os
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


class setup:

    def __init__(self, rootJnt):
        print(f"Initializing setup with root joint: {rootJnt}")
        self.rootJnt = rootJnt

    def root_setup(self):

        masterGrp, masterCtrl = controller.create_temp_ctrl(name = f'master_{CONTROL}', lock = ['v'])
        
        skelGrp = cmds.group(n = f'skeleton_{GROUP}', empty= True)
        dontTouchGrp = cmds.group(n = f'dontTouch_{GROUP}', empty= True)

        cmds.parent(skelGrp, masterCtrl)
        cmds.parent(dontTouchGrp, masterGrp)
        cmds.parent(self.rootJnt, skelGrp)

        offsetGrp, offsetCtrl = controller.create_temp_ctrl(name= f'offset_{CONTROL}', lock = ['sx', 'sy', 'sz', 'v'])
        rootGrp, rootCtrl = controller.create_temp_ctrl(name = f'root_{CONTROL}', lock = ['sx', 'sy', 'sz', 'v'])

        cmds.parent(offsetGrp, masterCtrl)
        cmds.parent(rootGrp, offsetCtrl)
        print("Root setup complete")

    def attr_ctrl(self):

        ctrl_grp, ctrl = controller.create_temp_ctrl(f'{CENTER}_attr_{CONTROL}', lock=['sx', 'sy', 'sz','rx', 'ry', 'rz', 'tx', 'ty', 'tz'])
        cmds.addAttr(ctrl, ln='skeleton_vis', at='enum', en = "off:on", k=True, h=False)
        cmds.addAttr(ctrl, ln='stretch_ctrls_vis', at='enum', en = "off:on", k=True, h=False)

        cmds.connectAttr(f'{ctrl}.skeleton_vis', 'L_rev_GRP.visibility')
        cmds.connectAttr(f'{ctrl}.skeleton_vis', 'R_rev_GRP.visibility')
        cmds.connectAttr(f'{ctrl}.skeleton_vis', 'root_JNT.visibility')


