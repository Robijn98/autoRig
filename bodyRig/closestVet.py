import maya.api.OpenMaya as om
import maya.cmds as cmds


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


sel = cmds.ls(sl=True)
for jnt in sel:
    rootCtrl_pos = cmds.xform(jnt, q=True, t=True, ws=True)
    fol_pos = getClosestVertex('brain_geo_mouth', rootCtrl_pos)

    cmds.select(fol_pos)
    riv = cmds.Rivet()
    riv = cmds.rename('pinOutput', f'{jnt}_rivet')
