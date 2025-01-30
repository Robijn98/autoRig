import maya.cmds as cmds
import sys
sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from general_functions import create_tempCtrl

GROUP = 'GRP'
JOINT = 'JNT'
GUIDE = 'GUIDE'
JAW = 'jaw'
CONTROL = 'CTRL'
#side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'

def addOffset(dst, suffix = 'OFF'):

    grp_offset = cmds.createNode('transform', name = f'{dst}_{suffix}')
    dst_mat = cmds.xform(dst, q=True, m=True, ws=True)
    cmds.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = cmds.listRelatives(dst, parent=True)
    if dst_parent:
        cmds.parent(grp_offset, dst_parent)
    cmds.parent(dst, grp_offset)

    return grp_offset

def createGuides(number=5):
    #creating groups to store guides
    jaw_guide_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_{GUIDE}_{GROUP}')
    locs_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_lip_{GUIDE}_{GROUP}',
                               parent = jaw_guide_grp)
    lips_locs_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_lipMinor_{GUIDE}_{GROUP}',
                                   parent= locs_grp)

    #create locators
    for part in ['upper', 'lower']:

        part_mult = 1 if part == 'upper' else -1
        mid_data = (0, part_mult, 0)

        mid_loc = cmds.spaceLocator(name = f'{CENTER}_{JAW}{part}_lip_{GUIDE}')[0]
        cmds.parent(mid_loc, lips_locs_grp)

        for side in ['L', 'R']:
            for x in range(number):
                multiplier = x + 1 if side == 'L' else -(x + 1)
                loc_data = (multiplier, part_mult, 0)
                loc = cmds.spaceLocator(name = f'{side}_{JAW}{part}_lip_{x+1}_{GUIDE}')[0]
                cmds.parent(loc, lips_locs_grp)

                #set data
                cmds.setAttr(f'{loc}.t', *loc_data)

        #set center data
        cmds.setAttr(f'{mid_loc}.t', *mid_data)

    #create corners
    left_corner_loc = cmds.spaceLocator(name = f'{LEFT}_{JAW}Corner_lip_{GUIDE}')[0]
    right_corner_loc = cmds.spaceLocator(name = f'{RIGHT}_{JAW}Corner_lip_{GUIDE}')[0]

    cmds.parent(left_corner_loc, lips_locs_grp)
    cmds.parent(right_corner_loc, lips_locs_grp)

    cmds.setAttr(f'{left_corner_loc}.translateX',  number+1)
    cmds.setAttr(f'{right_corner_loc}.translateX',-(number+1))

    cmds.select(cl=True)

    #create jaw_base
    jaw_base_guide_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_base_{GUIDE}_{GROUP}',
                                   parent= jaw_guide_grp)
    jaw_guide = cmds.spaceLocator(name = f'{CENTER}_{JAW}_{GUIDE}')[0]
    jaw_inverse_guide = cmds.spaceLocator(name = f'{CENTER}_{JAW}_inverse_{GUIDE}')[0]

    cmds.setAttr(f'{jaw_guide}.t', *(0, -1, -number))
    cmds.setAttr(f'{jaw_inverse_guide}.t', *(0, 1, -number))

    cmds.parent(jaw_guide, jaw_base_guide_grp)
    cmds.parent(jaw_inverse_guide, jaw_base_guide_grp)

    #release selection
    cmds.select(cl=True)

def lip_guides():
    grp = f'{CENTER}_{JAW}_lipMinor_{GUIDE}_{GROUP}'
    guides = []

    if cmds.objExists(grp):
        for loc in cmds.listRelatives(grp):
            guides.append(loc)

    return guides

def jaw_guides():
    grp = f'{CENTER}_{JAW}_base_{GUIDE}_{GROUP}'
    guides = []

    if cmds.objExists(grp):
        for loc in cmds.listRelatives(grp, c=True):
            guides.append(loc)

    return guides

def createHierachy():
    main_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_rig_{GROUP}')
    lip_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_lip_{GROUP}', parent = main_grp)
    main_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}Base_{GROUP}', parent = main_grp)

    lip_minor_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_lip_minor_{GROUP}', parent = lip_grp)
    lip_broad_grp = cmds.createNode('transform', name=f'{CENTER}_{JAW}_lip_broad_{GROUP}', parent = lip_grp)

    cmds.select(cl=True)

def createMinorJoints():

    minor_joints = []
    guides = lip_guides()
    #print(guides)
    for guide in guides:
        mat = cmds.xform(guide, q=True, m=True, ws=True)
        jnt = cmds.joint(name = guide.replace(GUIDE, JOINT))
        cmds.setAttr(f'{jnt}.radius', 0.5)
        cmds.xform(jnt, m=mat, ws=True)

        cmds.parent(jnt, f'{CENTER}_{JAW}_lip_minor_{GROUP}')

        minor_joints.append(jnt)

    return minor_joints

def createBroadJoints():

    upper_joint = cmds.joint(name = f'{CENTER}_{JAW}_broadUpper_{JOINT}')
    cmds.select(cl=True)
    lower_joint = cmds.joint(name = f'{CENTER}_{JAW}_broadLower_{JOINT}')
    cmds.select(cl=True)
    left_joint = cmds.joint(name = f'{LEFT}_{JAW}_broadCorner_{JOINT}')
    cmds.select(cl=True)
    right_joint = cmds.joint(name = f'{RIGHT}_{JAW}_broadCorner_{JOINT}')
    cmds.select(cl=True)

    #parent joints under broad group
    cmds.parent([upper_joint, lower_joint, left_joint, right_joint], f'{CENTER}_{JAW}_lip_broad_{GROUP}')

    #get guides positions
    upper_pos = cmds.xform(f'{CENTER}_{JAW}upper_lip_{GUIDE}', q=True, m=True, ws=True)
    lower_pos = cmds.xform(f'{CENTER}_{JAW}lower_lip_{GUIDE}', q=True, m=True, ws=True)
    left_pos = cmds.xform(f'{LEFT}_{JAW}Corner_lip_{GUIDE}', q=True, m=True, ws=True)
    right_pos = cmds.xform(f'{RIGHT}_{JAW}Corner_lip_{GUIDE}', q=True, m=True, ws=True)

    #set joint positions
    cmds.xform(upper_joint, m=upper_pos)
    cmds.xform(lower_joint, m=lower_pos)
    cmds.xform(left_joint, m=left_pos)
    cmds.xform(right_joint, m=right_pos)

    cmds.select(cl=True)

def createJawBase():
    #print(jaw_guides())
    jaw_jnt = cmds.joint(name = f'{CENTER}_{JAW}_{JOINT}')
    cmds.select(cl=True)
    jaw_inverse_jnt = cmds.joint(name = f'{CENTER}_inverse_{JAW}_{JOINT}')
    cmds.select(cl=True)

    jaw_mat = cmds.xform(jaw_guides()[0], q=True, m=True, ws=True)
    #print(jaw_guides()[1])
    jaw_inverse_mat = cmds.xform(jaw_guides()[1], q=True, m=True, ws=True)


    cmds.xform(jaw_jnt, m=jaw_mat)
    cmds.xform(jaw_inverse_jnt, m=jaw_inverse_mat)

    cmds.parent(jaw_jnt, f'{CENTER}_{JAW}Base_{GROUP}')
    cmds.parent(jaw_inverse_jnt, f'{CENTER}_{JAW}Base_{GROUP}')

    cmds.select(cl=True)

    #add offsets
    addOffset(jaw_jnt, suffix = 'OFF')
    addOffset(jaw_inverse_jnt, suffix = 'OFF')

    addOffset(jaw_jnt, suffix = 'AUTO')
    addOffset(jaw_inverse_jnt, suffix = 'AUTO')

    cmds.select(cl=True)

def constraintBroadJoints():

    jaw_jnt = f'{CENTER}_{JAW}_{JOINT}'
    inverse_jaw_jnt = f'{CENTER}_inverse_{JAW}_{JOINT}'

    broad_upper = f'{CENTER}_{JAW}_broadUpper_{JOINT}'
    broad_lower = f'{CENTER}_{JAW}_broadLower_{JOINT}'
    broad_left = f'{LEFT}_{JAW}_broadCorner_{JOINT}'
    broad_right = f'{RIGHT}_{JAW}_broadCorner_{JOINT}'

    #add offsets
    upper_off = addOffset(broad_upper)
    lower_off = addOffset(broad_lower)
    left_off = addOffset(broad_left)
    right_off = addOffset(broad_right)

    #constraining joints
    cmds.parentConstraint(jaw_jnt, lower_off, mo=True)
    cmds.parentConstraint(inverse_jaw_jnt, upper_off, mo=True)
    cmds.parentConstraint(upper_off, lower_off, left_off, mo=True)
    cmds.parentConstraint(upper_off, lower_off,right_off, mo=True)

    cmds.select(cl=True)

def getLipParts():

    upper_token = 'jawupper'
    lower_token = 'jawlower'
    corner_token = 'jawCorner'

    C_upper = f'{CENTER}_{JAW}_broadUpper_{JOINT}'
    C_lower = f'{CENTER}_{JAW}_broadLower_{JOINT}'
    R_corner = f'{RIGHT}_{JAW}_broadCorner_{JOINT}'
    L_corner = f'{LEFT}_{JAW}_broadCorner_{JOINT}'

    lip_joints = cmds.listRelatives(f'{CENTER}_{JAW}_lip_{GROUP}', allDescendents=True)

    dict_lips = {'C_upper': {}, 'C_lower': {},
                 'L_upper': {}, 'L_lower': {},
                 'R_upper': {}, 'R_lower': {},
                 'L_corner': {}, 'R_corner': {}}

    for joint in lip_joints:

        if cmds.objectType(joint) != 'joint':
            continue

        if joint.startswith('C') and upper_token in joint:
            dict_lips['C_upper'][joint] = [C_upper]

        if joint.startswith('C') and lower_token in joint:
            dict_lips['C_lower'][joint] = [C_lower]

        if joint.startswith('L') and upper_token in joint:
            dict_lips['L_upper'][joint] = [C_upper, L_corner]

        if joint.startswith('L') and lower_token in joint:
            dict_lips['L_lower'][joint] = [C_lower, L_corner]

        if joint.startswith('R') and upper_token in joint:
            dict_lips['R_upper'][joint] = [C_upper, R_corner]

        if joint.startswith('R') and lower_token in joint:
            dict_lips['R_lower'][joint] = [C_lower, R_corner]

        if joint.startswith('L') and corner_token in joint:
            dict_lips['L_corner'][joint] = [L_corner]

        if joint.startswith('R') and corner_token in joint:
            dict_lips['R_corner'][joint] = [R_corner]

    return dict_lips

def lipParts(part):

    lip_parts = [reversed(sorted(getLipParts()[f'L_{part}'].keys())), getLipParts()[f'C_{part}'].keys(),
                 sorted(getLipParts()[f'R_{part}'].keys())]

    return [joint for joint in lip_parts for joint in joint]

def createSeals(part):

    seal_name = f'{CENTER}_seal_{GROUP}'
    seal_parent = seal_name if cmds.objExists(seal_name) else \
        cmds.createNode('transform', name = seal_name, parent = f'{CENTER}_{JAW}_rig_{GROUP}')

    part_grp = cmds.createNode('transform', name = seal_name.replace('seal', f'seal_{part}'), parent = seal_parent)

    l_corner = f'{LEFT}_{JAW}_broadCorner_{JOINT}'
    r_corner = f'{RIGHT}_{JAW}_broadCorner_{JOINT}'

    value = len(lipParts(part))

    for index, joint in enumerate(lipParts(part)):
        node = cmds.createNode('transform', name = joint.replace('JNT', f'{part}_seal'), parent = part_grp)
        mat = cmds.xform(joint, q=True, m=True, ws=True)
        cmds.xform(node, m=mat)

        constraint = cmds.parentConstraint(l_corner, r_corner, node, mo=True)[0]
        cmds.setAttr(f'{constraint}.interpType', 2)

        r_corner_value = float(index)/float(value - 1)
        l_corner_value = 1 - r_corner_value

        l_corner_attr = f'{constraint}.{l_corner}W0'
        r_corner_attr = f'{constraint}.{r_corner}W1'

        cmds.setAttr(l_corner_attr, l_corner_value)
        cmds.setAttr(r_corner_attr, r_corner_value)

    cmds.select(cl=True)


def createJawAttrs():


    #node = cmds.circle(n = 'jaw_attributes')[0]
    #grp = cmds.group(node, n='jaw_attributes_GRP')
    node = cmds.createNode('transform', name = 'jaw_attributes', parent = f'{CENTER}_{JAW}_rig_{GROUP}')
    cmds.addAttr(node, ln= sorted(getLipParts()['C_upper'].keys())[0], min=0, max=1, dv=0)
    cmds.setAttr(f"{node}.{sorted(getLipParts()['C_upper'].keys())[0]}", lock=1)

    for upper in sorted(getLipParts()['L_upper'].keys()):
        cmds.addAttr(node, ln=upper, min=0, max=1, dv=0)

    cmds.addAttr(node, ln= sorted(getLipParts()['L_corner'].keys())[0], min=0, max=1, dv=1)
    cmds.setAttr(f"{node}.{sorted(getLipParts()['L_corner'].keys())[0]}", lock=1)

    for lower in sorted(getLipParts()['L_lower'].keys())[::-1]:
        cmds.addAttr(node, ln=lower, min=0, max=1, dv=0)

    cmds.addAttr(node, ln= sorted(getLipParts()['C_lower'].keys())[0], min=0, max=1, dv=0)
    cmds.setAttr(f"{node}.{sorted(getLipParts()['C_lower'].keys())[0]}", lock=1)

    createOffsetFollow()
    addSealAttr()

def createConstraint():

    for value in getLipParts().values():
        for lip_jnt, broad_jnt in value.items():

            seal_token = 'upper_seal' if 'upper' in lip_jnt else 'lower_seal'
            lip_seal = lip_jnt.replace(JOINT, seal_token)

            if cmds.objExists(lip_seal):
                const = cmds.parentConstraint(broad_jnt, lip_seal, lip_jnt, mo=True)[0]
                cmds.setAttr(f'{const}.interpType', 2)

                if len(broad_jnt) == 1:
                    seal_attr = f'{lip_jnt}_parentConstraint1.{lip_seal}W1'
                    rev = cmds.createNode('reverse', name= lip_jnt.replace(JOINT, 'REV'))
                    cmds.connectAttr(seal_attr, f'{rev}.inputX')
                    cmds.connectAttr(f'{rev}.outputX', f'{lip_jnt}_parentConstraint1.{broad_jnt[0]}W0')
                    cmds.setAttr(seal_attr, 0)

                if len(broad_jnt) == 2:
                    seal_attr = f'{lip_jnt}_parentConstraint1.{lip_seal}W2'
                    cmds.setAttr(seal_attr, 0)

                    seal_rev = cmds.createNode('reverse', name=lip_jnt.replace(JOINT, 'seal_REV'))
                    jaw_attr_rev = cmds.createNode('reverse', name=lip_jnt.replace(JOINT, 'jaw_attr_REV'))
                    seal_mult = cmds.createNode('multiplyDivide', name=lip_jnt.replace(JOINT, 'seal_MULT'))

                    cmds.connectAttr(seal_attr, f'{seal_rev}.inputX')
                    cmds.connectAttr(f'{seal_rev}.outputX', f'{seal_mult}.input2X')
                    cmds.connectAttr(f'{seal_rev}.outputX', f'{seal_mult}.input2Y')

                    cmds.connectAttr(f'jaw_attributes.{lip_jnt.replace(lip_jnt[0], "L")}', f'{seal_mult}.input1Y')

                    cmds.connectAttr(f'jaw_attributes.{lip_jnt.replace(lip_jnt[0], "L")}', f'{jaw_attr_rev}.inputX')

                    cmds.connectAttr(f'{jaw_attr_rev}.outputX', f'{seal_mult}.input1X')

                    cmds.connectAttr(f'{seal_mult}.outputX', f'{lip_jnt}_parentConstraint1.{broad_jnt[0]}W0')

                    cmds.connectAttr(f'{seal_mult}.outputY', f'{lip_jnt}_parentConstraint1.{broad_jnt[1]}W1')


            else:
                const = cmds.parentConstraint(broad_jnt, lip_jnt, mo=True)[0]
                cmds.setAttr(f'{const}.interpType', 2)


def initialValuesJaw(part, degree= 1.3):

    jaw_attr = [part for part in lipParts(part) if not part.startswith('C') and not part.startswith('R')]
    value = len(jaw_attr)

    for index, attr_name in enumerate(jaw_attr[::-1]):
        attr = f'jaw_attributes.{attr_name}'

        linear_value = float(index) / float(value-1)
        div_value = linear_value / degree
        final_value = div_value * linear_value

        cmds.setAttr(attr, final_value)

def createOffsetFollow():
    jaw_attr = 'jaw_attributes'

    jaw_joint = f'{CENTER}_{JAW}_{JOINT}'
    jaw_auto = f'{CENTER}_{JAW}_{JOINT}_AUTO'

    #add follow constraints
    cmds.addAttr(jaw_attr, ln = 'follow_ty', min = -10, max=10, dv=0)
    cmds.addAttr(jaw_attr, ln = 'follow_tz', min = -10, max=10, dv=0)

    unit = cmds.createNode('unitConversion', name = f'{CENTER}_{JAW}_follow_UNIT')

    remap_y = cmds.createNode('remapValue', name = f'{CENTER}_{JAW}_followY_remap')
    cmds.setAttr(f'{remap_y}.inputMax', 1)

    remap_z = cmds.createNode('remapValue', name=f'{CENTER}_{JAW}_followY_remap')
    cmds.setAttr(f'{remap_z}.inputMax', 1)

    mult_y = cmds.createNode('multDoubleLinear', name = f'{CENTER}_{JAW}_followY_MULT')
    cmds.setAttr(f'{mult_y}.input2', 1)

    cmds.connectAttr(f'{jaw_joint}.rx', f'{unit}.input')
    cmds.connectAttr(f'{unit}.output', f'{remap_y}.inputValue')
    cmds.connectAttr(f'{unit}.output', f'{remap_z}.inputValue')

    cmds.connectAttr(f'{jaw_attr}.follow_ty', f'{mult_y}.input1')
    cmds.connectAttr(f'{jaw_attr}.follow_tz', f'{remap_z}.outputMax')
    cmds.connectAttr(f'{mult_y}.output', f'{remap_y}.outputMax')

    cmds.connectAttr(f'{remap_y}.outValue', f'{jaw_auto}.ty')
    cmds.connectAttr(f'{remap_z}.outValue', f'{jaw_auto}.tz')

def addSealAttr():

    jaw_attr = 'jaw_attributes'

    cmds.addAttr(jaw_attr, at='double', ln='L_seal', min=0, max=10, dv=0)
    cmds.addAttr(jaw_attr, at='double', ln='R_seal', min=0, max=10, dv=0)

    cmds.addAttr(jaw_attr, at='double', ln='L_seal_delay', min=0.1, max=10, dv=4)
    cmds.addAttr(jaw_attr, at='double', ln='R_seal_delay', min=0.1, max=10, dv=4)


def connectSeal(part):

    seal_token = f'seal_{part}'

    jaw_attrs = 'jaw_attributes'
    lip_jnts = lipParts(part)
    value = len(lip_jnts)
    seal_driver = cmds.createNode('lightInfo', name=f'C_{seal_token}_DRV')

    triggers = {'L': list(), 'R': list()}


    for side in ['L','R']:
        delay_sub_name = f'{side}_{seal_token}_delay_SUB'
        delay_sub = cmds.createNode('plusMinusAverage', name=delay_sub_name)

        cmds.setAttr(f'{delay_sub}.operation', 2)
        cmds.setAttr(f'{delay_sub}.input1D[0]', 10)
        cmds.connectAttr(f'{jaw_attrs}.{side}_seal_delay', f'{delay_sub}.input1D[1]')

        lerp = 1 / float(value - 1)

        delay_div_name = f'{side}_{seal_token}_delay_DIV'
        delay_div = cmds.createNode('multDoubleLinear', name= delay_div_name)
        cmds.setAttr(f'{delay_div}.input2', lerp)
        cmds.connectAttr(f'{delay_sub}.output1D', f'{delay_div}.input1')

        mult_triggers = list()
        sub_triggers = list()
        triggers[side].append(mult_triggers)
        triggers[side].append(sub_triggers)

        print("HERE")
        print(triggers)

        for index in range(value):
            index_name = 'jaw_{:02d}'.format(index)

            #creat MULT node
            delay_mult_name = f'{index_name}_{side}_{seal_token}_delay_MULT'
            delay_mult = cmds.createNode('multDoubleLinear', n=delay_mult_name)
            cmds.setAttr(f'{delay_mult}.input1', index)
            cmds.connectAttr(f'{delay_div}.output', f'{delay_mult}.input2')

            mult_triggers.append(delay_mult)

            #create SUB Mode
            delay_sub_name = f'{index_name}_{side}_{seal_token}_delay_SUB'
            delay_sub = cmds.createNode('plusMinusAverage', n=delay_sub_name)
            cmds.connectAttr(f'{delay_mult}.output', f'{delay_sub}.input1D[0]')
            cmds.connectAttr(f'{jaw_attrs}.{side}_seal_delay', f'{delay_sub}.input1D[1]')

            sub_triggers.append(delay_sub)

    #get constraints
    const_targets = []

    for jnt in lip_jnts:
        attrs = cmds.listAttr(f'{jnt}_parentConstraint1', ud=True)
        for attr in attrs:
            if 'seal' in attr:
                const_targets.append(f'{jnt}_parentConstraint1.{attr}')


    #connect seal triggers to driver node
    for left_index, const_target in enumerate(const_targets):
        right_index = value - left_index - 1
        index_name = f'{seal_token}_{left_index}'

        l_mult_trigger, l_sub_trigger = triggers['L'][0][left_index], triggers['L'][1][left_index]
        r_mult_trigger, r_sub_trigger = triggers['R'][0][right_index], triggers['R'][1][right_index]

        #left
        l_remap_name = f'L_{seal_token}_{index_name}_REMAP'
        l_remap = cmds.createNode('remapValue', name = l_remap_name)
        cmds.setAttr(f'{l_remap}.outputMax', 1)
        cmds.setAttr(f'{l_remap}.value[0].value_Interp', 2)

        cmds.connectAttr(f'{l_mult_trigger}.output', f'{l_remap}.inputMin')
        cmds.connectAttr(f'{l_sub_trigger}.output1D', f'{l_remap}.inputMax')

        #connect left seal attribute to input of remap
        cmds.connectAttr(f'{jaw_attrs}.L_seal', f'{l_remap}.inputValue')

        #right
        #substract 1 minus result from left remap
        r_sub_name = f'R_{seal_token}_offset_{index_name}_SUB'
        r_sub = cmds.createNode('plusMinusAverage', name=r_sub_name)
        cmds.setAttr(f'{r_sub}.input1D[0]', 1)
        cmds.setAttr(f'{r_sub}.operation', 2)

        cmds.connectAttr(f'{l_remap}.outValue', f'{r_sub}.input1D[1]')

        r_remap_name = f'R_{seal_token}_{index_name}_REMAP'
        r_remap = cmds.createNode('remapValue', name=r_remap_name)
        cmds.setAttr(f'{r_remap}.outputMax', 1)
        cmds.setAttr(f'{r_remap}.value[0].value_Interp', 2)

        cmds.connectAttr(f'{r_mult_trigger}.output', f'{r_remap}.inputMin')
        cmds.connectAttr(f'{r_sub_trigger}.output1D', f'{r_remap}.inputMax')

        # connect right seal attribute to input of remap
        cmds.connectAttr(f'{jaw_attrs}.R_seal', f'{r_remap}.inputValue')

        cmds.connectAttr(f'{r_sub}.output1D', f'{r_remap}.outputMax')

        #final addition both sides
        plus_name = f'{index_name}_SUM'
        plus = cmds.createNode('plusMinusAverage', name = plus_name)

        cmds.connectAttr(f'{l_remap}.outValue', f'{plus}.input1D[0]')
        cmds.connectAttr(f'{r_remap}.outValue', f'{plus}.input1D[1]')

        clamp_name = f'{index_name}_CLAMP'
        clamp = cmds.createNode('remapValue', name = clamp_name)
        cmds.connectAttr(f'{plus}.output1D', f'{clamp}.inputValue')

        cmds.addAttr(seal_driver, at='double', ln=index_name, min=0, max=1, dv=0)
        cmds.connectAttr(f'{clamp}.outValue', f'{seal_driver}.{index_name}')

        cmds.connectAttr(f'{seal_driver}.{index_name}', const_target)

def createJawPins():

    pin_driver = cmds.createNode('lightInfo', name = f'{CENTER}_pin_DRV')

    for side in ['L', 'R']:

        jaw_attr = 'jaw_attributes'

        cmds.addAttr(jaw_attr, at='bool', ln=f'{side}_auto_corner_pin')
        cmds.addAttr(jaw_attr, at='double', ln=f'{side}_corner_pin', min=-10, max=10, dv=0)
        cmds.addAttr(jaw_attr, at='double', ln=f'{side}_input_ty', min=-10, max=10, dv=0)

        #create clamp and connect imput_ty to it
        clamp = cmds.createNode('clamp', name = f'{side}_corner_pin_auto_CLAMP')
        cmds.setAttr(f'{clamp}.minR', -10)
        cmds.setAttr(f'{clamp}.maxR', 10)

        cmds.connectAttr(f'{jaw_attr}.{side}_input_ty', f'{clamp}.inputR')

        #create condition for the two possible scenarios
        cnd = cmds.createNode('condition', name = f'{side}_corner_pin_auto_CND')
        cmds.setAttr(f'{cnd}.operation', 0)
        cmds.setAttr(f'{cnd}.secondTerm', 1)

        cmds.connectAttr(f'{jaw_attr}.{side}_auto_corner_pin', f'{cnd}.firstTerm')
        cmds.connectAttr(f'{clamp}.outputR', f'{cnd}.colorIfTrueR')
        cmds.connectAttr(f'{jaw_attr}.{side}_corner_pin', f'{cnd}.colorIfFalseR')

        #create addition
        plus = cmds.createNode('plusMinusAverage', name= f'{side}_corner_pin_PLUS')
        cmds.setAttr(f'{plus}.input1D[1]', 10)
        cmds.connectAttr(f'{cnd}.outColorR', f'{plus}.input1D[0]')

        #create division
        div = cmds.createNode('multDoubleLinear', name= f'{side}_corner_pin_DIV')
        cmds.setAttr(f'{div}.input2', 0.05)
        cmds.connectAttr(f'{plus}.output1D', f'{div}.input1')

        #add final output attributes to the driver node
        cmds.addAttr(pin_driver, at='double', ln=f'{side}_pin', min=0, max=1, dv=0)
        cmds.connectAttr(f'{div}.output', f'{pin_driver}.{side}_pin')

        #connect driver
        const_pin_up = f'{side}_jaw_broadCorner_JNT_OFF_parentConstraint1.C_jaw_broadUpper_JNT_OFFW0'
        const_pin_down = f'{side}_jaw_broadCorner_JNT_OFF_parentConstraint1.C_jaw_broadLower_JNT_OFFW1'

        cmds.connectAttr(f'{pin_driver}.{side}_pin', const_pin_up)

        rev = cmds.createNode('reverse', name = f'{side}_corner_pin_REV')
        cmds.connectAttr(f'{pin_driver}.{side}_pin', f'{rev}.inputX')
        cmds.connectAttr(f'{rev}.outputX', const_pin_down)



def create_jawCtrl():
    jaw_grp, jaw_ctrl = create_tempCtrl(f'{CENTER}_{JAW}_{CONTROL}', lock = ['sx', 'sy', 'sz', 'tx', 'ty', 'tz'])

    mat = cmds.xform(f'{CENTER}_{JAW}_{JOINT}', q=True, m=True, ws=True)
    cmds.xform(jaw_grp, m=mat, ws=True)

    cmds.parentConstraint(jaw_ctrl, f'{CENTER}_{JAW}_{JOINT}_OFF', mo=True)

    cmds.addAttr(jaw_ctrl, ln='follow_TY', at='double', min=-10, max=10, dv =0, k=True, h=False)
    cmds.addAttr(jaw_ctrl, ln='follow_TZ', at='double', min=-10, max=10, dv =0, k=True, h=False)

    cmds.addAttr(jaw_ctrl, ln=f'{LEFT}_seal', at='double', min=0, max=10, dv =0, k=True, h=False)
    cmds.addAttr(jaw_ctrl, ln=f'{RIGHT}_seal', at='double', min=0, max=10, dv =0, k=True, h=False)

    cmds.addAttr(jaw_ctrl, ln=f'{LEFT}_seal_delay', at='double', min=0.1, max=10, dv =4, k=True, h=False)
    cmds.addAttr(jaw_ctrl, ln=f'{RIGHT}_seal_delay', at='double', min=0.1, max=10, dv =4, k=True, h=False)

    cmds.addAttr(jaw_ctrl, ln=f'{LEFT}_autocorner_pin', at='enum', en = "off:on", k=True, h=False)
    cmds.addAttr(jaw_ctrl, ln=f'{LEFT}_corner_pin', at='double', min=-10, max=10, dv =0, k=True, h=False)
    cmds.addAttr(jaw_ctrl, ln=f'{LEFT}_input_TY', at='double', min=-10, max=10, dv =0, k=True, h=False)

    cmds.addAttr(jaw_ctrl, ln=f'{RIGHT}_autocorner_pin', at='enum', en = "off:on", k=True, h=False)
    cmds.addAttr(jaw_ctrl, ln=f'{RIGHT}_corner_pin', at='double', min=-10, max=10, dv =0, k=True, h=False)
    cmds.addAttr(jaw_ctrl, ln=f'{RIGHT}_input_TY', at='double', min=-10, max=10, dv =0, k=True, h=False)

    cmds.connectAttr(f'{jaw_ctrl}.follow_TY', 'jaw_attributes.follow_ty')
    cmds.connectAttr(f'{jaw_ctrl}.follow_TZ', 'jaw_attributes.follow_tz')

    cmds.connectAttr(f'{jaw_ctrl}.{LEFT}_seal', 'jaw_attributes.L_seal')
    cmds.connectAttr(f'{jaw_ctrl}.{RIGHT}_seal', 'jaw_attributes.R_seal')
    cmds.connectAttr(f'{jaw_ctrl}.{LEFT}_seal_delay', 'jaw_attributes.L_seal_delay')
    cmds.connectAttr(f'{jaw_ctrl}.{RIGHT}_seal_delay', 'jaw_attributes.R_seal_delay')

    cmds.connectAttr(f'{jaw_ctrl}.{LEFT}_autocorner_pin', 'jaw_attributes.L_auto_corner_pin')
    cmds.connectAttr(f'{jaw_ctrl}.{LEFT}_corner_pin', 'jaw_attributes.L_corner_pin')
    cmds.connectAttr(f'{jaw_ctrl}.{LEFT}_input_TY', 'jaw_attributes.L_input_ty')

    cmds.connectAttr(f'{jaw_ctrl}.{RIGHT}_autocorner_pin', 'jaw_attributes.R_auto_corner_pin')
    cmds.connectAttr(f'{jaw_ctrl}.{RIGHT}_corner_pin', 'jaw_attributes.R_corner_pin')
    cmds.connectAttr(f'{jaw_ctrl}.{RIGHT}_input_TY', 'jaw_attributes.R_input_ty')




#testing
#createGuides(number=1)
createHierachy()
createMinorJoints()
createBroadJoints()
createJawBase()
constraintBroadJoints()
createSeals('lower')
createSeals('upper')
createJawAttrs()
createConstraint()
initialValuesJaw('upper')
initialValuesJaw('lower')
connectSeal('lower')
connectSeal('upper')
createJawPins()
create_jawCtrl()