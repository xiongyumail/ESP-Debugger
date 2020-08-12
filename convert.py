import csv
import io

pos_input_filename = 'output/Down-all.pos'
bom_input_filename = 'output/Down.csv'


pos_output_filename = 'output/pos_jlc.csv'
bom_output_filename = 'output/bom_jlc.csv'


bom_input_field = ['Reference','Value','Footprint','Datasheet', 'LCCODE']
pos_input_field = ['Ref','Val','Package','PosX','PosY','Rot','Side']

bom_output_field = ['Comment','Description','Designator','Footprint','LibRef','Pins','Quantity']
pos_output_field = ['Designator','Footprint','Mid X','Mid Y','Ref X','Ref Y','Pad X','Pad Y','Layer','Rotation','Comment']

bom_input = []
pos_input = []

package_dict = {}
package_dict['LED_SMD:LED_0603_1608Metric'] = 'LED_0603'
package_dict['Fuse:Fuse_0805_2012Metric'] = '0805'
package_dict['Capacitor_SMD:C_0603_1608Metric'] = '0603'
package_dict['Capacitor_SMD:C_0402_1005Metric'] = '0402'
package_dict['Resistor_SMD:R_0402_1005Metric'] = '0402'
package_dict['Resistor_SMD:R_Array_Convex_4x0402'] = '0402_x4'
package_dict['Package_TO_SOT_SMD:SOT-23-6'] = 'SOT-23-6'
package_dict['Package_TO_SOT_SMD:SOT-223'] = 'SOT-223'
package_dict['Package_TO_SOT_SMD:SOT-23'] = 'SOT-23-3'

package_rot = {}
package_rot['R_Array_Convex_4x0402'] = 270
package_rot['SOT-23-6'] = 180
package_rot['SOT-223'] = 0
package_rot['SOT-23'] = 180

with open(bom_input_filename, 'r') as csvfile:
    content = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    bom_input = list(content)


posfile = open(pos_input_filename, 'r').readlines()
posfile2 = [x  for x in posfile if x[0] != '#']

open(pos_input_filename+'2', 'w+').writelines(posfile2) 
with open(pos_input_filename+'2', 'r') as csvfile:
    content = csv.DictReader(csvfile, delimiter=' ', skipinitialspace=True,quotechar='"',fieldnames=pos_input_field)
    pos_input = list(content)
     

with open(bom_output_filename, 'w+') as csvfile:
    content = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=bom_output_field)
    content.writeheader()
    for row in bom_input:
        p = row['Footprint']
        if package_dict.has_key(p):
            p = package_dict[p]
        
        content.writerow({
            'Comment'       : row['Value'],
            'Description'   : row['Reference'],
            'Designator'    : row['Reference'],
            'Footprint'     : p,
            'LibRef'        : '',
            'Pins'          : 2,
            'Quantity'      : 1
            })


with open(pos_output_filename, 'w+') as csvfile:
    Layers = {'top': 'T', 'bottom' : 'B'}

    content = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=pos_output_field)
    content.writeheader()
    for row in pos_input:
        p = row['Package']
        if package_rot.has_key(p):
            rot = float(row['Rot']) + package_rot[p]
        else:
            rot = row['Rot']
        newrow = {
            'Designator'    : row['Ref'],
            'Footprint'     : row['Package'],
            'Mid X'         : row['PosX']+'mm',
            'Mid Y'         : row['PosY']+'mm',
            'Ref X': '','Ref Y':'','Pad X':'','Pad Y':'',
            'Layer'         : Layers[row['Side']],
            'Rotation'      : rot,
            'Comment'       : row['Val']
            }
        content.writerow(newrow)
    
    
    


