import math
import maya.cmds as cmds
import sys

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import create_tempCtrl

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import addOffset




GROUP = 'GRP'
JOINT = 'JNT'
GUIDE = 'GUIDE'
CONTROL = 'CTRL'

#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'


def createRibbonGuides(side, name, number=5):
    guides_grp = cmds.createNode('transform', name=f'{side}_{name}_{GUIDE}_{GROUP}')

    for x in range(number):
        multiplier = x + 1 if side == 'L' else -(x + 1)
        loc = cmds.spaceLocator(name=f'{side}_{name}_{GUIDE}_{x + 1}')[0]
        cmds.setAttr(f'{loc}.tx', multiplier)
        cmds.parent(loc, guides_grp)

    cmds.select(cl=True)

def return_guides(side, name):
    guide_grp = f'{side}_{name}_{GUIDE}_{GROUP}'
    guides = []

    if cmds.objExists(guide_grp):
        for loc in cmds.listRelatives(guide_grp, c=True):
            guides.append(loc)

    return guides


def createRibbon(side, name):
    guides = return_guides(side, name)
    guideAmount = len(guides)-1

    dist = cmds.createNode('distanceBetween')
    cmds.connectAttr(f'{guides[0]}.translate', f'{dist}.point1')
    cmds.connectAttr(f'{guides[-1]}.translate', f'{dist}.point2')
    distance = cmds.getAttr(f'{dist}.distance')


    plane = cmds.nurbsPlane(p=[0, 0, 0], ax=[0, 1, 0], w=distance, lr=0.1, d=3, u=guideAmount, v=1,
                            n=f'{side}_{name}_plane')[0]

    grp = cmds.group(em=True, n=f'{side}_{name}_follicle_{GROUP}')

    parameterU = 0
    changeDistance = 1/(guideAmount)
    for i in range(len(guides)):
        y = str(i + 1)
        fol = cmds.createNode('follicle')
        fol = cmds.rename('follicle1', f'{side}_{name}_follicle_0{y}')

        cmds.parent(fol, grp, s=True)
        cmds.makeIdentity(plane, apply=True, t=1, r=1, s=1, n=0)

        cmds.connectAttr(f'{side}_{name}_follicle_Shape{y}.outRotate', f'{fol}.rotate', f=True)
        cmds.connectAttr(f'{side}_{name}_follicle_Shape{y}.outTranslate', f'{fol}.translate')
        cmds.connectAttr(f'{plane}Shape.worldMatrix', f'{side}_{name}_follicle_Shape{y}.inputWorldMatrix')
        cmds.connectAttr(f'{plane}Shape.local', f'{side}_{name}_follicle_Shape{y}.inputSurface')

        cmds.setAttr(f'{fol}.parameterV', 0.5)
        cmds.setAttr(f'{fol}.parameterU', parameterU)
        parameterU += changeDistance

        # shape ribbon to guides


def createRibbonJnts(side, name):

    jnts = []
    ctrl_jnts = []
    plane = f'{side}_{name}_plane'
    follicles = cmds.listRelatives(f'{side}_{name}_follicle_{GROUP}')
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
    print(jnts)

    for num, jnt in enumerate(jnts):
        num += 1
        if jnt == jnts[-1]:
            print(num)
            pc = cmds.parentConstraint(f'{side}_{name}_{GUIDE}_{num}', jnt, mo=False)
            cmds.delete(pc)
        else:
            pc = cmds.parentConstraint(f'{side}_{name}_{GUIDE}_{num}', jnt, mo=False)
            cmds.delete(pc)

    cmds.select(f'{side}_{name}_plane')
    cmds.DeleteHistory()
    

    for num, jnt in enumerate(jnts):
        duplicate_jnt = cmds.duplicate(jnt)
        num += 1
        jnt = cmds.rename(jnt, f'{side}_{name}_skin_{JOINT}_0{num}')
        cmds.parent(jnt, f'{side}_{name}_follicle_0{num}')

        duplicate_jnt = cmds.rename(duplicate_jnt, f'{side}_{name}_{JOINT}_0{num}')
        ctrl_jnts.append(duplicate_jnt)

    ctrl_grp = cmds.group(empty=True, n=f'{side}_{name}_{GROUP}')
    cmds.parent(ctrl_jnts, ctrl_grp)
    cmds.group(plane, f'{side}_{name}_follicle_{GROUP}', n=f'{side}_{name}_{GROUP}_noTransform')

    cmds.select(ctrl_jnts, f'{side}_{name}_plane')
    #fix this to specific values so it doesnt get fucked if the settings change, thank you
    cmds.SmoothBindSkin(tsb=True, cj=False)



def createRibbonCtrls(side, name):
    #control creation
    ctrl_amount = len(return_guides(side, name))

    mainJnts = [f'{side}_{name}_{JOINT}_0{1}', f'{side}_{name}_{JOINT}_0{math.ceil(ctrl_amount/2)}', f'{side}_{name}_{JOINT}_0{ctrl_amount}']

    num = 0
    for i in range(ctrl_amount):
        num += 1
        jnt = f'{side}_{name}_{JOINT}_0{num}'
        ctrl_grp, ctrl = create_tempCtrl(f'{side}_{name}_0{num}_{CONTROL}', lock=[])
        mat = cmds.xform(jnt, q=True, m=True, ws=True)
        cmds.xform(ctrl_grp, m=mat, ws=True)
        if jnt not in mainJnts:
            addOffset(ctrl)

        cmds.parent(jnt, ctrl)


    upperLoc = cmds.spaceLocator(n = f'{side}_{name}_upperAimLoc')
    lowerLoc = cmds.spaceLocator(n = f'{side}_{name}_lowerAimLoc')

    mat = cmds.xform(f'{side}_{name}_01_{CONTROL}', q=True, m=True, ws=True)
    cmds.xform(upperLoc, m=mat, ws=True)
    cmds.parent(upperLoc, f'{side}_{name}_01_{CONTROL}')

    mat = cmds.xform(f'{side}_{name}_0{math.ceil(ctrl_amount/2)}_{CONTROL}', q=True, m=True, ws=True)
    cmds.xform(lowerLoc, m=mat, ws=True)
    cmds.parent(lowerLoc, f'{side}_{name}_0{math.ceil(ctrl_amount/2)}_{CONTROL}')

    cmds.delete(f'{side}_{name}_{GROUP}')


def connectRibbonToJoints(side, name, joints = []):
    ctrl_amount = len(return_guides(side, name))

    mainCtrls = [f'{side}_{name}_0{1}_{CONTROL}', f'{side}_{name}_0{math.ceil(ctrl_amount/2)}_{CONTROL}', f'{side}_{name}_0{ctrl_amount}_{CONTROL}']

    ctrls_upperLimb = []
    ctrls_lowerLimb = []

    mid_jnt = math.ceil(ctrl_amount / 2)

    for num, ctrl in enumerate(mainCtrls):
        offset = addOffset(ctrl)
        cmds.parentConstraint(joints[num], offset, mo=True)



    for num in range(1, ctrl_amount):

        if num<mid_jnt:
            ctrls_upperLimb.append(f'{side}_{name}_0{num}_{CONTROL}')

        if num>mid_jnt:
            ctrls_lowerLimb.append(f'{side}_{name}_0{num}_{CONTROL}')


    for ctrl in ctrls_upperLimb:
        if ctrl not in mainCtrls:
            cmds.pointConstraint(mainCtrls[0], f'{ctrl}_OFF', mo=True)
            cmds.pointConstraint(mainCtrls[1], f'{ctrl}_OFF', mo=True)
            cmds.aimConstraint(mainCtrls[0],f'{ctrl}_OFF', wut = 'objectrotation', wuo = f'{side}_{name}_upperAimLoc', mo=True)

    for ctrl in ctrls_lowerLimb:
        if ctrl not in mainCtrls:
            cmds.pointConstraint(mainCtrls[1], f'{ctrl}_OFF', mo=True)
            cmds.pointConstraint(mainCtrls[2], f'{ctrl}_OFF', mo=True)
            cmds.aimConstraint(mainCtrls[1], f'{ctrl}_OFF', wut = 'objectrotation', wuo = f'{side}_{name}_lowerAimLoc',u = [0, -1, 0], mo=True)


    stretchGroup = cmds.group(empty=True, n=f'{side}_{name}_stretch')

    for ctrl in range(ctrl_amount):
        cmds.parent(f'{side}_{name}_0{ctrl+1}_{GROUP}', stretchGroup)


def createRibbonLimb(side, name, joints = []):
    createRibbon(side, name)
    createRibbonJnts(side, name)
    createRibbonCtrls(side, name)
    connectRibbonToJoints(side, name, joints)

#createRibbonGuides('L', 'leg')
createRibbon('L', 'leg')
createRibbonJnts('L', 'leg')
createRibbonCtrls('L', 'leg')
connectRibbonToJoints('L', 'leg', joints = ['L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT'])

#createRibbonLimb('L', 'arm', joints = ['L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT'])
