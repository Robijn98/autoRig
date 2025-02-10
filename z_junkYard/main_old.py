cmds.rename('master_ctrl|skeleton_grp', 'skeleton_grp_IK')
cmds.parent('skeleton_grp', 'master_ctrl')
#cmds.parent('IK_grp', 'master_ctrl')
cmds.parent('C_attr_ctrl_grp', 'master_ctrl')

cmds.setAttr('master_ctrl.scaleX', k =True)
cmds.setAttr('master_ctrl.scaleY', k =True)
cmds.setAttr('master_ctrl.scaleZ', k =True)

cmds.setAttr('master_ctrl.scaleX', lock =False)
cmds.setAttr('master_ctrl.scaleY', lock =False)
cmds.setAttr('master_ctrl.scaleZ', lock =False)

if cmds.objExists('deltaMush1'):
    cmds.connectAttr('master_ctrl.scale','deltaMush1.scale')

if cmds.objExists('deltaMush2'):
    cmds.connectAttr('master_ctrl.scale','deltaMush2.scale')

if cmds.objExists('deltaMush3'):
    cmds.connectAttr('master_ctrl.scale','deltaMush3.scale')





#Blaster
cmds.setAttr('DC15A_blasterRifle_grp.tz', -0.947)
cmds.makeIdentity('DC15A_blasterRifle_grp', apply=True)
cmds.joint(n = 'gun_jnt', p = (0.876926, 8.10586, -18.529232))
cmds.parentConstraint('gun_jnt', 'DC15A_blasterRifle_geo', mo=True)
cmds.parentConstraint('gun_jnt', 'DC15s_blaster_geo', mo=True)
cmds.scaleConstraint('gun_jnt', 'DC15A_blasterRifle_geo', mo=True)
cmds.scaleConstraint('gun_jnt', 'DC15s_blaster_geo', mo=True)




#after ctrl creation
cmds.addAttr('gun_jnt_ctrl', ln = 'spaceSwitch', at='enum', en= "world:leftHand:rightHand:chest:hips:", k=True)

L_hand_pc = cmds.parentConstraint('L_wrist_end', 'gun_jnt_grp' ,mo=True)
R_hand_pc = cmds.parentConstraint('R_wrist_end', 'gun_jnt_grp' ,mo=True)
chest_pc = cmds.parentConstraint('chest_ctrl', 'gun_jnt_grp' ,mo=True)
hips_pc = cmds.parentConstraint('pelvis_ctrl', 'gun_jnt_grp' ,mo=True)

con = cmds.createNode('condition')
cmds.setAttr(f'{con}.colorIfTrueR', 1)
cmds.setAttr(f'{con}.colorIfFalseR', 0)
cmds.connectAttr('gun_jnt_ctrl.spaceSwitch', f'{con}.firstTerm')
cmds.setAttr(f'{con}.secondTerm', 1)
cmds.connectAttr(f'{con}.outColorR', 'gun_jnt_grp_parentConstraint1.L_wrist_endW0')


con = cmds.createNode('condition')
cmds.setAttr(f'{con}.colorIfTrueR', 1)
cmds.setAttr(f'{con}.colorIfFalseR', 0)
cmds.connectAttr('gun_jnt_ctrl.spaceSwitch', f'{con}.firstTerm')
cmds.setAttr(f'{con}.secondTerm', 2)
cmds.connectAttr(f'{con}.outColorR', 'gun_jnt_grp_parentConstraint1.R_wrist_endW1')

con = cmds.createNode('condition')
cmds.setAttr(f'{con}.colorIfTrueR', 1)
cmds.setAttr(f'{con}.colorIfFalseR', 0)
cmds.connectAttr('gun_jnt_ctrl.spaceSwitch', f'{con}.firstTerm')
cmds.setAttr(f'{con}.secondTerm', 3)
cmds.connectAttr(f'{con}.outColorR', 'gun_jnt_grp_parentConstraint1.chest_ctrlW2')


con = cmds.createNode('condition')
cmds.setAttr(f'{con}.colorIfTrueR', 1)
cmds.setAttr(f'{con}.colorIfFalseR', 0)
cmds.connectAttr('gun_jnt_ctrl.spaceSwitch', f'{con}.firstTerm')
cmds.setAttr(f'{con}.secondTerm', 4)
cmds.connectAttr(f'{con}.outColorR', 'gun_jnt_grp_parentConstraint1.pelvis_ctrlW3')

cmds.setAttr("DC15A_blasterRifle_geo.overrideEnabled", 1)
cmds.setAttr("DC15s_blaster_geo.overrideEnabled", 1)

cmds.connectAttr("C_attr_ctrl.model_display", "DC15A_blasterRifle_geo.overrideDisplayType")
cmds.connectAttr("C_attr_ctrl.model_display", "DC15s_blaster_geo.overrideDisplayType")



cmds.addAttr('gun_jnt_ctrl', ln = 'gun', at='enum', en= "blasterRifle:blaster:", k=True)
con = cmds.createNode('condition')
cmds.setAttr(f'{con}.colorIfTrueR', 1)
cmds.setAttr(f'{con}.colorIfFalseR', 0)
cmds.connectAttr('gun_jnt_ctrl.gun', f'{con}.firstTerm')
cmds.setAttr(f'{con}.secondTerm', 0)
cmds.setAttr(f'{con}.colorIfTrueG', 0)
cmds.setAttr(f'{con}.colorIfFalseG', 1)
cmds.connectAttr(f'{con}.outColorR', 'DC15A_blasterRifle_geo.visibility')
cmds.connectAttr(f'{con}.outColorG', 'DC15s_blaster_geo.visibility')




cmds.connectAttr("C_attr_ctrl.model_display", "cloneCommander_belt_geo.overrideDisplayType")