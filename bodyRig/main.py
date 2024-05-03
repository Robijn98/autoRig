import sys

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from cleanup_utils import root_setup
from cleanup_utils import cleanup_fullRig
from spine_utils import IKFK_spine
from arm_utils import IKFK_arm


from leg_utils import IKFK_leg
from finger_utils import FK_fingers

from foot_utils import rev_foot



LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'



root_setup('root_JNT')

IKFK_spine(amountOfFKCtrls = 4, spineJoints = ['C_spine_01_JNT', 'C_spine_02_JNT', 'C_spine_03_JNT',
                                               'C_spine_04_JNT', 'C_spine_05_JNT', 'C_spine_06_JNT'])

IKFK_leg('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT', 'L_ball_JNT', 'L_toe_JNT', LEFT)
IKFK_leg('R_hip_JNT', 'R_knee_JNT', 'R_ankle_JNT', 'R_ball_JNT','R_toe_JNT', RIGHT)

IKFK_arm('R_shoulder_JNT', 'R_elbow_JNT', 'R_wrist_JNT', 'R_clav_JNT', RIGHT)
IKFK_arm('L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT', 'L_clav_JNT', LEFT)


FK_fingers('L_wrist_JNT',['L_thumb', 'L_index', 'L_middle', 'L_ring', 'L_pinky'])
FK_fingers('R_wrist_JNT',['R_thumb', 'R_index', 'R_middle','R_ring', 'R_pinky'])

rev_foot('L_knee_JNT','L_ankle_JNT','L_ball_JNT','L_toe_JNT','L_rev_CTRL_guide', LEFT)
rev_foot('R_knee_JNT','R_ankle_JNT','R_ball_JNT','R_toe_JNT','R_rev_CTRL_guide', RIGHT)



cleanup_fullRig()

