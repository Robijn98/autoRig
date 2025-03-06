import cmds.maya as cmds

sys.path.append('/home/s5725067/myRepos/autoRig/')
import rig_constants
importlib.reload(rig_constants)
from rig_constants import *

"""

This script creates joints on a curve. The curve is rebuilded to have the same number of spans as the number of joints.
It is inspired by the script from the class creating a quadruped rig for production by Paween Sarachan 

"""


class joints_to_curves:
    def __init__(self, curve, prefix, num_joints, span):
        self.curve = curve
        self.prefix = prefix
        self.num_joints = num_joints
        self.span = span


    def joints_on_curves(self):
        
        cmds.rebuildcurve(self.curve, ch=True, rpo=True, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=self.span, d=3)
        length = cmds.arclen(self.curve, ch=False)
        jnt_IK = []
        
        for i in range(self.num_joints + 1):
            jtmp = cmds.joint(p=(length/self.num_joints * (i + 1), 0, 0), n=f"{self.prefix}_{i}_IK_{JOINT}")
            jnt_IK.append(jtmp)
        
        spineIkh = cmds.ikHandle(sj=jnt_IK[0], ee=jnt_IK[-1], c=self.curve, ccv=False, sol= "ikSplinSolver", pcv=False, n=f"{self.prefix}_IK_{JOINT}")
        cmds.delete(spineIkh[1])
        cmds.makeIdentity(jnt_IK, apply=True, t=1, r=1, n=0, pn=1)
        cmds.joint(jnt_IK[0], e=True, oj='xyz', sao='yup', ch=True, zso=True)

