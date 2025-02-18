import sys
import maya.cmds as cmds
from controller import create_temp_ctrl

class stretchy_limb:

    GROUP = 'GRP'
    CONTROL = 'CTRL'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    ARM = 'arm'
    LEG = 'leg'
    STRETCH = 'stretchy'
    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'

    def __init__(self, joints = [], ik_ctrl, side):
        self.joints = joints
        self.ik_ctrl = ik_ctrl
        self.side = side

    
    def stretch_joints(self):
        cmds.select(clear=True)
        #duplicate chain
        for  jnt in self.joints:
            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            dupl_jnt = cmds.joint(n = jnt.replace(self.JOINT, f'scale_{self.JOINT}'))
            cmds.xform(dupl_jnt, m=mat, ws=True)
            cmds.makeIdentity(dupl_jnt, apply=True, r=True)

    

    def stretchy_proporties(self):
        #create 'attach' ctrl
        root_grp, root_ctrl = create_temp_ctrl(f'{self.side}_{self.ARM}_root_CTRL', lock=['sx', 'sy', 'sz'])
        mat = cmds.xform(self.joints[0], q=True, m=True, ws=True)
        cmds.xform(root_grp, m=mat, ws=True)

        #measure distance between the limbs
        joint1_stretch = self.joints[0].replace(self.JOINT, f'scale_{self.JOINT}')
        joint2_stretch = self.joints[1].replace(self.JOINT, f'scale_{self.JOINT}')
        joint3_stretch = self.joints[2].replace(self.JOINT, f'scale_{self.JOINT}')

        dis_upper = cmds.createNode('distanceBetween', n=f'{self.side}_upper_dist')
        dis_lower = cmds.createNode('distanceBetween', n=f'{self.side}_lower_dist')

        cmds.connectAttr(f'{joint1_stretch}.worldMatrix[0]', f'{dis_upper}.inMatrix1')
        cmds.connectAttr(f'{joint2_stretch}.worldMatrix[0]', f'{dis_upper}.inMatrix2')

        cmds.connectAttr(f'{joint2_stretch}.worldMatrix[0]', f'{dis_lower}.inMatrix1')
        cmds.connectAttr(f'{joint3_stretch}.worldMatrix[0]', f'{dis_lower}.inMatrix2')

        doubleLin = cmds.createNode('addDoubleLinear', n=f'{self.side}_fullDist')

        cmds.connectAttr(f'{dis_upper}.distance', f'{doubleLin}.input1')
        cmds.connectAttr(f'{dis_lower}.distance', f'{doubleLin}.input2')

        fullDist_distance = cmds.getAttr(f'{doubleLin}.output')

        #measure distance to the IK_Ctrl
        loc_end = cmds.spaceLocator(n=f'{self.side}_{self.ARM}_stretchEnd')
        cmds.hide(loc_end)
        mat = cmds.xform(self.ik_ctrl, q=True, m=True, ws=True)
        cmds.xform(loc_end, m=mat, ws=True)
        cmds.parent(loc_end, self.ik_ctrl)
        
        dis_stretch = cmds.createNode('distanceBetween', n=f'{self.side}_stretchDist1')
        cmds.connectAttr(f'{self.side}_{self.ARM}_root_CTRL.worldMatrix[0]', f'{dis_stretch}.inMatrix1')
        cmds.connectAttr(f'{loc_end[0]}.worldMatrix[0]', f'{dis_stretch}.inMatrix2')
        dis_stretch_distance = cmds.getAttr(f'{dis_stretch}.distance')

        #condition to check if IK is longer than ge
        con = cmds.createNode('condition', n=f'{self.side}_condition')
        cmds.connectAttr(f'{dis_stretch}.distance', f'{con}.firstTerm')
        cmds.connectAttr(f'{doubleLin}.output', f'{con}.secondTerm')

        multDiv = cmds.createNode('multiplyDivide', n = f'{self.side}_multi')
        cmds.connectAttr(f'{con}.outColorR', f"{self.joints[0].replace(self.JOINT, f'IK_{self.JOINT}')}.scaleX")
        cmds.connectAttr(f'{con}.outColorR', f"{self.joints[1].replace(self.JOINT, f'IK_{self.JOINT}')}.scaleX")

        cmds.connectAttr(f'{dis_stretch}.distance', f'{multDiv}.input1X')
        cmds.connectAttr(f'{doubleLin}.output', f'{multDiv}.input2X')
        cmds.setAttr(f'{multDiv}.operation', 2)

        #connect the scale to the joints
        cmds.setAttr(f'{con}.operation', 2)
        cmds.connectAttr(f'{multDiv}.outputX', f'{con}.colorIfTrueR')
        
        #on and off switch
        cmds.addAttr(self.ik_ctrl, ln='stretch',  at='enum', en='off:stretch:squash', k=True)

        con_stretch = cmds.createNode('condition')

        cmds.connectAttr(f'{self.ik_ctrl}.stretch', f'{con_stretch}.firstTerm')
        cmds.setAttr(f'{con_stretch}.colorIfTrueR', 0)
        cmds.setAttr(f'{con_stretch}.colorIfFalseR', 2)

        con_squash = cmds.createNode('condition')

        cmds.connectAttr(f'{self.ik_ctrl}.stretch', f'{con_squash}.firstTerm')
        cmds.setAttr(f'{con_squash}.colorIfTrueR', 0)
        cmds.setAttr(f'{con_squash}.colorIfFalseR', 4)

        con_off = cmds.createNode('condition')

        cmds.connectAttr(f'{con_squash}.outColorR', f'{con_off}.colorIfTrueR')
        cmds.connectAttr(f'{con_stretch}.outColorR', f'{con_off}.colorIfFalseR')

        cmds.connectAttr(f'{self.ik_ctrl}.stretch', f'{con_off}.firstTerm')

        cmds.setAttr(f'{con_off}.secondTerm', 2)
        cmds.connectAttr(f'{con_off}.outColorR', f'{con}.operation')


#Execute
#stretchy_limb(joints = ['L_arm_shoulder_JNT', 'L_arm_elbow_JNT', 'L_arm_wrist_JNT'], ik_ctrl = 'L_arm_wrist_CTRL', side = 'L').stretch_joints()
