import sys
import maya.cmds as cmds
import importlib

sys.path.append('/home/s5725067/myRepos/autoRig/')
import rig_constants
importlib.reload(rig_constants)
from rig_constants import *

sys.path.append('/home/s5725067/myRepos/autoRig/utils/')
import controller_utils
importlib.reload(controller_utils)
from controller_utils import controller



class IKFK_spine:

    def __init__(self, spineJoints=[]):
        self.spineJoints = spineJoints
        print(f"Initializing spine with joints: {spineJoints}")

    def fk_spine(self, amountOfCtrls = 4):

        startPoint = cmds.xform(self.spineJoints[0], q=True, t=True, ws=True)
        endPoint = cmds.xform(self.spineJoints[-1], q=True, t=True, ws=True)
        spineCurve = cmds.curve(n = f'{SPINE}_FK_curve', p=[startPoint, endPoint], d=1)
        cmds.rebuildCurve(spineCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kep=1, kt=0, s=1, d=3)

        #create FK joints
        for CV in range(amountOfCtrls):
            pos = cmds.pointPosition(f'{spineCurve}.cv[{CV}]', w=True)

            origin_jnt = self.spineJoints[CV]
            FK_jnt = cmds.joint(n = origin_jnt.replace(JOINT, f'FK_{JOINT}'), p=pos)

            oc = cmds.orientConstraint(self.spineJoints[0], FK_jnt, mo=False)
            cmds.delete(oc)

        cmds.select(d=True)

        #parent FK ctrls in right order
        for CV in range(amountOfCtrls):
            origin_jnt = self.spineJoints[CV]
            FK_jnt =  origin_jnt.replace(JOINT, f'FK_{JOINT}')
            FK_grp, FK_ctrl = controller.create_temp_ctrl(FK_jnt.replace(JOINT, CONTROL), lock=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])
            mat = cmds.xform(FK_jnt, q=True, m=True, ws=True)
            cmds.xform(FK_grp, m=mat, ws=True)

            if CV != 0:
                prev_jnt = self.spineJoints[CV-1]
                prev_ctrl = prev_jnt.replace(JOINT, f'FK_{CONTROL}')
                cmds.parent(FK_grp, prev_ctrl)


            cmds.parentConstraint(FK_ctrl, FK_jnt, mo=True)


    def ik_spine(self):

        #create controls
        startPoint = cmds.xform(self.spineJoints[0], q=True, m=True, ws=True)
        endPoint = cmds.xform(self.spineJoints[-1], q=True, m=True, ws=True)

        body_grp, body_ctrl = controller.create_temp_ctrl(f'body_{CONTROL}', lock=['sx', 'sy', 'sz'])
        cmds.xform(body_grp, m=startPoint, ws=True)

        pelvis_grp, pelvis_ctrl = controller.create_temp_ctrl(f'pelvis_{CONTROL}', lock=['sx', 'sy', 'sz'])
        cmds.xform(pelvis_grp, m=startPoint, ws=True)


        chest_grp, chest_ctrl = controller.create_temp_ctrl(f'chest_{CONTROL}', lock=['sx', 'sy', 'sz'])
        cmds.xform(chest_grp, m=endPoint, ws=True)


        #create IK spline
        IK_spine = cmds.ikHandle(n=f'{SPINE}_IK', sol='ikSplineSolver', sj=self.spineJoints[0], ee=self.spineJoints[-1], ns=1,
                                rtm=False, pcv=False)
        IK_curve = cmds.rename(IK_spine[2], f'{SPINE}_IK_curve')

        cmds.select(d=True)
        pelvis_jnt = cmds.joint(n=f'pelvis_{JOINT}')
        cmds.xform(pelvis_jnt, m=startPoint, ws=True)
        cmds.parent(pelvis_jnt, pelvis_ctrl)

        cmds.select(d=True)
        chest_jnt = cmds.joint(n=f'chest_{JOINT}')
        cmds.xform(chest_jnt, m=endPoint, ws=True)
        cmds.parent(chest_jnt, chest_ctrl)

        cmds.select(IK_curve, pelvis_jnt, chest_jnt)
        cmds.SmoothBindSkin()

        #correct twist settings
        cmds.setAttr(f"{IK_spine[0]}.dTwistControlEnable", 1)
        cmds.setAttr(f"{IK_spine[0]}.dWorldUpType", 4)

        cmds.connectAttr(f"{pelvis_ctrl}.worldMatrix[0]", f"{IK_spine[0]}.dWorldUpMatrix")
        cmds.connectAttr(f"{chest_ctrl}.worldMatrix", f"{IK_spine[0]}.dWorldUpMatrixEnd")

        #connect
        cmds.parent(chest_grp, self.spineJoints[3].replace(JOINT, f"FK_{CONTROL}"))
        cmds.parent(pelvis_grp, body_ctrl)
        cmds.parent(self.spineJoints[0].replace(JOINT, f"FK_{JOINT}"), body_ctrl)
        cmds.parent(self.spineJoints[0].replace(JOINT, f"FK_{GROUP}"), body_ctrl)


    def stretchSquashSpine(self):
        #stretch squash
        curveInfo = cmds.createNode('curveInfo', n= 'spineLength')

        cmds.connectAttr('spine_IK_curveShape.worldSpace[0]', f'{curveInfo}.inputCurve')

        multDiv = cmds.createNode('multiplyDivide')

        #cmds.connectAttr(f'{curveInfo}.arcLength', f'{multDiv}.input1X')
        cmds.setAttr(f'{multDiv}.operation', 2)

        og_length = cmds.getAttr(f'{curveInfo}.arcLength')
        cmds.setAttr(f'{multDiv}.input2X', og_length)


        #volume preservation
        multDiv_volume = cmds.createNode('multiplyDivide', n = 'spine_squareRootX_Pow')
        cmds.connectAttr(f'{multDiv}.outputX', f'{multDiv_volume}.input1X')
        cmds.setAttr(f'{multDiv_volume}.input2X', -0.5)
        cmds.setAttr(f'{multDiv_volume}.operation', 3)


        #global scale
        spineNorm = cmds.createNode('multiplyDivide', n='globalSpine_normalize')

        cmds.connectAttr('master_CTRL.scaleY', 'master_CTRL.scaleX')
        cmds.connectAttr('master_CTRL.scaleY', 'master_CTRL.scaleZ')

        cmds.connectAttr('master_CTRL.scaleY', f'{spineNorm}.input2X')
        cmds.connectAttr('spineLength.arcLength', f'{spineNorm}.input1X')

        cmds.connectAttr(f'{spineNorm}.outputX', f'{multDiv}.input1X')

        cmds.setAttr(f'{spineNorm}.operation', 2)


        for jnt in self.spineJoints:
            if self.spineJoints[0] == jnt:
                print('skipping first spine joint')
            else:
                cmds.connectAttr(f'{multDiv}.outputX', f'{jnt}.scaleX')
                cmds.connectAttr(f'{multDiv_volume}.outputX', f'{jnt}.scaleY')
                cmds.connectAttr(f'{multDiv_volume}.outputX', f'{jnt}.scaleZ')


    def spine(self, amountOfFKCtrls = 4, stretchSquash=False):
        self.fk_spine(amountOfCtrls=amountOfFKCtrls)
        self.ik_spine()
        if stretchSquash:
            self.stretchSquashSpine()
        print("Spine setup complete")