import sys
import maya.cmds as cmds

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import create_tempCtrl
from general_functions import addOffset


GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'
FOOT = 'foot'
REVERSE = 'rev'

#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'

import sys
import maya.cmds as cmds

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



#create guides function


def rev_foot_joints(ankleJnt, ballJnt, toeJnt, side):
    if f'{side}_innerBank_guide':
        cmds.select(cl=True)
        innerbank_jnt = cmds.joint(name=f'{side}_innerbank_{REVERSE}_{JOINT}')
        mat = cmds.xform(f'{side}_innerBank_guide', q=True, m=True, ws=True)
        cmds.xform(innerbank_jnt, m=mat, ws=True)
    else:
        raise ValueError('no innerbank guide')

    if f'{side}_outerBank_guide':
        cmds.select(cl=True)
        outerbank_jnt = cmds.joint(name=f'{side}_outerbank_{REVERSE}_{JOINT}')
        mat = cmds.xform(f'{side}_outerBank_guide', q=True, m=True, ws=True)
        cmds.xform(outerbank_jnt, m=mat, ws=True)
    else:
        raise ValueError('no outerbank guide')

    if f'{side}_heel_guide':
        cmds.select(cl=True)
        heel_jnt = cmds.joint(name=f'{side}_heel_{REVERSE}_{JOINT}')
        mat = cmds.xform(f'{side}_heel_guide', q=True, m=True, ws=True)
        cmds.xform(heel_jnt, m=mat, ws=True)
    else:
        raise ValueError('no heel guide')

    cmds.select(cl=True)
    pivot_jnt = cmds.joint(name=f'{side}_pivot_{REVERSE}_{JOINT}')
    mat = cmds.xform(ballJnt, q=True, m=True, ws=True)
    cmds.xform(pivot_jnt, m=mat, ws=True)

    cmds.select(cl=True)
    toe_jnt = cmds.joint(name=f'{side}_toe_{REVERSE}_{JOINT}')
    mat = cmds.xform(toeJnt, q=True, m=True, ws=True)
    cmds.xform(toe_jnt, m=mat, ws=True)

    cmds.select(cl=True)
    ball_jnt = cmds.joint(name=f'{side}_ball_{REVERSE}_{JOINT}')
    mat = cmds.xform(ballJnt, q=True, m=True, ws=True)
    cmds.xform(ball_jnt, m=mat, ws=True)

    cmds.select(cl=True)
    ankle_jnt = cmds.joint(name=f'{side}_ankle_{REVERSE}_{JOINT}')
    mat = cmds.xform(ankleJnt, q=True, m=True, ws=True)
    cmds.xform(ankle_jnt, m=mat, ws=True)

    #parenting in right order
    cmds.parent(ankle_jnt, ball_jnt)
    cmds.parent(ball_jnt, toe_jnt)
    cmds.parent(toe_jnt, pivot_jnt)
    cmds.parent(pivot_jnt, heel_jnt)
    cmds.parent(heel_jnt, outerbank_jnt)
    cmds.parent(outerbank_jnt, innerbank_jnt)

    cmds.makeIdentity(innerbank_jnt, apply=True, t=1, r=1, s=1, n=0, pn=1)



def rev_foot_IK(kneeJnt, ankleJnt, ballJnt, toeJnt, side):

    ball_IK = cmds.ikHandle(n=f'{side}_ankle_IK', sj=ankleJnt.replace(JOINT, f'IK_{JOINT}'),
                             ee=ballJnt.replace(JOINT, f'IK_{JOINT}'), sol='ikSCsolver')[0]

    toe_IK = cmds.ikHandle(n=f'{side}_ball_IK', sj=ballJnt.replace(JOINT, f'IK_{JOINT}'),
                             ee=toeJnt.replace(JOINT, f'IK_{JOINT}'), sol='ikSCsolver')[0]

    leg_IK = f'{side}_{LEG}_IK'

    cmds.parent(toe_IK, f'{side}_toe_{REVERSE}_{JOINT}')
    cmds.parent(ball_IK, f'{side}_ball_{REVERSE}_{JOINT}')
    cmds.parent(leg_IK, f'{side}_ball_{REVERSE}_{JOINT}')


def rev_foot_ctrl(kneeJnt, ankleJnt, ballJnt, toeJnt, controlLoc, side):

    rot_grp, rot_ctrl = create_tempCtrl(f'{side}_rev_{FOOT}_{CONTROL}', lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])
    ctrl_pos = cmds.xform(controlLoc, q=True, m=True, ws=True)
    cmds.xform(rot_grp, m=ctrl_pos, ws=True)

    #banking
    innerbank_jnt = f'{side}_innerbank_{REVERSE}_{JOINT}'
    outerbank_jnt = f'{side}_outerbank_{REVERSE}_{JOINT}'
    pivot_jnt = f'{side}_pivot_{REVERSE}_{JOINT}'
    ball_jnt = f'{side}_ball_{REVERSE}_{JOINT}'
    toe_jnt = f'{side}_toe_{REVERSE}_{JOINT}'
    heel_jnt = f'{side}_heel_{REVERSE}_{JOINT}'

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


def rev_foot(kneeJnt, ankleJnt, ballJnt, toeJnt, controlLoc, side):
    rev_foot_joints(ankleJnt, ballJnt, toeJnt, side)
    rev_foot_IK(kneeJnt, ankleJnt, ballJnt, toeJnt, side)
    rev_foot_ctrl(kneeJnt, ankleJnt, ballJnt, toeJnt, controlLoc, side)


'''#execute
rev_foot_joints('_ankle_JNT','L_ball_JNT','L_toe_JNT',LEFT)
rev_foot_IK('L_knee_JNT','L_ankle_JNT','L_ball_JNT','L_toe_JNT',LEFT)
rev_foot_ctrl('L_knee_JNT','L_ankle_JNT','L_ball_JNT','L_toe_JNT','L_rev_CTRL_guide',LEFT)
'''















