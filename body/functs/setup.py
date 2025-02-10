import sys
import maya.cmds as cmds
from general_functions import create_tempCtrl

class setup:

    GROUP = 'GRP'
    CONTROL = 'CTRL'
    JOINT = 'JNT'
    GUIDE = 'GUIDE'
    ROOT = 'root'
    CENTER = 'C'

    def __init__(self, rootJnt):
        self.rootJnt = rootJnt

    def root_setup(self):
        masterGrp, masterCtrl = create_tempCtrl(f'master_{self.CONTROL}', lock = ['v'])

        skelGrp = cmds.group(n = f'skeleton_{self.GROUP}', empty= True)
        dontTouchGrp = cmds.group(n = f'dontTouch_{self.GROUP}', empty= True)

        cmds.parent(skelGrp, masterCtrl)
        cmds.parent(dontTouchGrp, masterGrp)
        cmds.parent(self.rootJnt, skelGrp)

        offsetGrp, offsetCtrl = create_tempCtrl(f'offset_{self.CONTROL}', lock = ['sx', 'sy', 'sz', 'v'])
        rootGrp, rootCtrl = create_tempCtrl(f'root_{self.CONTROL}', lock = ['sx', 'sy', 'sz', 'v'])

        cmds.parent(offsetGrp, masterCtrl)
        cmds.parent(rootGrp, offsetCtrl)


