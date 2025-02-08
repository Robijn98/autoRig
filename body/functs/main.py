import sys
import maya.cmds as cmds
sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from cleanup_utils import root_setup
from cleanup_utils import hand_cleanup
from cleanup_utils import rev_foot_cleanup
from cleanup_utils import spine_cleanup
from cleanup_utils import cleanup_fullRig
import numpy as np

from spine_utils import IKFK_spine
from arm_utils import IKFK_arm
from leg_utils import IKFK_leg
from finger_utils import FK_fingers
from foot_utils import rev_foot
from general_functions import create_tempCtrl


sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\faceRig\\")

# from eye_utils import createEyeGuides
# from eye_utils import createMinorEyeJoints
# from eye_utils import eyeConnection
# from eyebrow_utils import createEyebrowGuides
# from eyebrow_utils import createEyeBrowJnts
# from eyebrow_utils import createEyebrowRibbon

#CONSTANTS
GROUP = 'GRP'
CONTROL = 'CTRL'
JOINT = 'JNT'
GUIDE = 'GUIDE'

LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'


# def attr_ctrl():
#     ctrl_grp, ctrl = create_tempCtrl(f'{CENTER}_attr_{CONTROL}', lock=['sx', 'sy', 'sz','rx', 'ry', 'rz', 'tx', 'ty', 'tz'])
#     cmds.addAttr(ctrl, ln='skeleton_vis', at='enum', en = "off:on", k=True, h=False)
#     cmds.addAttr(ctrl, ln='stretch_ctrls_vis', at='enum', en = "off:on", k=True, h=False)

#     cmds.connectAttr(f'{ctrl}.skeleton_vis', 'L_rev_GRP.visibility')
#     cmds.connectAttr(f'{ctrl}.skeleton_vis', 'R_rev_GRP.visibility')
#     cmds.connectAttr(f'{ctrl}.skeleton_vis', 'root_JNT.visibility')



#root_setup('root_JNT')


# FK_fingers('L_wrist_JNT',['L_thumb', 'L_index', 'L_middle', 'L_ring', 'L_pinky'])



# IKFK_spine(amountOfFKCtrls = 3, spineJoints = ['C_spine_00_JNT', 'C_spine_02_JNT', 'C_spine_03_JNT',
#                                                'C_spine_04_JNT', 'C_spine_05_JNT', 'C_spine_06_JNT'])


# IKFK_leg('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT', 'L_ball_JNT', 'L_toe_JNT', LEFT)
# IKFK_leg('R_hip_JNT', 'R_knee_JNT', 'R_ankle_JNT', 'R_ball_JNT','R_toe_JNT', RIGHT)

# IKFK_arm('R_shoulder_JNT', 'R_elbow_JNT', 'R_wrist_JNT', 'R_clav_JNT', RIGHT)
# IKFK_arm('L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT', 'L_clav_JNT', LEFT)


# FK_fingers('L_wrist_JNT',['L_thumb', 'L_index', 'L_middle', 'L_ring', 'L_pinky'])
# FK_fingers('R_wrist_JNT',['R_thumb', 'R_index', 'R_middle','R_ring', 'R_pinky'])

# rev_foot('L_knee_JNT','L_ankle_JNT','L_ball_JNT','L_toe_JNT','L_rev_CTRL_guide', LEFT)
# rev_foot('R_knee_JNT','R_ankle_JNT','R_ball_JNT','R_toe_JNT','R_rev_CTRL_guide', RIGHT)

# cleanup_fullRig()
# #leg_cleanup('R_hip_JNT', 'R_knee_JNT', 'R_ankle_JNT', RIGHT)
# #rev_foot_cleanup('R_ankle_JNT', RIGHT)

# #createEyeGuides('R', number=3)
# #createEyeGuides('L', number=3)


# #attr_ctrl()
# #cleanup_fullRig()
def main():
    cmds.polyCube()
    #root_setup('root_JNT')

