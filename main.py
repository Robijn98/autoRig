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

try:
    import rig_hand
    importlib.reload(rig_hand)
    from rig_hand import hand
    print("imported hand_rig successfully")
except ImportError:
    print("Error importing hand_rig")


try: 
    import rig_foot
    importlib.reload(rig_foot)
    from rig_foot import foot
    print("imported foot_rig successfully")
except ImportError:
    print("Error importing foot_rig")


#cleanup
try:
    import rig_cleanup
    importlib.reload(rig_cleanup)
    from rig_cleanup import cleanup
    print("imported cleanup successfully")
except ImportError:
    print("Error importing cleanup")


#face
sys.path.append('/home/s5725067/myRepos/autoRig/utils/')
try:
    import create_guides
    importlib.reload(create_guides)
    from create_guides import guides
except ImportError:
    print("Error importing create_guides")

try:
    import rig_eye
    importlib.reload(rig_eye)
    from rig_eye import eye
    print("imported eye_rig successfully") 
except ImportError:
    print("Error importing eye_rig")




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



# rev_foot('L_knee_JNT','L_ankle_JNT','L_ball_JNT','L_toe_JNT','L_rev_CTRL_guide', LEFT)
# rev_foot('R_knee_JNT','R_ankle_JNT','R_ball_JNT','R_toe_JNT','R_rev_CTRL_guide', RIGHT)

# #createEyeGuides('R', number=3)
# #createEyeGuides('L', number=3)


# #attr_ctrl()


def main():
    # print("reopening file")
    # current_file = cmds.file(q=True, sn=True)
    # if current_file:
    #     cmds.file(current_file, o=True, f=True)
    # else:
    #     print("No file to open")

        
    # print("Running main")

    # try:
    #     eye_guides = guides('R', 'eye')
    #     eye_guides.create_eye_guides()
    #     eye_guides = guides('L', 'eye')
    #     eye_guides.create_eye_guides()
    # except Exception as e:
    #     print(f"Error creating eye guides: {e}")
        
    
    try:
        my_setup = setup("root_JNT")
        my_setup.root_setup()
    except Exception as e:
        print(f"Error during setup: {e}")


    try:
        spine = IKFK_spine(['spineA_JNT', 'spineB_JNT', 'spineC_JNT', 'spineD_JNT', 'spineE_JNT', 'spineF_JNT'])
        
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
        foot_rig = foot('L_ankle_JNT', 'L_ball_JNT', 'L_toe_JNT', LEFT)
        foot_rig.rev_foot("L_rev_CTRL_guide")
        print("Left foot setup complete")
        foot_rig = foot('R_ankle_JNT', 'R_ball_JNT', 'R_toe_JNT', RIGHT)
        foot_rig.rev_foot("R_rev_CTRL_guide")
        print("Right foot setup complete")
    except Exception as e:
        print(f"Error during foot setup: {e}")


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
        fingers = hand('R_wrist_JNT',['R_thumb', 'R_index', 'R_middle','R_pinky'])
        fingers.fingers_rig()
        print("Right fingers setup complete")
        fingers = hand('L_wrist_JNT',['L_thumb', 'L_index', 'L_middle','L_pinky'])
        fingers.fingers_rig()
        print("Left fingers setup complete")
    except Exception as e:
        print(f"Error during finger setup: {e}")

    try:
        rig_clean = cleanup("L_hip_JNT", "L_knee_JNT", "L_ankle_JNT", "L_shoulder_JNT", "L_elbow_JNT", "L_wrist_JNT", LEFT, fingers = ['thumb', 'index', 'middle',  'pinky'])
        rig_clean.cleanup_full(spine = True, leg=True, arm=True, hand = True, rev_foot = True)
        rig_clean = cleanup("R_hip_JNT", "R_knee_JNT", "R_ankle_JNT", "R_shoulder_JNT", "R_elbow_JNT", "R_wrist_JNT", RIGHT, fingers = ['thumb', 'index', 'middle', 'pinky'])
        rig_clean.cleanup_full(spine = False, hand = True, rev_foot = True)
        print("Cleanup complete")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        
