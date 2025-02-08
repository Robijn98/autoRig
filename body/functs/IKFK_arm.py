import maya.cmds as cmds
from poleVector import find_poleVector
from general_functions import create_tempCtrl

class IKFK_arm:
    
    GROUP = 'GRP'
    CONTROL = 'CTRL'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    ARM = 'arm'

    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'

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
            dupl_jnt = cmds.joint(n=jnt.replace(self.JOINT, f'{prefix}_{self.JOINT}'))
            cmds.xform(dupl_jnt, m=mat, ws=True)
            cmds.makeIdentity(dupl_jnt, apply=True, r=True)
            duplicated_joints.append(dupl_jnt)
        
        return duplicated_joints


    def ik_arm(self):
        self.duplicate_chain('IK')
        arm_ik = cmds.ikHandle(sj = self.shoulderJnt.replace(self.JOINT, 'IK_' + self.JOINT), 
                                ee= self.wristJnt.replace(self.JOINT, 'IK_' + self.JOINT), 
                                sol = 'ikRPsolver', n = f'{self.side}_{self.ARM}_IK')

        pv = cmds.spaceLocator(n = f'{self.side}_arm_polevector')
        pv_t = find_poleVector(self.shoulderJnt, self.elbowJnt, self.wristJnt)
        cmds.xform(pv, t=pv_t)
        cmds.poleVectorConstraint(pv, arm_ik[0])

        #temp control creation
        IK_grp, IK_ctrl = create_tempCtrl(f'{self.side}_IK_wrist_{self.CONTROL}', lock=['sx', 'sy', 'sz'])
        mat = cmds.xform(self.wristJnt, q=True, m=True, ws=True) 
        cmds.xform(IK_grp, m=mat, ws=True)
        if self.side == self.LEFT:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', 90)
            cmds.setAttr(f'{IK_grp}.rotateZ', 0)
        else:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', -90)
            cmds.setAttr(f'{IK_grp}.rotateZ', 0)
        
        cmds.parent(arm_ik[0], IK_ctrl)
        PV_grp, PV_ctrl = create_tempCtrl(f'{self.side}_arm_pv_{self.CONTROL}', lock=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'])
        mat = cmds.xform(pv, q=True, m=True, ws=True)
        cmds.xform(PV_grp, m=mat, ws=True)
        cmds.parent(pv, PV_ctrl)
        cmds.hide(pv)


    def fk_arm(self):
        self.duplicate_chain('FK')
        for num, jnt in enumerate([self.shoulderJnt, self.elbowJnt, self.wristJnt]):
            FK_jnt = jnt.replace(self.JOINT, f'FK_{self.JOINT}')
            FK_grp, FK_ctrl = create_tempCtrl(FK_jnt.replace(self.JOINT, self.CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            cmds.xform(FK_grp, m=mat, ws=True)

            cmds.parentConstraint(FK_ctrl, FK_jnt, mo=True)

            if jnt != self.shoulderJnt:
                prev_jnt = [self.shoulderJnt, self.elbowJnt][num-1]
                prev_jnt  = prev_jnt.replace(self.JOINT, f'FK_{self.JOINT}')
                prev_ctrl = prev_jnt.replace(self.JOINT, self.CONTROL)
                cmds.parent(FK_grp, prev_ctrl)


    def IKFK_switch(self):
        cmds.addAttr(f'{self.side}_IK_wrist_{self.CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True)
        cmds.addAttr(f'{self.side}_arm_pv_{self.CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True, proxy=f'{self.side}_IK_wrist_{self.CONTROL}.IK_FK_Switch')

        for jnt in [self.shoulderJnt, self.elbowJnt, self.wristJnt]:
            FK_jnt = jnt.replace(self.JOINT, f'FK_{self.JOINT}')
            FK_ctrl =FK_jnt.replace(self.JOINT, self.CONTROL)
            cmds.addAttr(FK_ctrl, ln='IK_FK_Switch', at='double', min=0, max=1, k=True, proxy = f'{self.side}_IK_wrist_{self.CONTROL}.IK_FK_Switch')

        for jnt in [self.shoulderJnt, self.elbowJnt, self.wristJnt]:
            pc = cmds.parentConstraint(jnt.replace(self.JOINT, f'IK_{self.JOINT}'), jnt.replace(self.JOINT, f'FK_{self.JOINT}'), jnt, mo=True)
            FK_jnt = jnt.replace(self.JOINT, f'FK_{self.JOINT}')
            cmds.connectAttr(f'{self.side}_IK_wrist_{self.CONTROL}.IK_FK_Switch', f'{pc[0]}.{FK_jnt}W1')

            rev = cmds.createNode('reverse', n = f'{jnt}_IKFK_reverse')
            cmds.connectAttr(f'{self.side}_IK_wrist_{self.CONTROL}.IK_FK_Switch', f'{rev}.inputX')
            IK_jnt = jnt.replace(self.JOINT, f'IK_{self.JOINT}')
            cmds.connectAttr(f'{rev}.outputX', f'{pc[0]}.{IK_jnt}W0')

        rev = cmds.createNode('reverse')
        cmds.connectAttr(f'{self.side}_IK_wrist_{self.CONTROL}.IK_FK_Switch', f'{rev}.inputX')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_IK_wrist_{self.CONTROL}.visibility')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_arm_pv_{self.CONTROL}.visibility')

        cmds.connectAttr(f'{self.side}_IK_wrist_{self.CONTROL}.IK_FK_Switch', f'{self.shoulderJnt.replace(self.JOINT, "FK_" + self.CONTROL)}.visibility')



    def clav_control(self):
        clav_grp, clav_ctrl = create_tempCtrl(self.clavJnt.replace(self.JOINT, self.CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])
        mat = cmds.xform(self.clavJnt, q=True, m=True, ws=True)
        cmds.xform(clav_grp, m=mat, ws=True)

        cmds.parentConstraint(clav_ctrl, self.clavJnt)

    def IKFK_arm(self):
        self.ik_arm()
        self.fk_arm()
        self.IKFK_switch()
        if self.clav == True:
            self.clav_control()

# arm = IKFK_arm('L_arm_shoulder_JNT', 'L_arm_elbow_JNT', 'L_arm_wrist_JNT', 'L_clavicle_JNT', 'L')


