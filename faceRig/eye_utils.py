import maya.cmds as cmds
import math


GROUP = 'GRP'
JOINT = 'JNT'
GUIDE = 'GUIDE'
EYE = 'eye'

#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'


def addOffsetGrp(dst, suffix='OFF'):
    grp_offset = cmds.createNode('transform', name=f'{dst}_{suffix}')
    dst_mat = cmds.xform(dst, q=True, m=True, ws=True)
    cmds.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = cmds.listRelatives(dst, parent=True)
    if dst_parent:
        cmds.parent(grp_offset, dst_parent)
    cmds.parent(dst, grp_offset)

    return grp_offset


def addOffsetJnt(dst, suffix='OFF'):
    jnt_offset = cmds.joint(name=f'{dst}_{suffix}')
    dst_mat = cmds.xform(dst, q=True, m=True, ws=True)
    cmds.xform(jnt_offset, m=dst_mat, ws=True)

    dst_parent = cmds.listRelatives(dst, parent=True)
    if dst_parent:
        cmds.parent(jnt_offset, dst_parent)
    cmds.parent(dst, jnt_offset)

    return jnt_offset


def createEyeGuides(side, number=3):
    # creating groups to store guides
    eye_guide_grp = cmds.createNode('transform', name=f'{side}_{EYE}_{GUIDE}_{GROUP}')

    eyes_locs_grp = cmds.createNode('transform', name=f'{side}_{EYE}_minor_{GUIDE}_{GROUP}',
                                    parent=eye_guide_grp)

    # create locators
    for part in ['upper', 'lower']:

        part_mult = 1 if part == 'upper' else -1
        mid_data = (0, part_mult, 0)

        for x in range(number):
            multiplier = x + 1 if side == 'L' else -(x + 1)
            loc_data = (multiplier, part_mult, 0)
            loc = cmds.spaceLocator(name=f'{side}_{EYE}{part}_{x + 1}_{GUIDE}')[0]
            cmds.parent(loc, eyes_locs_grp)

            # set data
            cmds.setAttr(f'{loc}.t', *loc_data)

    # create corners
    left_corner_loc = cmds.spaceLocator(name=f'{side}_{LEFT}_{EYE}Corner_{GUIDE}')[0]
    right_corner_loc = cmds.spaceLocator(name=f'{side}_{RIGHT}_{EYE}Corner_{GUIDE}')[0]

    cmds.parent(left_corner_loc, eyes_locs_grp)
    cmds.parent(right_corner_loc, eyes_locs_grp)

    if side == 'L':
        cmds.setAttr(f'{left_corner_loc}.translateX', number + 1)
    else:
        cmds.setAttr(f'{right_corner_loc}.translateX', -(number + 1))

    cmds.select(cl=True)

    # create jaw_base
    eye_base_guide_grp = cmds.createNode('transform', name=f'{CENTER}_{EYE}_base_{GUIDE}_{GROUP}',
                                         parent=eye_guide_grp)
    jaw_guide = cmds.spaceLocator(name=f'{side}_{CENTER}_{EYE}_{GUIDE}')[0]

    if side == 'L':
        cmds.setAttr(f'{jaw_guide}.t', *(math.ceil(number / 2), 0, -number))
    else:
        cmds.setAttr(f'{jaw_guide}.t', *(-math.ceil(number / 2), 0, -number))

    cmds.parent(jaw_guide, eye_base_guide_grp)

    # release selection
    cmds.select(cl=True)

    aim_locator = cmds.spaceLocator(name=f'{side}_{EYE}Aim_{GUIDE}')[0]

    if side == 'L':
        cmds.setAttr(f'{aim_locator}.t', *(math.ceil(number / 2), 0, 3))
    else:
        cmds.setAttr(f'{aim_locator}.t', *(-math.ceil(number / 2), 0, 3))

    cmds.parent(aim_locator, eye_base_guide_grp)



def eye_guides(side):
    grp = f'{side}_{EYE}_minor_{GUIDE}_{GROUP}'
    guides = []

    if cmds.objExists(grp):
        for loc in cmds.listRelatives(grp):
            guides.append(loc)

    return guides


def createMinorEyeJoints(side):
    main_grp = cmds.group(empty=True, name=f'{side}_{EYE}_minor_{GROUP}')
    cmds.select(cl=True)

    minor_joints = []
    guides = eye_guides(side)

    mid_eye_guide = f'{side}_{CENTER}_{EYE}_{GUIDE}'

    guides.append(mid_eye_guide)

    for guide in guides:
        mat = cmds.xform(guide, q=True, m=True, ws=True)
        jnt = cmds.joint(name=guide.replace(GUIDE, JOINT))
        cmds.setAttr(f'{jnt}.radius', 0.5)
        cmds.xform(jnt, m=mat, ws=True)

        cmds.parent(jnt, main_grp)

        minor_joints.append(jnt)

        #SDK offset group
        grp_offset = cmds.createNode('transform', name=f'{jnt}_SDK')
        dst_mat = cmds.xform(mid_eye_guide, q=True, m=True, ws=True)
        cmds.xform(grp_offset, m=dst_mat, ws=True)

        dst_parent = cmds.listRelatives(jnt, parent=True)
        if dst_parent:
            cmds.parent(grp_offset, dst_parent)
        cmds.parent(jnt, grp_offset)


        #fleshy offset group
        grp_offset = cmds.createNode('transform', name=f'{jnt}_fleshy')
        dst_mat = cmds.xform(mid_eye_guide, q=True, m=True, ws=True)
        cmds.xform(grp_offset, m=dst_mat, ws=True)

        dst_parent = cmds.listRelatives(jnt, parent=True)
        if dst_parent:
            cmds.parent(grp_offset, dst_parent)
        cmds.parent(jnt, grp_offset)

        addOffsetGrp(jnt, suffix = 'OFF')

    #aim_jnt
    aim_guide = f'{side}_{EYE}Aim_{GUIDE}'
    mat = cmds.xform(aim_guide, q=True, m=True, ws=True)
    jnt = cmds.joint(name=aim_guide.replace(GUIDE, JOINT))
    cmds.setAttr(f'{jnt}.radius', 0.5)
    cmds.xform(jnt, m=mat, ws=True)

    cmds.parent(jnt, main_grp)

    return minor_joints


def eyeConnection(side, influenceProcent=0.2):
    aim_jnt = f'{side}_{EYE}Aim_{JOINT}'
    aimed_jnt = f'{side}_{CENTER}_{EYE}_{JOINT}'
    cmds.aimConstraint(aim_jnt, aimed_jnt, mo=False, aim=(0, 0, 1))

    # multiply divide
    jnts = cmds.listRelatives('L_eye_minor_GRP', ad=True, typ='joint')
    amount_jnts = sum(1 for s in jnts if 'upper' in s)
    mid_jnt = math.ceil(amount_jnts / 2)
    mid_jnt_upper = f'{side}_{EYE}upper_{mid_jnt}_{JOINT}'
    mid_jnt_lower = f'{side}_{EYE}lower_{mid_jnt}_{JOINT}'

    multDiv = cmds.createNode('multiplyDivide')
    cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
    cmds.connectAttr(f'{multDiv}.output', f'{mid_jnt_upper}_fleshy.rotate')
    for axis in ['X', 'Y', 'Z']:
        cmds.setAttr(f"{multDiv}.input2{axis}", influenceProcent)
    #cmds.setAttr(f"{multDiv}.input2X", influenceProcent)
    #cmds.setAttr(f"{multDiv}.input2Y", influenceProcent)
    #cmds.setAttr(f"{multDiv}.input2Z", influenceProcent)

    multDiv = cmds.createNode('multiplyDivide')
    cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
    cmds.connectAttr(f'{multDiv}.output', f'{mid_jnt_lower}_fleshy.rotate')
    for axis in ['X', 'Y', 'Z']:
        cmds.setAttr(f"{multDiv}.input2{axis}", influenceProcent)

    #cmds.setAttr(f"{multDiv}.input2X", influenceProcent)
    #cmds.setAttr(f"{multDiv}.input2Y", influenceProcent)
    #cmds.setAttr(f"{multDiv}.input2Z", influenceProcent)

    newProcent = influenceProcent
    leftJnt = mid_jnt + 1
    rightJnt = mid_jnt - 1
    for jnt in range(math.ceil(mid_jnt / 2)):
        newProcent = newProcent / 2

        for num in [leftJnt, rightJnt]:
            jnt_upper = f'{side}_{EYE}upper_{num}_{JOINT}'
            jnt_lower = f'{side}_{EYE}lower_{num}_{JOINT}'
            multDiv = cmds.createNode('multiplyDivide')
            cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
            cmds.connectAttr(f'{multDiv}.output', f'{jnt_upper}_fleshy.rotate')
            for axis in ['X', 'Y', 'Z']:
                cmds.setAttr(f"{multDiv}.input2{axis}", newProcent)
            #cmds.setAttr(f"{multDiv}.input2X", newProcent)
            #cmds.setAttr(f"{multDiv}.input2Y", newProcent)
            #cmds.setAttr(f"{multDiv}.input2Z", newProcent)

            multDiv = cmds.createNode('multiplyDivide')
            cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
            cmds.connectAttr(f'{multDiv}.output', f'{jnt_lower}_fleshy.rotate')
            for axis in ['X', 'Y', 'Z']:
                cmds.setAttr(f"{multDiv}.input2{axis}", newProcent)
            #cmds.setAttr(f"{multDiv}.input2X", newProcent)
            #cmds.setAttr(f"{multDiv}.input2Y", newProcent)
            #cmds.setAttr(f"{multDiv}.input2Z", newProcent)

        leftJnt = leftJnt + 1
        rightJnt = rightJnt - 1



