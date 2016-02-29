import xlrd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = Axes3D(fig)



file_location = "C:/Users/Ross/Downloads/obd2_with_gps.xlsx"
#opening the file at file location
workbook = xlrd.open_workbook(file_location)
#choosing which sheet in excel file
sheet = workbook.sheet_by_index(0)

longitude = []
latitude = []
speed = []
throttle = []
empty = []

Matrix = [[0 for x in range(sheet.nrows)] for x in range(sheet.nrows)]

for i in range(sheet.nrows):
    longitude.append(sheet.cell_value(i, 2))
    latitude.append(sheet.cell_value(i, 3))
    speed.append(sheet.cell_value(i, 13))
    throttle.append(sheet.cell_value(i, 14))

longitude.pop(0)
latitude.pop(0)
speed.pop(0)

empty = [0] * len(longitude)

ax.scatter3D(longitude, latitude, speed)
ax.set_xlabel('longitude')
ax.set_ylabel('latitude')
ax.set_zlabel('speed')
plt.show()

'''
for p in longitude:
    print (p)

for p in latitude:
    print (p)

for p in speed:
    print (p)

for p in throttle:
    print (p)
'''
'''
for col in range(sheet.nrows):
    print (sheet.cell_value(0, col))
'''

rpms = []
throttles = []
distances = []
mpgs = []


'''
col_idx = int(col_idx)
if col_idx < 0 or col_idx >= xl_sheet.ncols:
    print ('Please enter a valid column number (0-%d)' % (xl_sheet.ncols-1))
    return

row_vals = []
for row_idx in range(0, sheet.nrows):
        cell_obj = sheet.cell(row_idx, col_idx)
        cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        row_vals.append(cell_obj.value)
'''

'''

row = sheet.row(0)
from xlrd.sheet import ctype_text

print('(Column #) type:value')
for idx, cell_obj in enumerate(row):
    cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
    print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
'''