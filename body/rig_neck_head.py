import maya.cmds as cmds
import math
import sys
import os 
import importlib

sys.path.append('/home/s5725067/myRepos/autoRig/')
import rig_constants
importlib.reload(rig_constants)
from rig_constants import *

sys.path.append('/home/s5725067/myRepos/autoRig/utils/')
import controller_utils
importlib.reload(controller_utils)
from controller_utils import controller


class neck_head:
    
    def __init__(self):
        self.neckJnts = []
        self.headJnt = headJnt

    def duplicate_chain(self, prefix):
        cmds.select(d=True)
        duplicated_joints = []
        for jnt in self.neckJnts:
            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            dupl_jnt = cmds.joint(n=jnt.replace(JOINT, f'{prefix}_{JOINT}'))
            cmds.xform(dupl_jnt, m=mat, ws=True)
            cmds.makeIdentity(dupl_jnt, apply=True, r=True)
            duplicated_joints.append(dupl_jnt)
        

    def fk_neck(self):
        self.duplicate_chain('FK')
        neck_ctrls = []
        for jnt in self.neckJnts:
            FK_grp, FK_ctrl = controller.create_temp_ctrl(jnt.replace(JOINT, f'FK_{CONTROL}'))
            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            cmds.xform(FK_grp, m=mat, ws=True)
            cmds.parentConstraint(FK_ctrl, jnt)
            neck_ctrls.append(FK_ctrl)
        
        for enum, ctrl in enumerate(neck_ctrls):
            if enum != 0:
                prev_ctrl = neck_ctrls[enum-1]
                cmds.
        
        for i in range(len(neck_ctrls) - 1):
            prev_ctrl = neck_ctrls[i-1]

        cmds.parent(neck_ctrls[0], self.neckJnts[0].replace(JOINT, 'FK_' + GROUP))




def main():
    print("reopening file")
    current_file = cmds.file(q=True, sn=True)
    if current_file:
        cmds.file(current_file, o=True, f=True)
    else:
        print("No file to open")

    print("Running main")

    neck_head_rig = neck_head(neckJnts = ['spineEnd_JNT', 'neckA_JNT', 'neckB_JNT'], headJnt = 'head_JNT')
    neck_head_rig.fk_neck()
    print("neck_head rig created successfully") 
    