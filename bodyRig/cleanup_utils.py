import sys
import maya.cmds as cmds

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import create_tempCtrl

GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'
ROOT = 'root'

#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'

def root_setup(rootJoint = ''):
    masterGrp, masterCtrl = create_tempCtrl(f'master_{CONTROL}', lock = ['sx', 'sy', 'sz', 'v'])

    skelGrp = cmds.group(n = f'skeleton_{GROUP}', empty= True)
    dontTouchGrp = cmds.group(n = f'dontTouch_{GROUP}', empty= True)

    cmds.parent(skelGrp, masterCtrl)
    cmds.parent(dontTouchGrp, masterGrp)
    cmds.parent(rootJoint, skelGrp)

    offsetGrp, offsetCtrl = create_tempCtrl(f'offset_{CONTROL}', lock = ['sx', 'sy', 'sz', 'v'])
    rootGrp, rootCtrl = create_tempCtrl(f'root_{CONTROL}', lock = ['sx', 'sy', 'sz', 'v'])

    cmds.parent(offsetGrp, masterCtrl)
    cmds.parent(rootGrp, offsetCtrl)


def leg_cleanup(hipJnt, kneeJnt, ankleJnt, side):
    cmds.select(hipJnt)
    spineBase = cmds.pickWalk(d='up')[0]

    cmds.parent(hipJnt.replace(JOINT, f'FK_{JOINT}'), spineBase)
    cmds.parent(hipJnt.replace(JOINT, f'IK_{JOINT}'), f'skeleton_{GROUP}')

    # IK cleanup
    if cmds.objExists('pelvis_CTRL'):
        cmds.parentConstraint('pelvis_CTRL', hipJnt.replace(JOINT, f'IK_{JOINT}'), mo=True)
    else:
        raise Exception("Warning: no pelvis control exists.")

    cmds.parent(f'{side}_IK_ankle_GRP', 'offset_CTRL')
    cmds.parent(f'{side}_leg_pv_GRP', 'offset_CTRL')

    # FK
    grp = hipJnt.replace(JOINT, f'FK_{GROUP}')

    if cmds.objExists('pelvis_CTRL'):
        cmds.parent(grp, 'pelvis_CTRL')
    else:
        raise Exception("Warning: no pelvis control exists.")


def arm_cleanup(shoulderJnt, elbowJnt, wristJnt, side):
    cmds.select(shoulderJnt)
    clav = cmds.pickWalk(d='up')[0]

    cmds.parent(shoulderJnt.replace(JOINT, f'FK_{JOINT}'), clav)
    cmds.parent(shoulderJnt.replace(JOINT, f'IK_{JOINT}'), f'skeleton_{GROUP}')

    # IK cleanup
    if cmds.objExists(clav.replace(JOINT, CONTROL)):
        cmds.parentConstraint(clav.replace(JOINT, CONTROL), shoulderJnt.replace(JOINT, f'IK_{JOINT}'), mo=True)
    else:
        raise Exception("Warning: no clavicle control exists.")

    cmds.parent(f'{side}_IK_wrist_GRP', 'offset_CTRL')
    cmds.parent(f'{side}_arm_pv_GRP', 'offset_CTRL')

    # FK
    grp = shoulderJnt.replace(JOINT, f'FK_{GROUP}')

    if cmds.objExists(clav.replace(JOINT, CONTROL)):
        cmds.parent(grp, clav.replace(JOINT, CONTROL))
        if cmds.objExists('chest_CTRL'):
            cmds.parent(clav.replace(JOINT, GROUP), 'chest_CTRL')
    else:
        raise Exception("Warning: no clavicle control exists.")


def hand_cleanup(wristJnt, side, fingers=[]):
    mat = cmds.xform(wristJnt, q=True, m=True, ws=True)
    handLoc = cmds.spaceLocator(n=f'{side}_wrist_{GROUP}')
    cmds.xform(handLoc, m=mat, ws=True)

    for finger in fingers:
        fingerStart = f'{side}_{finger}_00_{GROUP}'
        cmds.parent(fingerStart, handLoc)

    cmds.parent(handLoc, f'master_{CONTROL}')
    cmds.parentConstraint(wristJnt, handLoc)

    cmds.parent(f'{side}_hand_{GROUP}', f'master_{CONTROL}')

    cmds.orientConstraint(f'{side}_IK_wrist_{CONTROL}', f'{side}_wrist_IK_{JOINT}', mo=True)


def spine_cleanup():
    cmds.parent('spine_IK', f'dontTouch_{GROUP}')
    cmds.parent('spine_IK_curve', f'dontTouch_{GROUP}')
    cmds.parent('spine_FK_curve', f'dontTouch_{GROUP}')
    cmds.parent('body_GRP', f'root_{CONTROL}')


def cleanup_fullRig():
    leg_cleanup('R_hip_JNT', 'R_knee_JNT', 'R_ankle_JNT', RIGHT)
    leg_cleanup('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT', LEFT)

    arm_cleanup('L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT', LEFT)
    arm_cleanup('R_shoulder_JNT', 'R_elbow_JNT', 'R_wrist_JNT', RIGHT)

    hand_cleanup('L_wrist_JNT', LEFT, fingers=['thumb', 'index', 'middle', 'ring', 'pinky'])
    hand_cleanup('R_wrist_JNT',RIGHT, fingers=['thumb','index', 'middle', 'ring', 'pinky'])

    spine_cleanup()



#EXECUTE
#root_setup('root')


