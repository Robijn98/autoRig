import sys
import maya.cmds as cmds

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from poleVector import find_poleVector

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import create_tempCtrl


GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'
ARM = 'arm'

#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'


def ik_arm(shoulderJnt, elbowJnt, wristJnt, side):
    cmds.select(d=True)

    #duplicate chain
    for  jnt in [shoulderJnt, elbowJnt, wristJnt]:
        mat = cmds.xform(jnt, q=True, m=True, ws=True)
        dupl_jnt = cmds.joint(n = jnt.replace(JOINT, f'IK_{JOINT}'))
        cmds.xform(dupl_jnt, m=mat, ws=True)
        cmds.makeIdentity(dupl_jnt, apply=True, r=True)



    #IK and polevector creation
    arm_ik = cmds.ikHandle(sj = shoulderJnt.replace(JOINT, f'IK_{JOINT}'), ee= wristJnt.replace(JOINT, f'IK_{JOINT}'), sol = 'ikRPsolver', n = f'{side}_{ARM}_IK')

    pv = cmds.spaceLocator(n = f'{side}_arm_polevector')
    pv_t = find_poleVector(shoulderJnt, elbowJnt, wristJnt)
    print(pv_t)
    cmds.xform(pv, t=pv_t)
    cmds.poleVectorConstraint(pv, arm_ik[0])

    #temp control creation
    IK_grp, IK_ctrl = create_tempCtrl(f'{side}_IK_wrist_{CONTROL}', lock=['sx', 'sy', 'sz'])
    mat = cmds.xform(wristJnt, q=True, m=True, ws=True)
    cmds.xform(IK_grp, m=mat, ws=True)
    if side == LEFT:
        cmds.setAttr(f'{IK_grp}.rotateY', 0)
        cmds.setAttr(f'{IK_grp}.rotateX', 90)
        cmds.setAttr(f'{IK_grp}.rotateZ', 0)
    else:
        cmds.setAttr(f'{IK_grp}.rotateY', 0)
        cmds.setAttr(f'{IK_grp}.rotateX', -90)
        cmds.setAttr(f'{IK_grp}.rotateZ', 0)
    cmds.parent(arm_ik[0], IK_ctrl)

    PV_grp, PV_ctrl = create_tempCtrl(f'{side}_arm_pv_{CONTROL}', lock=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'])
    mat = cmds.xform(pv, q=True, m=True, ws=True)
    cmds.xform(PV_grp, m=mat, ws=True)

    cmds.parent(pv, PV_ctrl)
    cmds.hide(pv)

def fk_arm(shoulderJnt, elbowJnt, wristJnt, side):
    cmds.select(d=True)

    original_chain = [shoulderJnt, elbowJnt, wristJnt]
    #duplicate chain
    for jnt in original_chain:
        mat = cmds.xform(jnt, q=True, m=True, ws=True)
        dupl_jnt = cmds.joint(n = jnt.replace(JOINT, f'FK_{JOINT}'))
        cmds.xform(dupl_jnt, m=mat, ws=True)
        cmds.makeIdentity(dupl_jnt, apply=True, r=True)

    #ctrl creation
    for num, jnt in enumerate(original_chain):
        FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
        FK_grp, FK_ctrl = create_tempCtrl(FK_jnt.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

        mat = cmds.xform(jnt, q=True, m=True, ws=True)
        cmds.xform(FK_grp, m=mat, ws=True)

        cmds.parentConstraint(FK_ctrl, FK_jnt, mo=True)


        if jnt != shoulderJnt:
            prev_jnt = original_chain[num-1]
            prev_jnt  = prev_jnt.replace(JOINT, f'FK_{JOINT}')
            prev_ctrl = prev_jnt.replace(JOINT, CONTROL)
            cmds.parent(FK_grp, prev_ctrl)

def IKFK_switch(shoulderJnt, elbowJnt, wristJnt, side):
    #create and link attributes
    cmds.addAttr(f'{side}_IK_wrist_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True)
    cmds.addAttr(f'{side}_arm_pv_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True, proxy=f'{side}_IK_wrist_{CONTROL}.IK_FK_Switch')

    for jnt in [shoulderJnt, elbowJnt, wristJnt]:
        FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
        FK_ctrl =FK_jnt.replace(JOINT, CONTROL)
        cmds.addAttr(FK_ctrl, ln='IK_FK_Switch', at='double', min=0, max=1, k=True, proxy = f'{side}_IK_wrist_{CONTROL}.IK_FK_Switch')

    #parentConstraints
    for jnt in [shoulderJnt, elbowJnt, wristJnt]:
        pc = cmds.parentConstraint(jnt.replace(JOINT, f'IK_{JOINT}'), jnt.replace(JOINT, f'FK_{JOINT}'), jnt, mo=True)
        FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
        cmds.connectAttr(f'{side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{pc[0]}.{FK_jnt}W1')

        rev = cmds.createNode('reverse', n = f'{jnt}_IKFK_reverse')
        cmds.connectAttr(f'{side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
        IK_jnt = jnt.replace(JOINT, f'IK_{JOINT}')
        cmds.connectAttr(f'{rev}.outputX', f'{pc[0]}.{IK_jnt}W0')

    #visibility
    rev = cmds.createNode('reverse')
    cmds.connectAttr(f'{side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
    cmds.connectAttr(f'{rev}.outputX', f'{side}_IK_wrist_{CONTROL}.visibility')
    cmds.connectAttr(f'{rev}.outputX', f'{side}_arm_pv_{CONTROL}.visibility')

    cmds.connectAttr(f'{side}_IK_wrist_{CONTROL}.IK_FK_Switch', f'{shoulderJnt.replace(JOINT, "FK_" + CONTROL)}.visibility')


def clav_control(clavJnt, side):
    clav_grp, clav_ctrl = create_tempCtrl(clavJnt.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])
    mat = cmds.xform(clavJnt, q=True, m=True, ws=True)
    cmds.xform(clav_grp, m=mat, ws=True)

    cmds.parentConstraint(clav_ctrl, clavJnt)


def IKFK_arm(shoulderJnt, elbowJnt, wristJnt, clavJnt, side, clav =True):
    ik_arm(shoulderJnt, elbowJnt, wristJnt, side)
    fk_arm(shoulderJnt, elbowJnt, wristJnt, side)
    IKFK_switch(shoulderJnt, elbowJnt, wristJnt, side)
    if clav == True:
        clav_control(clavJnt, side)

#EXECUTE
#IKFK_arm('L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT', 'L_clavicle_JNT', LEFT)


