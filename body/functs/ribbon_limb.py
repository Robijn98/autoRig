import math
import maya.cmds as cmds
import sys
from general_functions import create_tempCtrl
from general_functions import addOffset


class ribbon:

    GROUP = 'GRP'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    CONTROL = 'CTRL'

    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'

    def __init__(self, side, name):
        self.side = side
        self.name = name

    def return_guides(self):
        guide_grp = f'{self.side}_{self.name}_{self.GUIDE}_{self.GROUP}'
        guides = []

        if cmds.objExists(guide_grp):
            for loc in cmds.listRelatives(guide_grp, c=True):
                guides.append(loc)

        return guides


    def create_ribbon(self):
        guides = self.return_guides()
        guideAmount = len(guides)-1

        dist = cmds.createNode('distanceBetween')
        cmds.connectAttr(f'{guides[0]}.translate', f'{dist}.point1')
        cmds.connectAttr(f'{guides[-1]}.translate', f'{dist}.point2')
        distance = cmds.getAttr(f'{dist}.distance')

        plane = cmds.nurbsPlane(p=[0, 0, 0], ax=[0, 1, 0], w=distance, lr=0.1, d=3, u=guideAmount, v=1,
                                n=f'{self.side}_{self.name}_plane')[0]
        grp = cmds.group(em=True, n=f'{self.side}_{self.name}_follicle_{self.GROUP}')

        parameterU = 0
        changeDistance = 1/(guideAmount)
        for i in range(len(guides)):
            y = str(i + 1)
            fol = cmds.createNode('follicle')
            fol = cmds.rename('follicle1', f'{self.side}_{self.name}_follicle_0{y}')

            cmds.parent(fol, grp, s=True)
            cmds.makeIdentity(plane, apply=True, t=1, r=1, s=1, n=0)

            cmds.connectAttr(f'{self.side}_{self.name}_follicle_Shape{y}.outRotate', f'{fol}.rotate', f=True)
            cmds.connectAttr(f'{self.side}_{self.name}_follicle_Shape{y}.outTranslate', f'{fol}.translate')
            cmds.connectAttr(f'{plane}Shape.worldMatrix', f'{self.side}_{self.name}_follicle_Shape{y}.inputWorldMatrix')
            cmds.connectAttr(f'{plane}Shape.local', f'{self.side}_{self.name}_follicle_Shape{y}.inputSurface')

            cmds.setAttr(f'{fol}.parameterV', 0.5)
            cmds.setAttr(f'{fol}.parameterU', parameterU)
            parameterU += changeDistance

    def create_ribbon_jnts(self):
        jnts = []
        ctrl_jnts = []
        plane = f'{self.side}_{self.name}_plane'
        follicles = cmds.listRelatives(f'{self.side}_{self.name}_follicle_{self.GROUP}')
        for fol in follicles:
            y = len(follicles)
            cmds.select(d=True)
            jnt = cmds.joint(n=f'joint_{y+1}')
            pc = cmds.parentConstraint(fol, jnt, mo=False)
            cmds.delete(pc)
            jnts.append(jnt)
        
        cmds.select(jnts, plane)
        #fix this to specific values so it doesnt get fucked if the settings change, thank you
        cmds.SmoothBindSkin(tsb=True, cj=False)
        
        for num, jnt in enumerate(jnts):
            num += 1
            if jnt == jnts[-1]:
                pc = cmds.parentConstraint(f'{self.side}_{self.name}_{self.GUIDE}_{num}', jnt, mo=False)
                cmds.delete(pc)
            else:
                pc = cmds.parentConstraint(f'{self.side}_{self.name}_{self.GUIDE}_{num}', jnt, mo=False)
                cmds.delete(pc)
        
        cmds.select(f'{self.side}_{self.name}_plane')
        cmds.DeleteHistory()
        
        for num, jnt in enumerate(jnts):    
            duplicate_jnt = cmds.duplicate(jnt)
            num += 1
            jnt = cmds.rename(jnt, f'{self.side}_{self.name}_skin_{self.JOINT}_0{num}')
            cmds.parent(jnt, f'{self.side}_{self.name}_follicle_0{num}')
            
            duplicate_jnt = cmds.rename(duplicate_jnt, f'{self.side}_{self.name}_{self.JOINT}_0{num}')
            ctrl_jnts.append(duplicate_jnt)

        ctrl_grp = cmds.group(empty=True, n=f'{self.side}_{self.name}_{self.GROUP}')
        cmds.parent(ctrl_jnts, ctrl_grp)
        cmds.group(plane, f'{self.side}_{self.name}_follicle_{self.GROUP}', n=f'{self.side}_{self.name}_{self.GROUP}_noTransform')

        cmds.select(ctrl_jnts, f'{self.side}_{self.name}_plane')
        #fix this to specific values so it doesnt get fucked if the settings change, thank you
        cmds.SmoothBindSkin(tsb=True, cj=False)

        
    def create_ribbon_ctrls(self):
        ctrl_amount = len(self.return_guides())
        mainJnts = [f'{self.side}_{self.name}_{self.JOINT}_0{1}', f'{self.side}_{self.name}_{self.JOINT}_0{math.ceil(ctrl_amount/2)}', f'{self.side}_{self.name}_{self.JOINT}_0{ctrl_amount}']

        num = 0
        for i in range(ctrl_amount):
            num += 1
            jnt = f'{self.side}_{self.name}_{self.JOINT}_0{num}'
            ctrl_grp, ctrl = create_tempCtrl(f'{self.side}_{self.name}_0{num}_{self.CONTROL}', lock=[])
            mat = cmds.xform(jnt, q=True, m=True, ws=True)
            cmds.xform(ctrl_grp, m=mat, ws=True)
            if jnt not in mainJnts:
                addOffset(ctrl)

            cmds.parent(jnt, ctrl)

        upperLoc = cmds.spaceLocator(n = f'{self.side}_{self.name}_upperAimLoc')
        lowerLoc = cmds.spaceLocator(n = f'{self.side}_{self.name}_lowerAimLoc')

        mat = cmds.xform(f'{self.side}_{self.name}_01_{self.CONTROL}', q=True, m=True, ws=True)
        cmds.xform(upperLoc, m=mat, ws=True)
        cmds.parent(upperLoc, f'{self.side}_{self.name}_01_{self.CONTROL}')

        mat = cmds.xform(f'{self.side}_{self.name}_0{math.ceil(ctrl_amount/2)}_{self.CONTROL}', q=True, m=True, ws=True)
        cmds.xform(lowerLoc, m=mat, ws=True)
        cmds.parent(lowerLoc, f'{self.side}_{self.name}_0{math.ceil(ctrl_amount/2)}_{self.CONTROL}')

        cmds.delete(f'{self.side}_{self.name}_{self.GROUP}')

    def connect_ribbon_to_joints(self, joints = []):
        ctrl_amount = len(self.return_guides())

        mainCtrls = [f'{self.side}_{self.name}_0{1}_{self.CONTROL}', f'{self.side}_{self.name}_0{math.ceil(ctrl_amount/2)}_{self.CONTROL}', f'{self.side}_{self.name}_0{ctrl_amount}_{self.CONTROL}']

        ctrls_upperLimb = []
        ctrls_lowerLimb = []

        mid_jnt = math.ceil(ctrl_amount / 2)

        for num, ctrl in enumerate(mainCtrls):
            offset = addOffset(ctrl)
            cmds.parentConstraint(joints[num], offset, mo=True)

        for num in range(1, ctrl_amount):

            if num<mid_jnt:
                ctrls_upperLimb.append(f'{self.side}_{self.name}_0{num}_{self.CONTROL}')

            if num>mid_jnt:
                ctrls_lowerLimb.append(f'{self.side}_{self.name}_0{num}_{self.CONTROL}')


        for ctrl in ctrls_upperLimb:
            if ctrl not in mainCtrls:
                cmds.pointConstraint(mainCtrls[0], f'{ctrl}_OFF', mo=True)
                cmds.pointConstraint(mainCtrls[1], f'{ctrl}_OFF', mo=True)
                cmds.aimConstraint(mainCtrls[0],f'{ctrl}_OFF', wut = 'objectrotation', wuo = f'{self.side}_{self.name}_upperAimLoc', mo=True)

        for ctrl in ctrls_lowerLimb:
            if ctrl not in mainCtrls:
                cmds.pointConstraint(mainCtrls[1], f'{ctrl}_OFF', mo=True)
                cmds.pointConstraint(mainCtrls[2], f'{ctrl}_OFF', mo=True)
                cmds.aimConstraint(mainCtrls[1], f'{ctrl}_OFF', wut = 'objectrotation', wuo = f'{self.side}_{self.name}_lowerAimLoc',u = [0, -1, 0], mo=True)


        stretchGroup = cmds.group(empty=True, n=f'{self.side}_{self.name}_stretch')

        for ctrl in range(ctrl_amount):
            cmds.parent(f'{self.side}_{self.name}_0{ctrl+1}_{self.GROUP}', stretchGroup)

    
    def create_ribbon_limb(self, joints = []):
        self.create_ribbon()
        self.create_ribbon_jnts()
        self.create_ribbon_ctrls()
        self.connect_ribbon_to_joints(joints)





