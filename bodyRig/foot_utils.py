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

rev_foot_joints('L_ankle_JNT','L_ball_JNT','L_toe_JNT',LEFT)


def rev_foot_IK(kneeJnt, ankleJnt, ballJnt, toeJnt, side):

    ankle_IK = cmds.ikHandle(n=f'{side}_ankle_IK', sj=kneeJnt.replace(JOINT, f'IK_{JOINT}'),
                             ee=ankleJnt.replace(JOINT, f'IK_{JOINT}'), sol='ikSCsolver')[0]

    ball_IK = cmds.ikHandle(n=f'{side}_ball_IK', sj=ankleJnt.replace(JOINT, f'IK_{JOINT}'),
                             ee=toeJnt.replace(JOINT, f'IK_{JOINT}'), sol='ikSCsolver')[0]

    leg_IK = f'{side}_{LEG}_IK'

    cmds.parent(ankle_IK, f'{side}_ankle_{REVERSE}_{JOINT}')
    cmds.parent(ball_IK, f'{side}_ball_{REVERSE}_{JOINT}')
    cmds.parent(leg_IK, f'{side}_ball_{REVERSE}_{JOINT}')






















