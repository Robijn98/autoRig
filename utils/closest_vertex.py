import maya.api.OpenMaya as om
import maya.cmds as cmds

class closest_vertex:

    def __init__(self, mayaMesh, pos=[0, 0, 0]):
        self.mayaMesh = mayaMesh
        self.pos = pos
    
    def get_closest_vertex(self):
        mVector = om.MVector(self.pos)
        selectionList = om.MSelectionList()
        selectionList.add(self.mayaMesh)
        dPath = selectionList.getDagPath(0)
        mMesh = om.MFnMesh(dPath)
        ID = mMesh.getClosestPoint(om.MPoint(mVector), space=om.MSpace.kWorld)[1]
        list = cmds.ls(cmds.polyListComponentConversion(self.mayaMesh + '.f[' + str(ID) + ']', ff=True, tv=True), flatten=True)
        d = mVector - om.MVector(cmds.xform(list[0], t=True, ws=True, q=True))
        smallestDist2 = d.x * d.x + d.y * d.y + d.z * d.z
        closest = list[0]
        for i in range(1, len(list)):
            d = mVector - om.MVector(cmds.xform(list[i], t=True, ws=True, q=True))
            d2 = d.x * d.x + d.y * d.y + d.z * d.z
            if d2 < smallestDist2:
                smallestDist2 = d2
                closest = list[i]
        return closest


    def create_rivet(self, jnts = []):
        for jnt in jnts:
            rootCtrl_pos = cmds.xform(jnt, q=True, t=True, ws=True)
            fol_pos = self.get_closest_vertex()
            cmds.select(fol_pos)
            riv = cmds.Rivet()
            riv = cmds.rename('pinOutput', f'{jnt}_rivet')


# Usage:
# import closest_vertex
# cv = closest_vertex.closest_vertex('pCube1')
# cv.create_rivet(['joint1', 'joint2', 'joint3'])

