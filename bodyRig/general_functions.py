import sys
import maya.cmds as cmds
import maya.api.OpenMaya as om

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


def getClosestVertex(mayaMesh, pos=[0, 0, 0]):
    mVector = om.MVector(pos)  # using MVector type to represent position
    selectionList = om.MSelectionList()
    selectionList.add(mayaMesh)
    dPath = selectionList.getDagPath(0)
    mMesh = om.MFnMesh(dPath)
    ID = mMesh.getClosestPoint(om.MPoint(mVector), space=om.MSpace.kWorld)[1]  # getting closest face ID
    list = cmds.ls(cmds.polyListComponentConversion(mayaMesh + '.f[' + str(ID) + ']', ff=True, tv=True),
                   flatten=True)  # face's vertices list
    # setting vertex [0] as the closest one
    d = mVector - om.MVector(cmds.xform(list[0], t=True, ws=True, q=True))
    smallestDist2 = d.x * d.x + d.y * d.y + d.z * d.z  # using distance squared to compare distance
    closest = list[0]
    # iterating from vertex [1]
    for i in range(1, len(list)):
        d = mVector - om.MVector(cmds.xform(list[i], t=True, ws=True, q=True))
        d2 = d.x * d.x + d.y * d.y + d.z * d.z
        if d2 < smallestDist2:
            smallestDist2 = d2
            closest = list[i]
    return closest


def connectMeshToAttrCtrl():
    sel = cmds.ls(sl=True)

    for geo in sel:
        cmds.setAttr(f'{geo}.overrideEnabled', 1)
        cmds.connectAttr("C_attr_CTRL.model_display", f'{geo}.overrideDisplayType')
