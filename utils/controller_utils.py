import sys
import maya.cmds as cmds
import maya.api.OpenMaya as om

sys.path.append('/home/s5725067/myRepos/autoRig/')
from rig_constants import *

class controller:

    @staticmethod
    def create_temp_ctrl(name, lock=[]):
        ctrl = cmds.circle(n=name)[0]
        grp = cmds.group(ctrl, n=name.replace(CONTROL, GROUP))

        for transform in lock:
            cmds.setAttr(f'{ctrl}.{transform}', lock=True, keyable=False, channelBox=False)

        return grp, ctrl

    @staticmethod
    def add_offset(name, suffix='OFF'):
        grp_offset = cmds.createNode('transform', name=f'{name}_{suffix}')
        name_mat = cmds.xform(name, q=True, m=True, ws=True)
        cmds.xform(grp_offset, m=name_mat, ws=True)

        name_parent = cmds.listRelatives(name, parent=True)
        if name_parent:
            cmds.parent(grp_offset, name_parent)
        cmds.parent(name, grp_offset)

        return grp_offset

    @staticmethod
    def connect_mesh_to_attr_ctrl(mesh=[]):
        for geo in mesh:
            cmds.setAttr(f'{geo}.overrideEnabled', 1)
            cmds.connectAttr("C_attr_CTRL.model_display", f'{geo}.overrideDisplayType')

    @staticmethod
    def add_offset_grp(name, suffix='OFF'):
        grp_offset = cmds.createNode('transform', name=f'{name}_{suffix}')
        name_mat = cmds.xform(name, q=True, m=True, ws=True)
        cmds.xform(grp_offset, m=name_mat, ws=True)

        name_parent = cmds.listRelatives(name, parent=True)
        if name_parent:
            cmds.parent(grp_offset, name_parent)
        cmds.parent(name, grp_offset)

        return grp_offset

    @staticmethod
    def add_offset_jnt(name, suffix='OFF'):
        jnt_offset = cmds.joint(name=f'{name}_{suffix}')
        name_mat = cmds.xform(name, q=True, m=True, ws=True)
        cmds.xform(jnt_offset, m=name_mat, ws=True)

        name_parent = cmds.listRelatives(name, parent=True)
        if name_parent:
            cmds.parent(jnt_offset, name_parent)
        cmds.parent(name, jnt_offset)

        return jnt_offset
