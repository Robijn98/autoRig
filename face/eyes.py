import maya.cmds as cmds
import math
import sys
from controller import create_temp_ctrl
from controller import add_offset_grp
from controller import add_offset_jnt


class eye:

    GROUP = 'GRP'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    EYE = 'eye'
    CONTROL = 'CTRL'
    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'

    def __init__(self, side):
        self.side = side

    def eye_guides(self):
        grp = f'{self.side}_{self.EYE}_{self.GUIDE}_{self.GROUP}'
        guides = []

        if cmds.objExists(grp):
            for loc in cmds.listRelatives(grp):
                guides.append(loc)

        return guides

    def create_minor_eye_jnts(self):
        main_grp = cmds.group(empty=True, name=f'{self.side}_{self.EYE}_minor_{self.GROUP}')
        cmds.select(cl=True)

        minor_joints = []
        guides = self.eye_guides()

        mid_eye_guide = f'{self.side}_{self.CENTER}_{self.EYE}_{self.GUIDE}'

        guides.append(mid_eye_guide)

        for guide in guides:
            mat = cmds.xform(guide, q=True, m=True, ws=True)
            jnt = cmds.joint(name=guide.replace(self.GUIDE, self.JOINT))
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

            add_offsetGrp(jnt, suffix = 'OFF')

        #aim_jnt
        aim_guide = f'{self.side}_{self.EYE}Aim_{self.GUIDE}'
        mat = cmds.xform(aim_guide, q=True, m=True, ws=True)
        jnt = cmds.joint(name=aim_guide.replace(self.GUIDE, self.JOINT))
        cmds.setAttr(f'{jnt}.radius', 0.5)
        cmds.xform(jnt, m=mat, ws=True)

        cmds.parent(jnt, main_grp)

        return minor_joints


def eye_connection(self, influenceProcent=0.2):
    aim_jnt = f'{self.side}_{self.EYE}Aim_{self.JOINT}'
    aimed_jnt = f'{self.side}_{self.CENTER}_{self.EYE}_{self.JOINT}'
    cmds.aimConstraint(aim_jnt, aimed_jnt, mo=False, aim=(0, 0, 1))

    #create ctrl
    ctrl_grp, ctrl = create_temp_ctrl(f'{self.side}_{self.EYE}_{self.CONTROL}', lock=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'])
    mat = cmds.xform(aim_jnt, q=True, m=True, ws=True)
    cmds.xform(ctrl_grp, m=mat, ws=True)
    cmds.parent(aim_jnt, ctrl)
    cmds.addAttr(ctrl, ln='fleshy_multiplier',  at='double', min=0, max=5, dv=1, k=True)

    # multiply divide
    jnts = cmds.listRelatives(f'{self.side}_eye_minor_GRP', ad=True, typ='joint')
    amount_jnts = sum(1 for s in jnts if 'upper' in s)
    mid_jnt = math.ceil(amount_jnts / 2)
    mid_jnt_upper = f'{self.side}_{self.EYE}upper_{mid_jnt}_{self.JOINT}'
    mid_jnt_lower = f'{self.side}_{self.EYE}lower_{mid_jnt}_{self.JOINT}'

    multDiv = cmds.createNode('multiplyDivide')
    cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
    cmds.connectAttr(f'{multDiv}.output', f'{mid_jnt_upper}_fleshy.rotate')

    multDivAttr = cmds.createNode('multiplyDivide')
    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr(f'{ctrl}.fleshy_multiplier', f'{multDivAttr}.input1{axis}')
        cmds.setAttr(f"{multDivAttr}.input2{axis}", influenceProcent)

    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr(f'{multDivAttr}.output{axis}',f"{multDiv}.input2{axis}")

    multDiv = cmds.createNode('multiplyDivide')
    cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
    cmds.connectAttr(f'{multDiv}.output', f'{mid_jnt_lower}_fleshy.rotate')

    newProcent = influenceProcent
    leftJnt = mid_jnt + 1
    rightJnt = mid_jnt - 1
    for jnt in range(math.ceil(mid_jnt / 2)):
        newProcent = newProcent / 2

        for num in [leftJnt, rightJnt]:
            jnt_upper = f'{self.side}_{EYE}upper_{num}_{JOINT}'
            jnt_lower = f'{self.side}_{EYE}lower_{num}_{JOINT}'

            multDiv = cmds.createNode('multiplyDivide')
            cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
            cmds.connectAttr(f'{multDiv}.output', f'{jnt_upper}_fleshy.rotate')

            multDivAttr = cmds.createNode('multiplyDivide')
            for axis in ['X', 'Y', 'Z']:
                cmds.connectAttr(f'{ctrl}.fleshy_multiplier', f'{multDivAttr}.input1{axis}')
                cmds.setAttr(f"{multDivAttr}.input2{axis}", influenceProcent)

            for axis in ['X', 'Y', 'Z']:
                cmds.connectAttr(f'{multDivAttr}.output{axis}', f"{multDiv}.input2{axis}")

            multDiv = cmds.createNode('multiplyDivide')
            cmds.connectAttr(f'{aimed_jnt}.rotate', f'{multDiv}.input1')
            cmds.connectAttr(f'{multDiv}.output', f'{jnt_lower}_fleshy.rotate')

            multDivAttr = cmds.createNode('multiplyDivide')
            for axis in ['X', 'Y', 'Z']:
                cmds.connectAttr(f'{ctrl}.fleshy_multiplier', f'{multDivAttr}.input1{axis}')
                cmds.setAttr(f"{multDivAttr}.input2{axis}", influenceProcent)

            for axis in ['X', 'Y', 'Z']:
                cmds.connectAttr(f'{multDivAttr}.output{axis}', f"{multDiv}.input2{axis}")

        leftJnt = leftJnt + 1
        rightJnt = rightJnt - 1


