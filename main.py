import sys
import maya.cmds as cmds
import importlib

sys.path.append('/home/s5725067/myRepos/autoRig/')
import rig_constants
importlib.reload(rig_constants)
from rig_constants import *

sys.path.append('/home/s5725067/myRepos/autoRig/body/')
try:
    import rig_setup
    importlib.reload(rig_setup)
    from rig_setup import setup
    print("imported rig_setup successfully")
except ImportError:
    print("Error importing rig_setup")

#body import
try:
    import rig_spine
    importlib.reload(rig_spine)
    from rig_spine import IKFK_spine
    print("imported spine_rig successfully")
except ImportError:
    print("Error importing spine_rig")

try:
    import rig_leg
    importlib.reload(rig_leg)
    from rig_leg import IKFK_leg
    print("imported leg_rig successfully")
except ImportError:
    print("Error importing leg_rig")

try:
    import rig_arm
    importlib.reload(rig_arm)
    from rig_arm import IKFK_arm
    print("imported arm_rig successfully")
except ImportError:
    print("Error importing arm_rig")

#cleanup
try:
    import rig_cleanup
    importlib.reload(rig_cleanup)
    from rig_cleanup import cleanup
    print("imported cleanup successfully")
except ImportError:
    print("Error importing cleanup")

#from cleanup import cleanup
# from cleanup import hand_cleanup
# from cleanup import rev_foot_cleanup
# from cleanup import spine_cleanup
# from cleanup import cleanup_fullRig
# import numpy as np

#from spine_rig import IKFK_spine
# from spine_utils import IKFK_spine
# from arm_utils import IKFK_arm
# from leg_utils import IKFK_leg
# from finger_utils import FK_fingers
# from foot_utils import rev_foot
# from controller import create_temp_ctrl


# from eye_utils import createEyeGuides
# from eye_utils import createMinorEyeJoints
# from eye_utils import eyeConnection
# from eyebrow_utils import createEyebrowGuides
# from eyebrow_utils import createEyeBrowJnts
# from eyebrow_utils import createEyebrowRibbon


# def attr_ctrl():
#     ctrl_grp, ctrl = create_temp_ctrl(f'{CENTER}_attr_{CONTROL}', lock=['sx', 'sy', 'sz','rx', 'ry', 'rz', 'tx', 'ty', 'tz'])
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
    print("Running main")
    try:
        my_setup = setup('root_JNT')
        my_setup.root_setup()
    except Exception as e:
        print(f"Error during setup: {e}")

    try:
        spine = IKFK_spine(['spineA_JNT', 'spineB_JNT', 'spineC_JNT', 'spineD_JNT', 'spineE_JNT', 'spineF_JNT', 'spineG_JNT'])
        
        spine.spine()
    except Exception as e:
        print(f"Error during spine setup: {e}")

    try:
        leg = IKFK_leg('L_hip_JNT', 'L_knee_JNT', 'L_ankle_JNT', 'L_ball_JNT', 'L_toe_JNT', LEFT)
        leg.leg()
        print("Left leg setup complete")
        leg = IKFK_leg('R_hip_JNT', 'R_knee_JNT', 'R_ankle_JNT', 'R_ball_JNT','R_toe_JNT', RIGHT)
        leg.leg()
        print("Right leg setup complete")
    except Exception as e:
        print(f"Error during leg setup: {e}")

    try:
        arm = IKFK_arm('R_shoulder_JNT', 'R_elbow_JNT', 'R_wrist_JNT', 'R_clav_JNT', RIGHT)
        arm.arm()
        print("Right arm setup complete")
        arm = IKFK_arm('L_shoulder_JNT', 'L_elbow_JNT', 'L_wrist_JNT', 'L_clav_JNT', LEFT)
        arm.arm()
        print("Left arm setup complete")
    except Exception as e:
        print(f"Error during arm setup: {e}")

    try:
        rig_clean = cleanup("L_hip_JNT", "L_knee_JNT", "L_ankle_JNT", "L_shoulder_JNT", "L_elbow_JNT", "L_wrist_JNT", LEFT, fingers = [])
        rig_clean.cleanup_full(spine = True, leg=True, arm=True, hand = False, rev_foot = False)
        rig_clean = cleanup("R_hip_JNT", "R_knee_JNT", "R_ankle_JNT", "R_shoulder_JNT", "R_elbow_JNT", "R_wrist_JNT", RIGHT, fingers = [])
        rig_clean.cleanup_full(spine = False, hand = False, rev_foot = False)
    except Exception as e:
        print(f"Error during cleanup: {e}")


