import maya.cmds as cmds

class guides:
    def __init__(self, side, name, number=5):
        self.side = side
        self.name = name
        self.number = number
        self.guides_grp = None

    def createRibbonGuides(self):
        self.guides_grp = cmds.createNode('transform', name=f'{self.side}_{self.name}_{GUIDE}_{GROUP}')

        for x in range(self.number):
            multiplier = x + 1 if self.side == 'L' else -(x + 1)
            loc = cmds.spaceLocator(name=f'{self.side}_{self.name}_{GUIDE}_{x + 1}')[0]
            cmds.setAttr(f'{loc}.tx', multiplier)
            cmds.parent(loc, self.guides_grp)

        cmds.select(cl=True)



