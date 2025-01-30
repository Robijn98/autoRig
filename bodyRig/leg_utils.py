import maya.cmds as cmds
from poleVector import find_poleVector
from general_functions import create_tempCtrl

GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'
LEG = 'leg'

#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'



def ik_leg(hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt, side):
    cmds.select(d=True)

    #duplicate chain
    for  jnt in [hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt]:
        mat = cmds.xform(jnt, q=True, m=True, ws=True)
        dupl_jnt = cmds.joint(n = jnt.replace(JOINT, f'IK_{JOINT}'))
        cmds.xform(dupl_jnt, m=mat, ws=True)
        cmds.makeIdentity(dupl_jnt, apply=True, r=True)



    #IK and polevector creation
    leg_ik = cmds.ikHandle(sj = hipJnt.replace(JOINT, f'IK_{JOINT}'), ee= ankleJnt.replace(JOINT, f'IK_{JOINT}'), sol ='ikRPsolver', n =f'{side}_{LEG}_IK')

    pv = cmds.spaceLocator(n = f'{side}_{LEG}_polevector')
    pv_translate = find_poleVector(hipJnt, kneeJnt, ankleJnt)
    cmds.xform(pv, t=pv_translate)
    cmds.poleVectorConstraint(pv, leg_ik[0])

    #temp control creation
    IK_grp, IK_ctrl = create_tempCtrl(f'{side}_IK_ankle_{CONTROL}', lock=['sx', 'sy', 'sz'])
    mat = cmds.xform(ankleJnt, q=True, m=True, ws=True)
    cmds.xform(IK_grp, m=mat, ws=True)
    if side == LEFT:
        cmds.setAttr(f'{IK_grp}.rotateX', 0)
        cmds.setAttr(f'{IK_grp}.rotateY', -90)
        cmds.setAttr(f'{IK_grp}.rotateZ', 0)
    else:
        cmds.setAttr(f'{IK_grp}.rotateX', -90)
        cmds.setAttr(f'{IK_grp}.rotateY', 0)
        cmds.setAttr(f'{IK_grp}.rotateZ', 90)


    cmds.parent(leg_ik[0], IK_ctrl)

    PV_grp, PV_ctrl = create_tempCtrl(f'{side}_{LEG}_pv_{CONTROL}', lock=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'])
    mat = cmds.xform(pv, q=True, m=True, ws=True)
    cmds.xform(PV_grp, m=mat, ws=True)

    cmds.parent(pv, PV_ctrl)
    cmds.hide(pv)

def fk_leg(hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt, side):
    cmds.select(d=True)

    original_chain = [hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt]
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


        if jnt != hipJnt:
            prev_jnt = original_chain[num-1]
            prev_jnt  = prev_jnt.replace(JOINT, f'FK_{JOINT}')
            prev_ctrl = prev_jnt.replace(JOINT, CONTROL)
            cmds.parent(FK_grp, prev_ctrl)

def IKFK_switch(hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt, side):
    #create and link attributes
    cmds.addAttr(f'{side}_IK_ankle_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True)
    cmds.addAttr(f'{side}_leg_pv_{CONTROL}', ln='IK_FK_Switch',  at='double', min=0, max=1, k=True, proxy=f'{side}_IK_ankle_{CONTROL}.IK_FK_Switch')


    for jnt in [hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt]:
        FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
        FK_ctrl = FK_jnt.replace(JOINT, CONTROL)
        cmds.addAttr(FK_ctrl, ln='IK_FK_Switch', at='double', min=0, max=1, k=True, proxy = f'{side}_IK_ankle_{CONTROL}.IK_FK_Switch')

    #parentConstraints
    for jnt in [hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt]:
        pc = cmds.parentConstraint(jnt.replace(JOINT, f'IK_{JOINT}'), jnt.replace(JOINT, f'FK_{JOINT}'), jnt, mo=True)
        FK_jnt = jnt.replace(JOINT, f'FK_{JOINT}')
        cmds.connectAttr(f'{side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{pc[0]}.{FK_jnt}W1')

        rev = cmds.createNode('reverse', n = f'{jnt}_IKFK_reverse')
        cmds.connectAttr(f'{side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
        IK_jnt = jnt.replace(JOINT, f'IK_{JOINT}')
        cmds.connectAttr(f'{rev}.outputX', f'{pc[0]}.{IK_jnt}W0')

    #visibility
    rev = cmds.createNode('reverse')
    cmds.connectAttr(f'{side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{rev}.inputX')
    cmds.connectAttr(f'{rev}.outputX', f'{side}_IK_ankle_{CONTROL}.visibility')
    cmds.connectAttr(f'{rev}.outputX', f'{side}_leg_pv_{CONTROL}.visibility')

    cmds.connectAttr(f'{side}_IK_ankle_{CONTROL}.IK_FK_Switch', f'{hipJnt.replace(JOINT, "FK_" + CONTROL)}.visibility')



def leg_cleanup(hipJnt, kneeJnt, ankleJnt, ballJnt,  side):
    cmds.select(hipJnt)
    spineBase = cmds.pickWalk(d='up')[0]

    cmds.parent(hipJnt.replace(JOINT, f'FK_{JOINT}'), spineBase)
    cmds.parent(hipJnt.replace(JOINT, f'IK_{JOINT}'), 'skeleton_grp')

    # IK cleanup
    if cmds.objExists('pelvis_CTRL'):
        cmds.parentConstraint('pelvis_CTRL', hipJnt.replace(JOINT, f'IK_{JOINT}'), mo=True)
    else:
        raise Exception("Warning: no pelvis control exists.")

    cmds.parent(f'{side}_IK_ankle_GRP', 'offset_CTRL')
    cmds.parent(f'{side}_leg_pv_GRP', 'offset_CTRL')

    # FK
    grp = hipJnt.replace(JOINT, f'FK_{GROUP}')

    if cmds.objExists('pelvis_CTRL'):
        cmds.parent(grp, 'pelvis_CTRL')
    else:
        raise Exception("Warning: no pelvis control exists.")



def IKFK_leg(hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt, side):
    ik_leg(hipJnt, kneeJnt, ankleJnt, ballJnt, toeJnt,side)
    fk_leg(hipJnt, kneeJnt, ankleJnt, ballJnt,toeJnt, side)
    IKFK_switch(hipJnt, kneeJnt, ankleJnt, ballJnt,toeJnt, side)


#fk_leg('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT', 'L_ball_JNT', 'L_toe_JNT', LEFT)
#IKFK_switch('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT', 'L_ball_JNT', 'L_toe_JNT', LEFT)


#EXECUTE
