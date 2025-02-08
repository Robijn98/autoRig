import maya.cmds as cmds
from poleVector import find_poleVector
from general_functions import create_tempCtrl

class IKFK_leg:
    
    GROUP = 'GRP'
    CONTROL = 'CTRL'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    ARM = 'arm'

    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'

    def __init__(self, hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt, side):
        self.hipJnt = hipJnt
        self.kneeJnt = kneeJnt
        self.ankleJnt = ankleJnt
        self.ballJnt = ballJnt
        self.toeJnt = toeJnt
        self.side = side


    def duplicate_chain(self, prefix):
        cmds.select(d=True)
        duplicated_joints = []
        for jnt in [self.hipJnt, self.kneeJnt, self.ankleJnt, self.ballJnt, self.toeJnt]:
            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            dupl_jnt = cmds.joint(n=jnt.replace(self.JOINT, f'{prefix}_{self.JOINT}'))
            cmds.xform(dupl_jnt, m=mat, ws=True)
            cmds.makeIdentity(dupl_jnt, apply=True, r=True)
            duplicated_joints.append(dupl_jnt)
        
        return duplicated_joints

    def ik_leg(self):
        self.duplicate_chain('IK')
        leg_ik = cmds.ikHandle(sj = self.hipJnt.replace(self.JOINT, 'IK_' + self.JOINT), 
                                ee= self.ankleJnt.replace(self.JOINT, 'IK_' + self.JOINT), 
                                sol = 'ikRPsolver', n = f'{self.side}_{self.LEG}_IK')

        pv = cmds.spaceLocator(n = f'{self.side}_{self.LEG}_polevector')
        pv_t = find_poleVector(self.hipJnt, self.kneeJnt, self.ankleJnt)
        cmds.xform(pv, t=pv_t)
        cmds.poleVectorConstraint(pv, leg_ik[0])

        #temp control creation
        IK_grp, IK_ctrl = create_tempCtrl(f'{self.side}_IK_ankle_{self.CONTROL}', lock=['sx', 'sy', 'sz'])
        mat = cmds.xform(self.ankleJnt, q=True, m=True, ws=True) 
        cmds.xform(IK_grp, m=mat, ws=True)
        if self.side == self.LEFT:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', 90)
            cmds.setAttr(f'{IK_grp}.rotateZ', 0)
        else:
            cmds.setAttr(f'{IK_grp}.rotateY', 0)
            cmds.setAttr(f'{IK_grp}.rotateX', -90)
        cmds.parent(leg_ik[0], IK_ctrl)
        cmds.parent(pv, IK_ctrl)
        cmds.hide(pv)


    def fk_leg(hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt, side):
        self.duplicate_chain('FK')
        for num, jnt in enumerate([self.hipJnt, self.kneeJnt, self.ankleJnt, self.ballJnt, self.toeJnt]):
            FK_jnt = jnt.replace(self.JOINT, f'FK_{self.JOINT}')
            FK_grp, FK_ctrl = create_tempCtrl(FK_jnt.replace(self.JOINT, self.CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            cmds.xform(FK_grp, m=mat, ws=True)

            cmds.parentConstraint(FK_ctrl, FK_jnt, mo=True)

            if jnt != self.hipJnt:
                prev_jnt = self.hipJnt[num-1]
                prev_jnt  = prev_jnt.replace(self.JOINT, f'FK_{self.JOINT}')
                prev_ctrl = prev_jnt.replace(self.JOINT, self.CONTROL)
                cmds.parent(FK_grp, prev_ctrl)

    def IKFK_switch(self):
        cmds.addAttr(f'{self.side}_IK_ankle_{self.CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True)
        cmds.addAttr(f'{self.side}_leg_pv_{self.CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True, proxy=f'{self.side}_IK_ankle_{self.CONTROL}.IK_FK_Switch')

        for jnt in [self.hipJnt, self.kneeJnt, self.ankleJnt, self.ballJnt, self.toeJnt]:
            FK_jnt = jnt.replace(self.JOINT, f'FK_{self.JOINT}')
            FK_ctrl = FK_jnt.replace(self.JOINT, self.CONTROL)
            cmds.addAttr(FK_ctrl, ln='IK_FK_Switch', at='double', min=0, max=1, k=True, proxy = f'{self.side}_IK_ankle_{self.CONTROL}.IK_FK_Switch')

        #parentConstraints
        for jnt in [self.hipJnt, self.kneeJnt, self.ankleJnt, self.ballJnt, self.toeJnt]:
            pc = cmds.parentConstraint(jnt.replace(self.JOINT, 'IK_' + self.JOINT), jnt.replace(self.JOINT, 'FK_' + self.JOINT), jnt, mo=True)
            FK_jnt = jnt.replace(self.JOINT, 'FK_' + self.JOINT)
            cmds.connectAttr(f'{self.side}_IK_ankle_{self.CONTROL}.IK_FK_Switch', f'{pc[0]}.{FK_jnt}W1')

            rev = cmds.createNode('reverse', n = f'{jnt}_IKFK_reverse')
            cmds.connectAttr(f'{self.side}_IK_ankle_{self.CONTROL}.IK_FK_Switch', f'{rev}.inputX')
            IK_jnt = jnt.replace(self.JOINT, 'IK_' + self.JOINT)
            cmds.connectAttr(f'{rev}.outputX', f'{pc[0]}.{IK_jnt}W0')
        
        #visibility
        rev = cmds.createNode('reverse')
        cmds.connectAttr(f'{self.side}_IK_ankle_{self.CONTROL}.IK_FK_Switch', f'{rev}.inputX')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_IK_ankle_{self.CONTROL}.visibility')
        cmds.connectAttr(f'{rev}.outputX', f'{self.side}_leg_pv_{self.CONTROL}.visibility')

        cmds.connectAttr(f'{self.side}_IK_ankle_{self.CONTROL}.IK_FK_Switch', f'{self.hipJnt.replace(self.JOINT, "FK_" + self.CONTROL)}.visibility')

    def IKFK_leg(self):
        self.ik_leg()
        self.fk_leg()
        self.IKFK_switch()

# leg = IKFK_leg('L_leg_hip_JNT', 'L_leg_knee_JNT', 'L_leg_ankle_JNT', 'L_leg_ball_JNT', 'L_leg_toe_JNT', 'L')