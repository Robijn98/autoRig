import sys
import maya.cmds as cmds

import importlib
sys.path.append('/home/s5725067/myRepos/autoRig/')
import rig_constants
importlib.reload(rig_constants)
from rig_constants import *


class cleanup:

    def __init__(self, hipJnt, kneeJnt, ankleJnt, shoulderJnt, elbowJnt, wristJnt, side, fingers = []):
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

        cmds.parent(self.hipJnt.replace(JOINT, f'FK_{JOINT}'), spineBase)
        cmds.parent(self.hipJnt.replace(JOINT, f'IK_{JOINT}'), f'skeleton_{GROUP}')

        # IK cleanup
        if cmds.objExists('pelvis_CTRL'):
            cmds.parentConstraint('pelvis_CTRL', self.hipJnt.replace(JOINT, f'IK_{JOINT}'), mo=True)
        else:
            raise Exception("Warning: no pelvis control exists.")

        cmds.parent(f'{self.side}_IK_ankle_GRP', 'offset_CTRL')
        cmds.parent(f'{self.side}_leg_pv_GRP', 'offset_CTRL')

        # FK
        grp = self.hipJnt.replace(JOINT, f'FK_{GROUP}')

        if cmds.objExists('pelvis_CTRL'):
            cmds.parent(grp, 'pelvis_CTRL')
        else:
            raise Exception("Warning: no pelvis control exists.")


    def arm_cleanup(self):
        cmds.select(self.shoulderJnt)
        clav = cmds.pickWalk(d='up')[0]

        cmds.parent(self.shoulderJnt.replace(JOINT, f'FK_{JOINT}'), clav)
        cmds.parent(self.shoulderJnt.replace(JOINT, f'IK_{JOINT}'), f'skeleton_{GROUP}')

        # IK cleanup
        if cmds.objExists(clav.replace(JOINT, CONTROL)):
            cmds.parentConstraint(clav.replace(JOINT, CONTROL), self.shoulderJnt.replace(JOINT, f'IK_{JOINT}'), mo=True)
        else:
            raise Exception("Warning: no clavicle control exists.")

        cmds.parent(f'{self.side}_IK_wrist_GRP', 'offset_CTRL')
        cmds.parent(f'{self.side}_arm_pv_GRP', 'offset_CTRL')

        # FK
        grp = self.shoulderJnt.replace(JOINT, f'FK_{GROUP}')

        if cmds.objExists(clav.replace(JOINT, CONTROL)):
            cmds.parent(grp, clav.replace(JOINT, CONTROL))
            if cmds.objExists('chest_CTRL'):
                cmds.parent(clav.replace(JOINT, GROUP), 'chest_CTRL')
        else:
            raise Exception("Warning: no clavicle control exists.")


    def hand_cleanup(self):
        mat = cmds.xform(self.wristJnt, q=True, m=True, ws=True)
        handLoc = cmds.spaceLocator(n=f'{self.side}_wrist_{GROUP}')
        cmds.xform(handLoc, m=mat, ws=True)

        for finger in self.fingers:
            fingerStart = f'{self.side}_{finger}_00_{GROUP}'
            cmds.parent(fingerStart, handLoc)

        cmds.parent(handLoc, f'master_{CONTROL}')
        cmds.parentConstraint(self.wristJnt, handLoc)

        cmds.parent(f'{self.side}_hand_{GROUP}', f'master_{CONTROL}')

        cmds.orientConstraint(f'{self.side}_IK_wrist_{CONTROL}', f'{self.side}_wrist_IK_{JOINT}', mo=True)


    def spine_cleanup(self):
        cmds.parent('spine_IK', f'dontTouch_{GROUP}')
        cmds.parent('spine_IK_curve', f'dontTouch_{GROUP}')
        cmds.parent('spine_FK_curve', f'dontTouch_{GROUP}')
        cmds.parent('body_GRP', f'root_{CONTROL}')

    def rev_foot_cleanup(self):
        offset = cmds.group(name = f'{self.side}_{REVERSE}_{GROUP}', empty=True)
        mat = cmds.xform(self.ankleJNT, q=True, m=True, ws=True)
        cmds.xform(offset, m=mat, ws=True)

        cmds.parent(f'{self.side}_innerbank_{REVERSE}_{JOINT}', offset)

        cmds.parentConstraint(f'{self.side}_IK_ankle_CTRL', offset, mo=True)

        cmds.parent(f'{self.side}_rev_{FOOT}_{GROUP}', f'{self.side}_IK_ankle_CTRL')
        cmds.parent(offset, f'dontTouch_{GROUP}')

        cmds.scaleConstraint('master_CTRL', offset, mo=True)


    def cleanup_full(self, spine = True, leg = True, arm = True, hand = True, rev_foot = True):
        if spine:
            self.spine_cleanup()
        if leg:
            self.leg_cleanup()
        if arm:
            self.arm_cleanup()
        if hand:
            self.hand_cleanup()
        if rev_foot:
            self.rev_foot_cleanup()





