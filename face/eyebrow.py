import math
import maya.cmds as cmds

class eyebrow:

    GROUP = 'GRP'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    BROW = 'eyebrow'
    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'


    def __init__(self, side, name):
        self.side = side
        self.name = name


    def eyebrow_guides(self, number=4):
        eyebrow_guide_grp = f'{self.side}_{self.name}_{GUIDE}_{GROUP}'
        guides = []

        if cmds.objExists(eyebrow_guide_grp):
            for loc in cmds.listRelatives(eyebrow_guide_grp, c=True):
                guides.append(loc)

        return guides


    def create_eyebrow_ribbon(self):
        listName = self.eyebrow_guides()
        planeLength = len(listName)

        plane = cmds.nurbsPlane(p=[planeLength / 2, 0, 0], ax=[0, 0, 0], w=planeLength, lr=0.1, d=3, u=planeLength, v=1,
                                n=f'{self.side}_{BROW}_plane')[0]

        grp = cmds.group(em=True, n=f'{self.side}_follicle_{GROUP}')

        for i in range(len(listName)):
            y = str(i + 1)
            fol = cmds.createNode('follicle')
            fol = cmds.rename('follicle1', f'{self.side}_{BROW}_follicle_0{y}')

            cmds.parent(fol, grp, s=True)
            cmds.makeIdentity(plane, apply=True, t=1, r=1, s=1, n=0)

            cmds.connectAttr(f'{self.side}_{BROW}_follicle_Shape{y}.outRotate', f'{fol}.rotate', f=True)
            cmds.connectAttr(f'{self.side}_{BROW}_follicle_Shape{y}.outTranslate', f'{fol}.translate')
            cmds.connectAttr(f'{plane}Shape.worldMatrix', f'{self.side}_{BROW}_follicle_Shape{y}.inputWorldMatrix')
            cmds.connectAttr(f'{plane}Shape.local', f'{self.side}_{BROW}_follicle_Shape{y}.inputSurface')

            cmds.setAttr(f'{fol}.parameterV', 0.5)
            cmds.setAttr(f'{fol}.parameterU', 1/ (len(listName)))


    def create_eyebrow_jnts(self):
        jnts = []
        ctrl_jnts = []
        plane = f'{self.side}_{BROW}_plane'
        follicles = cmds.listRelatives(f'{self.side}_follicle_{GROUP}')
        for fol in follicles:
            y = len(follicles) + 1
            cmds.select(d=True)
            jnt = cmds.joint(n=f'joint_{y}')
            pc = cmds.parentConstraint(fol, jnt, mo=False)
            cmds.delete(pc)
            jnts.append(jnt)

        cmds.select(jnts, plane)
        cmds.SmoothBindSkin(tsb=True, cj=False)

        for num, jnt in enumerate(jnts):
            num += 1
            pc = cmds.parentConstraint(f'{self.side}_{BROW}_{GUIDE}_{num}', jnt, mo=False)
            cmds.delete(pc)

        cmds.select(f'{self.side}_{BROW}_plane')
        cmds.DeleteHistory()

        for num, jnt in enumerate(jnts):
            duplicate_jnt = cmds.duplicate(jnt)
            num += 1
            jnt = cmds.rename(jnt, f'{self.side}_{BROW}_skin_{JOINT}_0{num}')
            cmds.parent(jnt, f'{self.side}_{BROW}_follicle_0{num}')

            duplicate_jnt = cmds.rename(duplicate_jnt, f'{self.side}_{BROW}_{JOINT}_0{num}')
            ctrl_jnts.append(duplicate_jnt)

        ctrl_grp = cmds.group(empty=True, n=f'{self.side}_{BROW}_{GROUP}')
        cmds.parent(ctrl_jnts, ctrl_grp)
        cmds.group(plane, f'{self.side}_follicle_{GROUP}', n=f'{self.side}_{BROW}_{GROUP}_noTransform')

        cmds.select(ctrl_jnts, f'{self.side}_{BROW}_plane')
        cmds.SmoothBindSkin(tsb=True, cj=False)

