import sys
import maya.cmds as cmds

GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'



def create_tempCtrl(name, lock = []):
    ctrl = cmds.circle(n = name)[0]
    grp = cmds.group(ctrl, n = name.replace(CONTROL, GROUP))

    for transform in lock:
        cmds.setAttr(f'{ctrl}.{transform}', lock=True, keyable=False, channelBox=False)

    return grp, ctrl


def addOffset(dst, suffix = 'OFF'):

    grp_offset = cmds.createNode('transform', name = f'{dst}_{suffix}')
    dst_mat = cmds.xform(dst, q=True, m=True, ws=True)
    cmds.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = cmds.listRelatives(dst, parent=True)
    if dst_parent:
        cmds.parent(grp_offset, dst_parent)
    cmds.parent(dst, grp_offset)

    return grp_offset
