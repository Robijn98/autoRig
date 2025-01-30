
import maya.cmds as cmds


WRIST = 'wrist'
def spaceSwitch_wrist(side):
    # after ctrl creation
    cmds.addAttr(f'{side}_IK_{WRIST}_CTRL', ln='spaceSwitch', at='enum', en="root:chest:body:", k=True)

    # L_hand_pc = cmds.parentConstraint('root_CTRL', f'{side}_IK_{WRIST}_GRP' ,mo=True)
    chest_pc = cmds.parentConstraint('chest_CTRL', f'{side}_IK_{WRIST}_GRP', mo=True)
    body_pc = cmds.parentConstraint('body_CTRL', f'{side}_IK_{WRIST}_GRP', mo=True)

    con = cmds.createNode('condition')
    cmds.setAttr(f'{con}.colorIfTrueR', 1)
    cmds.setAttr(f'{con}.colorIfFalseR', 0)
    cmds.connectAttr(f'{side}_IK_{WRIST}_CTRL.spaceSwitch', f'{con}.firstTerm')
    cmds.setAttr(f'{con}.secondTerm', 1)
    cmds.connectAttr(f'{con}.outColorR', f'{side}_IK_{WRIST}_GRP_parentConstraint1.chest_CTRLW0')

    con = cmds.createNode('condition')
    cmds.setAttr(f'{con}.colorIfTrueR', 1)
    cmds.setAttr(f'{con}.colorIfFalseR', 0)
    cmds.connectAttr(f'{side}_IK_{WRIST}_CTRL.spaceSwitch', f'{con}.firstTerm')
    cmds.setAttr(f'{con}.secondTerm', 2)
    cmds.connectAttr(f'{con}.outColorR', f'{side}_IK_{WRIST}_GRP_parentConstraint1.body_CTRLW1')

def lock_pv(side):
    # after ctrl creation
    cmds.addAttr(f'{side}_arm_pv_CTRL', ln='lock', at='enum', en="off:on:", k=True)

    chest_pc = cmds.parentConstraint(f'{side}_IK_wrist_CTRL', f'{side}_arm_pv_GRP', mo=True)

    con = cmds.createNode('condition')
    cmds.setAttr(f'{con}.colorIfTrueR', 1)
    cmds.setAttr(f'{con}.colorIfFalseR', 0)
    cmds.connectAttr(f'{side}_arm_pv_CTRL.lock', f'{con}.firstTerm')
    cmds.setAttr(f'{con}.secondTerm', 1)
    cmds.connectAttr(f'{con}.outColorR', f'{side}_arm_pv_GRP_parentConstraint1.{side}_IK_wrist_CTRLW0')

