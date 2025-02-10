import sys
import maya.cmds as cmds
from general_functions import create_tempCtrl

class cleanup:

    GROUP = 'GRP'
    CONTROL = 'CTRL'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    ROOT = 'root'
    FOOT = 'foot'
    REVERSE = 'rev'
    LEG = 'leg'
    LEFT = 'L'
    RIGHT = 'R'
    CENTER = 'C'

    def __init__(self, hipJnt, kneeJnt, ankleJnt, shoulderJnt, elbowJnt, wristJnt, fingers = [], side):
        self.hipJnt = hipJnt
        self.kneeJnt = kneeJnt
        self.ankleJnt = ankleJnt
        self.shoulderJnt = shoulderJnt
        self.elbowJnt = elbowJnt
        self.wristJnt = wristJnt
        self.fingers = fingers
        self.side = side

    

    def leg_cleanup(self):
        cmds.select(self.hipJnt)
        spineBase = cmds.pickWalk(d='up')[0]

        cmds.parent(self.hipJnt.replace(self.JOINT, f'FK_{self.JOINT}'), spineBase)
        cmds.parent(self.hipJnt.replace(self.JOINT, f'IK_{self.JOINT}'), f'skeleton_{self.GROUP}')

        # IK cleanup
        if cmds.objExists('pelvis_CTRL'):
            cmds.parentConstraint('pelvis_CTRL', self.hipJnt.replace(self.JOINT, f'IK_{self.JOINT}'), mo=True)
        else:
            raise Exception("Warning: no pelvis control exists.")

        cmds.parent(f'{self.side}_IK_ankle_GRP', 'offset_CTRL')
        cmds.parent(f'{self.side}_leg_pv_GRP', 'offset_CTRL')

        # FK
        grp = self.hipJnt.replace(self.JOINT, f'FK_{self.GROUP}')

        if cmds.objExists('pelvis_CTRL'):
            cmds.parent(grp, 'pelvis_CTRL')
        else:
            raise Exception("Warning: no pelvis control exists.")


    def arm_cleanup(self):
        cmds.select(self.shoulderJnt)
        clav = cmds.pickWalk(d='up')[0]

        cmds.parent(self.shoulderJnt.replace(self.JOINT, f'FK_{self.JOINT}'), clav)
        cmds.parent(self.shoulderJnt.replace(self.JOINT, f'IK_{self.JOINT}'), f'skeleton_{self.GROUP}')

        # IK cleanup
        if cmds.objExists(clav.replace(self.JOINT, self.CONTROL)):
            cmds.parentConstraint(clav.replace(self.JOINT, self.CONTROL), self.shoulderJnt.replace(self.JOINT, f'IK_{self.JOINT}'), mo=True)
        else:
            raise Exception("Warning: no clavicle control exists.")

        cmds.parent(f'{self.side}_IK_wrist_GRP', 'offset_CTRL')
        cmds.parent(f'{self.side}_arm_pv_GRP', 'offset_CTRL')

        # FK
        grp = self.shoulderJnt.replace(self.JOINT, f'FK_{self.GROUP}')

        if cmds.objExists(clav.replace(self.JOINT, self.CONTROL)):
            cmds.parent(grp, clav.replace(self.JOINT, self.CONTROL))
            if cmds.objExists('chest_CTRL'):
                cmds.parent(clav.replace(self.JOINT, self.GROUP), 'chest_CTRL')
        else:
            raise Exception("Warning: no clavicle control exists.")


    def hand_cleanup(self):
        mat = cmds.xform(self.wristJnt, q=True, m=True, ws=True)
        handLoc = cmds.spaceLocator(n=f'{self.side}_wrist_{self.GROUP}')
        cmds.xform(handLoc, m=mat, ws=True)

        for finger in self.fingers:
            fingerStart = f'{self.side}_{finger}_00_{self.GROUP}'
            cmds.parent(fingerStart, handLoc)

        cmds.parent(handLoc, f'master_{self.CONTROL}')
        cmds.parentConstraint(self.wristJnt, handLoc)

        cmds.parent(f'{self.side}_hand_{self.GROUP}', f'master_{self.CONTROL}')

        cmds.orientConstraint(f'{self.side}_IK_wrist_{self.CONTROL}', f'{self.side}_wrist_IK_{self.JOINT}', mo=True)


    def spine_cleanup(self):
        cmds.parent('spine_IK', f'dontTouch_{self.GROUP}')
        cmds.parent('spine_IK_curve', f'dontTouch_{self.GROUP}')
        cmds.parent('spine_FK_curve', f'dontTouch_{self.GROUP}')
        cmds.parent('body_GRP', f'root_{self.CONTROL}')

    def rev_foot_cleanup(self):
        offset = cmds.group(name = f'{self.side}_{self.REVERSE}_{self.GROUP}', empty=True)
        mat = cmds.xform(self.ankleJNT, q=True, m=True, ws=True)
        cmds.xform(offset, m=mat, ws=True)

        cmds.parent(f'{self.side}_innerbank_{self.REVERSE}_{self.JOINT}', offset)

        cmds.parentConstraint(f'{self.side}_IK_ankle_CTRL', offset, mo=True)

        cmds.parent(f'{self.side}_rev_{self.FOOT}_{self.GROUP}', f'{self.side}_IK_ankle_CTRL')
        cmds.parent(offset, f'dontTouch_{self.GROUP}')

        cmds.scaleConstraint('master_CTRL', offset, mo=True)


    def cleanup_full(self)
        leg_cleanup()
        arm_cleanup()
        hand_cleanup()
        rev_foot_cleanup()
        spine_cleanup()





