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

import polevector
importlib.reload(polevector)
from polevector import poleVector


class IKFK_leg_quarduped:
    
    def __init__(self, hipJnt, kneeJnt, ankleJnt, footJnt, ballJnt, toeJnt, side):
        self.hipJnt = hipJnt
        self.kneeJnt = kneeJnt
        self.ankleJnt = ankleJnt
        self.footJnt = footJnt
        self.ballJnt = ballJnt
        self.toeJnt = toeJnt
        self.side = side


    def duplicate_chain(self, prefix):
        cmds.select(d=True)
        duplicated_joints = []
        for jnt in [self.hipJnt, self.kneeJnt, self.ankleJnt, self.footJnt, self.ballJnt, self.toeJnt]:
            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            dupl_jnt = cmds.joint(n=jnt.replace(JOINT, f'{prefix}_{JOINT}'))
            cmds.xform(dupl_jnt, m=mat, ws=True)
            cmds.makeIdentity(dupl_jnt, apply=True, r=True)
            duplicated_joints.append(dupl_jnt)
                

    def ik_leg(self):
        self.duplicate_chain('IK')
        leg_ik = cmds.ikHandle(sj = self.hipJnt.replace(JOINT, 'IK_' + JOINT), 
                                ee= self.ankleJnt.replace(JOINT, 'IK_' + JOINT), 
                                sol = 'ikRPsolver', n = f'{self.side}_{LEG}_IK')

        pv = cmds.spaceLocator(n = f'{self.side}_{LEG}_polevector')
        leg_poleVec = poleVector(self.hipJnt, self.kneeJnt, self.ankleJnt)
        pv_t = leg_poleVec.find_polevector(scalar = 5)
        cmds.xform(pv, t=pv_t)
        cmds.poleVectorConstraint(pv, leg_ik[0])

        #temp control creation
        IK_grp, IK_ctrl = controller.create_temp_ctrl(f'{self.side}_IK_ankle_{CONTROL}', lock=['sx', 'sy', 'sz'])
        mat = cmds.xform(self.footJnt, q=True, m=True, ws=True) 
        cmds.xform(IK_grp, m=mat, ws=True)
        if self.side == LEFT:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', 90)
            cmds.setAttr(f'{IK_grp}.rotateZ', 0)
        else:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', -90)
        cmds.parent(leg_ik[0], IK_ctrl)
        cmds.parent(pv, IK_ctrl)
        pv_grp, pv_ctrl = controller.create_temp_ctrl(f'{self.side}_leg_pv_{CONTROL}', lock=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'])
        mat = cmds.xform(pv, q=True, m=True, ws=True)
        cmds.xform(pv_grp, m=mat, ws=True)
        cmds.parent(pv, pv_ctrl)
        cmds.hide(pv)



    def fk_leg(self):
        self.duplicate_chain('FK')
        for num, jnt in enumerate([self.hipJnt, self.kneeJnt, self.ankleJnt, self.footJnt, self.ballJnt]):
            FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
            FK_grp, FK_ctrl = controller.create_temp_ctrl(FK_jnt.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            cmds.xform(FK_grp, m=mat, ws=True)

            cmds.parentConstraint(FK_ctrl, FK_jnt, mo=True)

            jnts = [self.hipJnt, self.kneeJnt, self.ankleJnt, self.ballJnt]
            if jnt != self.hipJnt:
                prev_jnt = jnts[num-1]
                prev_ctrl = prev_jnt.replace(JOINT, f'FK_{CONTROL}')
                cmds.parent(FK_grp, prev_ctrl)
                

    def IKFK_switch(self):
        cmds.addAttr(f'{self.side}_IK_ankle_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True)
        cmds.addAttr(f'{self.side}_leg_pv_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True, proxy=f'{self.side}_IK_ankle_{CONTROL}.IK_FK_Switch')

        for jnt in [self.hipJnt, self.kneeJnt, self.ankleJnt, self.footJnt, self.ballJnt, self.toeJnt]:
            FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
            FK_ctrl = FK_jnt.replace(JOINT, CONTROL)
            cmds.addAttr(FK_ctrl, ln='IK_FK_Switch', at='double', min=0, max=1, k=True, proxy = f'{self.side}_IK_ankle_{CONTROL}.IK_FK_Switch')

        #parentConstraints
        for jnt in [self.hipJnt, self.kneeJnt, self.ankleJnt, self.footJnt, self.ballJnt, self.toeJnt]:
            pc = cmds.parentConstraint(jnt.replace(JOINT, 'IK_' + JOINT), jnt.replace(JOINT, 'FK_' + JOINT), jnt, mo=True)
            FK_jnt = jnt.replace(JOINT, 'FK_' + JOINT)
            cmds.connectAttr(f'{self.side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{pc[0]}.{FK_jnt}W1')

            rev = cmds.createNode('reverse', n = f'{jnt}_IKFK_reverse')
            cmds.connectAttr(f'{self.side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
            IK_jnt = jnt.replace(JOINT, 'IK_' + JOINT)
            cmds.connectAttr(f'{rev}.outputX', f'{pc[0]}.{IK_jnt}W0')
        
        #visibility
        rev = cmds.createNode('reverse')
        cmds.connectAttr(f'{self.side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_IK_ankle_{CONTROL}.visibility')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_leg_pv_{CONTROL}.visibility')

        cmds.connectAttr(f'{self.side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{self.hipJnt.replace(JOINT, "FK_" + CONTROL)}.visibility')

    def leg(self):
        self.ik_leg()
        self.fk_leg()
        self.IKFK_switch()

