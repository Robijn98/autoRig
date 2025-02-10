import sys
import maya.cmds as cmds
import maya.api.OpenMaya as om

class controller:

    GROUP = 'GRP'
    CONTROL = 'CTRL'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'

    def __init__(self, name):
        self.name = name

    def create_temp_ctrl(self, lock = []):
        ctrl = cmds.circle(n = self.name)[0]
        grp = cmds.group(ctrl, n = self.name.replace(self.CONTROL, self.GROUP))

        for transform in lock:
            cmds.setAttr(f'{ctrl}.{transform}', lock=True, keyable=False, channelBox=False)

        return grp, ctrl


    def add_offset(self, suffix = 'OFF'):

        grp_offset = cmds.createNode('transform', name = f'{self.name}_{suffix}')
        self.name_mat = cmds.xform(self.name, q=True, m=True, ws=True)
        cmds.xform(grp_offset, m=self.name_mat, ws=True)

        self.name_parent = cmds.listRelatives(self.name, parent=True)
        if self.name_parent:
            cmds.parent(grp_offset, self.name_parent)
        cmds.parent(self.name, grp_offset)

        return grp_offset


    def connect_mesh_to_attr_ctrl(self, mesh = []):
        for geo in mesh:
            cmds.setAttr(f'{geo}.overrideEnabled', 1)
            cmds.connectAttr("C_attr_CTRL.model_display", f'{geo}.overrideDisplayType')


    def add_offset_grp(self, suffix='OFF'):
        grp_offset = cmds.createNode('transform', name=f'{self.name}_{suffix}')
        self.name_mat = cmds.xform(self.name, q=True, m=True, ws=True)
        cmds.xform(grp_offset, m=self.name_mat, ws=True)

        self.name_parent = cmds.listRelatives(self.name, parent=True)
        if self.name_parent:
            cmds.parent(grp_offset, self.name_parent)
        cmds.parent(self.name, grp_offset)

        return grp_offset


    def add_offset_jnt(self, suffix='OFF'):
        jnt_offset = cmds.joint(name=f'{self.name}_{suffix}')
        self.name_mat = cmds.xform(self.name, q=True, m=True, ws=True)
        cmds.xform(jnt_offset, m=self.name_mat, ws=True)

        self.name_parent = cmds.listRelatives(self.name, parent=True)
        if self.name_parent:
            cmds.parent(jnt_offset, self.name_parent)
        cmds.parent(self.name, jnt_offset)

        return jnt_offset

