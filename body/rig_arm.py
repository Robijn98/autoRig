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

class IKFK_arm:

    def __init__(self, shoulderJnt, elbowJnt, wristJnt, clavJnt, side, clav = True):
        self.shoulderJnt = shoulderJnt
        self.elbowJnt = elbowJnt
        self.wristJnt = wristJnt
        self.clavJnt = clavJnt
        self.side = side
        self.clav = clav


    def duplicate_chain(self, prefix):
        cmds.select(d=True)
        duplicated_joints = []
        for jnt in [self.shoulderJnt, self.elbowJnt, self.wristJnt]:
            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            dupl_jnt = cmds.joint(n=jnt.replace(JOINT, f'{prefix}_{JOINT}'))
            cmds.xform(dupl_jnt, m=mat, ws=True)
            cmds.makeIdentity(dupl_jnt, apply=True, r=True)
            duplicated_joints.append(dupl_jnt)
        
        return duplicated_joints


    def ik_arm(self):
        self.duplicate_chain('IK')
        arm_ik = cmds.ikHandle(sj = self.shoulderJnt.replace(JOINT, 'IK_' + JOINT), 
                                ee= self.wristJnt.replace(JOINT, 'IK_' + JOINT), 
                                sol = 'ikRPsolver', n = f'{self.side}_{ARM}_IK')

        pv = cmds.spaceLocator(n = f'{self.side}_arm_polevector')
        arm_poleVec = poleVector(self.shoulderJnt, self.elbowJnt, self.wristJnt)
        pv_t = arm_poleVec.find_polevector()
        cmds.xform(pv, t=pv_t)
        cmds.poleVectorConstraint(pv, arm_ik[0])

        #temp control creation
        IK_grp, IK_ctrl = controller.create_temp_ctrl(f'{self.side}_IK_wrist_{CONTROL}', lock=['sx', 'sy', 'sz'])
        mat = cmds.xform(self.wristJnt, q=True, m=True, ws=True) 
        cmds.xform(IK_grp, m=mat, ws=True)
        if self.side == LEFT:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', 90)
            cmds.setAttr(f'{IK_grp}.rotateZ', 0)
        else:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', -90)
            cmds.setAttr(f'{IK_grp}.rotateZ', 0)
        
        cmds.parent(arm_ik[0], IK_ctrl)
        PV_grp, PV_ctrl = controller.create_temp_ctrl(f'{self.side}_arm_pv_{CONTROL}', lock=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'])
        mat = cmds.xform(pv, q=True, m=True, ws=True)
        cmds.xform(PV_grp, m=mat, ws=True)
        cmds.parent(pv, PV_ctrl)
        cmds.hide(pv)


    def fk_arm(self):
        self.duplicate_chain('FK')
        for num, jnt in enumerate([self.shoulderJnt, self.elbowJnt, self.wristJnt]):
            FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
            FK_grp, FK_ctrl = controller.create_temp_ctrl(FK_jnt.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            cmds.xform(FK_grp, m=mat, ws=True)

            cmds.parentConstraint(FK_ctrl, FK_jnt, mo=True)

            if jnt != self.shoulderJnt:
                prev_jnt = [self.shoulderJnt, self.elbowJnt][num-1]
                prev_jnt  = prev_jnt.replace(JOINT, f'FK_{JOINT}')
                prev_ctrl = prev_jnt.replace(JOINT, CONTROL)
                cmds.parent(FK_grp, prev_ctrl)


    def IKFK_switch(self):
        cmds.addAttr(f'{self.side}_IK_wrist_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True)
        cmds.addAttr(f'{self.side}_arm_pv_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True, proxy=f'{self.side}_IK_wrist_{CONTROL}.IK_FK_Switch')

        for jnt in [self.shoulderJnt, self.elbowJnt, self.wristJnt]:
            FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
            FK_ctrl =FK_jnt.replace(JOINT, CONTROL)
            cmds.addAttr(FK_ctrl, ln='IK_FK_Switch', at='double', min=0, max=1, k=True, proxy = f'{self.side}_IK_wrist_{CONTROL}.IK_FK_Switch')

        for jnt in [self.shoulderJnt, self.elbowJnt, self.wristJnt]:
            pc = cmds.parentConstraint(jnt.replace(JOINT, f'IK_{JOINT}'), jnt.replace(JOINT, f'FK_{JOINT}'), jnt, mo=True)
            FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
            cmds.connectAttr(f'{self.side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{pc[0]}.{FK_jnt}W1')

            rev = cmds.createNode('reverse', n = f'{jnt}_IKFK_reverse')
            cmds.connectAttr(f'{self.side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
            IK_jnt = jnt.replace(JOINT, f'IK_{JOINT}')
            cmds.connectAttr(f'{rev}.outputX', f'{pc[0]}.{IK_jnt}W0')

        rev = cmds.createNode('reverse')
        cmds.connectAttr(f'{self.side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_IK_wrist_{CONTROL}.visibility')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_arm_pv_{CONTROL}.visibility')

        cmds.connectAttr(f'{self.side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{self.shoulderJnt.replace(JOINT, "FK_" + CONTROL)}.visibility')



    def clav_control(self):
        clav_grp, clav_ctrl = controller.create_temp_ctrl(self.clavJnt.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])
        mat = cmds.xform(self.clavJnt, q=True, m=True, ws=True)
        cmds.xform(clav_grp, m=mat, ws=True)

        cmds.parentConstraint(clav_ctrl, self.clavJnt)

    def arm(self):
        self.ik_arm()
        self.fk_arm()
        self.IKFK_switch()
        if self.clav == True:
            self.clav_control()

# arm = IKFK_arm('L_arm_shoulder_JNT', 'L_arm_elbow_JNT', 'L_arm_wrist_JNT', 'L_clavicle_JNT', 'L')


