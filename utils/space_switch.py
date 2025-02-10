import maya.cmds as cmds

class space_switch:
    
    def __init__(self, side, part):
        self.side = side
        self.part = part

    def create_space_switch(self, parents = []):
        
        #cmds.addAttr(f'{self.side}_IK_{self.part}_CTRL', ln='spaceSwitch', at='enum', en="root:chest:body:", k=True)
        enum = ':'.join(parents)
        cmds.addAttr(f'{self.side}_IK_{self.part}_CTRL', ln='spaceSwitch', at='enum', en=enum, k=True)

        for parent in parents:
            pc = cmds.parentConstraint(f'{parent}_CTRL', f'{self.side}_IK_{self.part}_GRP', mo=True)
            con = cmds.createNode('condition')
            cmds.setAttr(f'{con}.colorIfTrueR', 1)
            cmds.setAttr(f'{con}.colorIfFalseR', 0)
            cmds.connectAttr(f'{self.side}_IK_{self.part}_CTRL.spaceSwitch', f'{con}.firstTerm')
            cmds.setAttr(f'{con}.secondTerm', parents.index(parent))
            cmds.connectAttr(f'{con}.outColorR', f'{self.side}_IK_{self.part}_GRP_parentConstraint1.{parent}_CTRLW{parents.index(parent)}')
