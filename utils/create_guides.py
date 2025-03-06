import maya.cmds as cmds
import sys
import os
import importlib
import math 

sys.path.append('/home/s5725067/myRepos/autoRig/')
import rig_constants
importlib.reload(rig_constants)
from rig_constants import *


class guides:
    def __init__(self, side, name, number=5):
        self.side = side
        self.name = name
        self.number = number
        self.guides_grp = None

    def create_ribbon_guides(self):
        self.guides_grp = cmds.createNode('transform', name=f'{self.side}_{self.name}_{GUIDE}_{GROUP}')

        for x in range(self.number):
            multiplier = x + 1 if self.side == 'L' else -(x + 1)
            loc = cmds.spaceLocator(name=f'{self.side}_{self.name}_{GUIDE}_{x + 1}')[0]
            cmds.setAttr(f'{loc}.tx', multiplier)
            cmds.parent(loc, self.guides_grp)

        cmds.select(cl=True)


    def create_eye_guides(self, number =3):
        # creating groups to store guides
        eye_guide_grp = cmds.createNode('transform', name=f'{self.side}_{self.name}_{GUIDE}_{GROUP}')

        eyes_locs_grp = cmds.createNode('transform', name=f'{self.side}_{self.name}_minor_{GUIDE}_{GROUP}',
                                        parent=eye_guide_grp)

        # create locators
        for part in ['upper', 'lower']:

            part_mult = 1 if part == 'upper' else -1
            mid_data = (0, part_mult, 0)

            for x in range(number):
                multiplier = x + 1 if self.side == 'L' else -(x + 1)
                loc_data = (multiplier, part_mult, 0)
                loc = cmds.spaceLocator(name=f'{self.side}_{self.name}{part}_{x + 1}_{GUIDE}')[0]
                cmds.parent(loc, eyes_locs_grp)

                # set data
                cmds.setAttr(f'{loc}.t', *loc_data)

        # create corners
        left_corner_loc = cmds.spaceLocator(name=f'{self.side}_{LEFT}_{self.name}Corner_{GUIDE}')[0]
        right_corner_loc = cmds.spaceLocator(name=f'{self.side}_{RIGHT}_{self.name}Corner_{GUIDE}')[0]

        cmds.parent(left_corner_loc, eyes_locs_grp)
        cmds.parent(right_corner_loc, eyes_locs_grp)

        if self.side == 'L':
            cmds.setAttr(f'{left_corner_loc}.translateX', number + 1)
        else:
            cmds.setAttr(f'{right_corner_loc}.translateX', -(number + 1))

        cmds.select(cl=True)

        # create base
        eye_base_guide_grp = cmds.createNode('transform', name=f'{CENTER}_{self.name}_base_{GUIDE}_{GROUP}',
                                            parent=
                                            eye_guide_grp)
        eye_guide = cmds.spaceLocator(name=f'{self.side}_{CENTER}_{self.name}_{GUIDE}')[0]

        if self.side == 'L':
            cmds.setAttr(f'{eye_guide}.t', *(math.ceil(number / 2), 0, -number))
        else:
            cmds.setAttr(f'{eye_guide}.t', *(-math.ceil(number / 2), 0, -number))
        
        cmds.parent(eye_guide, eye_base_guide_grp)  
        

    def create_eyebrow_guides(self, number=4):
        eyebrow_guide_grp = cmds.createNode('transform', name=f'{self.side}_{self.name}_{GUIDE}_{GROUP}')

        for x in range(number):
            multiplier = x + 1 if self.side == 'L' else -(x + 1)
            loc = cmds.spaceLocator(name=f'{self.side}_{self.name}_{GUIDE}_{x + 1}')[0]
            cmds.setAttr(f'{loc}.tx', multiplier)
            cmds.parent(loc, eyebrow_guide_grp)

        cmds.select(cl=True)


    def create_lip_guides(self, number=5):
        # creating groups to store guides
        jaw_guide_grp = cmds.createNode('transform', name=f'{CENTER}_{self.name}_{GUIDE}_{GROUP}')
        locs_grp = cmds.createNode('transform', name=f'{CENTER}_{self.name}_lip_{GUIDE}_{GROUP}',
                                   parent=jaw_guide_grp)
        lips_locs_grp = cmds.createNode('transform', name=f'{CENTER}_{self.name}_lipMinor_{GUIDE}_{GROUP}',
                                       parent=locs_grp)

        # create locators
        for part in ['upper', 'lower']:

            part_mult = 1 if part == 'upper' else -1
            mid_data = (0, part_mult, 0)

            mid_loc = cmds.spaceLocator(name=f'{CENTER}_{self.name}{part}_lip_{GUIDE}')[0]
            cmds.parent(mid_loc, lips_locs_grp)

            for side in ['L', 'R']:
                for x in range(number):
                    multiplier = x + 1 if side == 'L' else -(x + 1)
                    loc_data = (multiplier, part_mult, 0)
                    loc = cmds.spaceLocator(name=f'{side}_{self.name}{part}_lip_{x + 1}_{GUIDE}')[0]
                    cmds.parent(loc, lips_locs_grp)

                    # set data
                    cmds.setAttr(f'{loc}.t', *loc_data)

            # set center data
            cmds.setAttr(f'{mid_loc}.t', *mid_data)

        # create corners
        left_corner_loc = cmds.spaceLocator(name=f'{LEFT}_{self.name}Corner_lip_{GUIDE}')[0]
        right_corner_loc = cmds.spaceLocator(name=f'{RIGHT}_{self.name}Corner_lip_{GUIDE}')[0]

        cmds.parent(left_corner_loc, lips_locs_grp)
        cmds.parent(right_corner_loc, lips_locs_grp)

        cmds.setAttr(f'{left_corner_loc}.translateX', number + 1)
        cmds.setAttr(f'{right_corner_loc}.translateX', -(number + 1))

        cmds.select(cl=True)

        # create jaw_base
        jaw_base_guide_grp = cmds.createNode('transform', name=f'{CENTER}_{self.name}_base_{GUIDE}_{GROUP}',
                                           parent=jaw_guide_grp)
        jaw_guide = cmds.spaceLocator(name=f'{CENTER}_{self.name}_{GUIDE}')[0]
        jaw_inverse_guide = cmds.spaceLocator

        cmds.setAttr(f'{jaw_guide}.t', *(0, -1, -number))
        cmds.setAttr(f'{jaw_inverse_guide}.t', *(0, 1, -number))

        cmds.parent(jaw_guide, jaw_base_guide_grp)
        cmds.parent(jaw_inverse_guide, jaw_base_guide_grp)

        cmds.select(cl=True)