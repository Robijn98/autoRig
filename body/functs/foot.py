import sys
import maya.cmds as cmds
from general_functions import create_tempCtrl
from general_functions import addOffset

class foot:
   
    GROUP = 'GRP'
    CONTROL = 'CTRL'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    FOOT = 'foot'
    REVERSE = 'rev'
    LEG = 'leg'

    # side constants
    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'

    def __init__(self, ankleJnt, ballJnt, toeJnt, side):
        self.ankleJnt = ankleJnt
        self.ballJnt = ballJnt
        self.toeJnt = toeJnt
        self.side = side


    def rev_foot_joints(self):
        # create reverse foot joints
        for guide in [f'{self.side}_innerBank_guide', f'{self.side}_outerBank_guide', f'{self.side}_heel_guide']:
            if cmds.objExists(guide):
                cmds.select(cl=True)
                jnt = cmds.joint(name=f'{guide.replace(self.GUIDE, self.JOINT)}')
                mat = cmds.xform(guide, q=True, m=True, ws=True)
                cmds.xform(jnt, m=mat, ws=True)
            else:
                raise ValueError(f'no {guide} guide')
        
        cmds.select(cl=True)

        for jnt in [self.ankleJnt, self.ballJnt, self.toeJnt]:
            if cmds.objExists(jnt):
                cmds.select(cl=True)
                jnt = cmds.joint(name=f'{jnt.replace(self.JOINT, f'{self.REVERSE}_{self.JOINT}')}')
                mat = cmds.xform(jnt, q=True, m=True, ws=True)
                cmds.xform(jnt, m=mat, ws=True)
            else:
                raise ValueError(f'no {jnt} joint')
        
        cmds.select(cl=True)
        pivot_jnt = cmds.joint(name=f'{self.side}_pivot_{self.REVERSE}_{self.JOINT}')
        mat = cmds.xform(self.ballJnt, q=True, m=True, ws=True)
        cmds.xform(pivot_jnt, m=mat, ws=True)

        # parenting in right order
        cmds.parent(self.ankleJnt, self.ballJnt)
        cmds.parent(self.ballJnt, self.toeJnt)
        cmds.parent(self.toeJnt, pivot_jnt)
        cmds.parent(pivot_jnt, self.ankleJnt)
        cmds.parent(self.ankleJnt, f'{self.side}_innerBank_{self.REVERSE}_{self.JOINT}')
        cmds.parent(f'{self.side}_innerBank_{self.REVERSE}_{self.JOINT}', f'{self.side}_outerBank_{self.REVERSE}_{self.JOINT}')

        cmds.makeIdentity(f'{self.side}_innerBank_{self.REVERSE}_{self.JOINT}', apply=True, t=1, r=1, s=1, n=0, pn=1)



    def rev_foot_IK(self):
        # create IK handles
        ball_IK = cmds.ikHandle(n=f'{self.side}_ankle_IK', sj=self.ankleJnt.replace(self.JOINT, f'IK_{self.JOINT}'),
                                ee=self.ballJnt.replace(self.JOINT, f'IK_{self.JOINT}'), sol='ikSCsolver')[0]

        toe_IK = cmds.ikHandle(n=f'{self.side}_ball_IK', sj=self.ballJnt.replace(self.JOINT, f'IK_{self.JOINT}'),
                                ee=self.toeJnt.replace(self.JOINT, f'IK_{self.JOINT}'), sol='ikSCsolver')[0]

        leg_IK = f'{self.side}_{self.LEG}_IK'

        cmds.parent(toe_IK, f'{self.side}_toe_{self.REVERSE}_{self.JOINT}')
        cmds.parent(ball_IK, f'{self.side}_ball_{self.REVERSE}_{self.JOINT}')
        cmds.parent(leg_IK, f'{self.side}_ball_{self.REVERSE}_{self.JOINT}')
        

    def rev_foot_ctrl(self, controlLoc):
        rot_grp, rot_ctrl = create_tempCtrl(f'{self.side}_rev_{self.FOOT}_{self.CONTROL}', lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])
        ctrl_pos = cmds.xform(controlLoc, q=True, m=True, ws=True)
        cmds.xform(rot_grp, m=ctrl_pos, ws=True)

        #banking
        innerbank_jnt = f'{self.side}_innerbank_{self.REVERSE}_{self.JOINT}'
        outerbank_jnt = f'{self.side}_outerbank_{self.REVERSE}_{self.JOINT}'
        pivot_jnt = f'{self.side}_pivot_{self.REVERSE}_{self.JOINT}'
        ball_jnt = f'{self.side}_ball_{self.REVERSE}_{self.JOINT}'
        toe_jnt = f'{self.side}_toe_{self.REVERSE}_{self.JOINT}'
        heel_jnt = f'{self.side}_heel_{self.REVERSE}_{self.JOINT}'

        #innerbank
        cond = cmds.createNode('condition')
        cmds.connectAttr(f'{rot_ctrl}.rotateZ', f'{cond}.colorIfTrueR')
        cmds.connectAttr(f'{rot_ctrl}.rotateZ', f'{cond}.firstTerm')

        cmds.connectAttr(f'{cond}.outColorR', f'{innerbank_jnt}.rotateZ')
        cmds.setAttr(f'{cond}.colorIfFalseR', 0)
        cmds.setAttr(f'{cond}.operation', 2)

        #outerbank
        cmds.connectAttr(f'{rot_ctrl}.rotateZ', f'{cond}.colorIfFalseG')
        cmds.connectAttr(f'{cond}.outColorG', f'{outerbank_jnt}.rotateZ')

        #pivot
        cmds.connectAttr(f'{rot_ctrl}.rotateY', f'{pivot_jnt}.rotateY')

        #heel
        cond = cmds.createNode('condition')
        cmds.connectAttr(f'{rot_ctrl}.rotateX', f'{cond}.colorIfTrueR')
        cmds.connectAttr(f'{rot_ctrl}.rotateX', f'{cond}.firstTerm')
        
        cmds.connectAttr(f'{cond}.outColorR', f'{heel_jnt}.rotateX')
        cmds.setAttr(f'{cond}.colorIfFalseR', 0)
        cmds.setAttr(f'{cond}.operation', 4)

        #ball
        cmds.addAttr(rot_ctrl, ln='weight', at='double', min=0, max=1, k=True)

        cond = cmds.createNode('condition')
        cmds.setAttr(f'{cond}.operation', 4)
        cmds.connectAttr(f'{rot_ctrl}.rotateX', f'{cond}.colorIfTrueR')
        cmds.connectAttr(f'{rot_ctrl}.rotateX', f'{cond}.firstTerm')

        cmds.connectAttr(f'{rot_ctrl}.rotateX', f'{cond}.colorIfFalseG')

        blend = cmds.createNode('blendColors')
        cmds.connectAttr(f'{cond}.outColorG', f'{blend}.color1R')
        cmds.connectAttr(f'{cond}.outColorG', f'{blend}.color2G')

        cmds.connectAttr(f'{rot_ctrl}.weight', f'{blend}.blender')

        #this is for maya 2023, when switching to maya 2024, can be replaced with the simpler negate node
        multDiv = cmds.createNode('multiplyDivide')
        cmds.connectAttr(f'{blend}.outputR', f'{multDiv}.input1X')
        cmds.setAttr(f'{multDiv}.input2X', -1)
        cmds.connectAttr(f'{multDiv}.outputX', f'{ball_jnt}.rotateZ')

        multDiv = cmds.createNode('multiplyDivide')
        cmds.connectAttr(f'{blend}.outputG', f'{multDiv}.input1X')
        cmds.setAttr(f'{multDiv}.input2X', -1)
        cmds.connectAttr(f'{multDiv}.outputX', f'{toe_jnt}.rotateZ')

    def rev_foot(self, controlLoc):
        self.rev_foot_joints()
        self.rev_foot_IK()
        self.rev_foot_ctrl(controlLoc)


#execute
#foot('L_ankle_JNT', 'L_ball_JNT', 'L_toe_JNT', 'L').rev_foot('L_foot_ctrl_LOC')
#foot('R_ankle_JNT', 'R_ball_JNT', 'R_toe_JNT', 'R').rev_foot('R_foot_ctrl_LOC')














