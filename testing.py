# Ross Santos, Jarrod Bieber
# Data Analysis program

import xlrd
import xlwt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = Axes3D(fig)

file_location = "C:/Users/Ross/Downloads/obd2_with_gps.xlsx"
#opening the file at file location
workbook = xlrd.open_workbook(file_location)
#choosing which sheet in excel file
sheet = workbook.sheet_by_index(0)

file_location_2 = "C:/Users/Ross/Downloads/Thurs_2-25_Log.xlsx"
workbook2 = xlrd.open_workbook(file_location_2)
sheet_2 = workbook2.sheet_by_index(0)

file_location_3 = "C:/Users/Ross/PycharmProjects/obd2_test_code/database_of_driving.xls"
workbook3 = xlrd.open_workbook(file_location_3)
sheet_speed = workbook3.sheet_by_index(0)
sheet_throttle = workbook3.sheet_by_index(1)

wb = xlwt.Workbook()
ws_speed = wb.add_sheet('speed')
ws_throttle = wb.add_sheet('throttle')

ws_speed.col(0).width, ws_throttle.col(0).width = 5000, 5000
ws_speed.col(1).width, ws_throttle.col(1).width, ws_speed.col(2).width, ws_throttle.col(2).width = 5000, 5000, 5000, 5000
ws_speed.write(0, 0, 'Longitude'), ws_speed.write(0, 1, 'Latitude')
ws_speed.write(0, 2, 'Speed Day 1'), ws_speed.write(0, 3, 'Speed Day 2')
ws_throttle.write(0, 0, 'Longitude'), ws_throttle.write(0, 1, 'Latitude')
ws_throttle.write(0, 2, 'Throttle Day 1'), ws_throttle.write(0, 3, 'Throttle Day 2')


longitude = []
latitude = []
speed = []
throttle = []
empty = []

Matrix = [[0 for x in range(sheet.nrows)] for x in range(sheet.nrows)]

dictionary = []
dictionary_2 = []
dictionary_database = []

for i in range(sheet_speed.nrows):
    dictionary_database.append({'longitude': sheet_speed.cell_value(i, 0), 'latitude': sheet_speed.cell_value(i, 1)})

for i in range(sheet.nrows):
    dictionary.append({'longitude': sheet.cell_value(i, 2), 'latitude': sheet.cell_value(i, 3), 'speed': sheet.cell_value(i, 13), 'throttle': sheet.cell_value(i, 14)})

for i in range(sheet_2.nrows):
    dictionary_2.append({'longitude': sheet_2.cell_value(i, 2), 'latitude': sheet_2.cell_value(i, 3), 'speed': sheet_2.cell_value(i, 12), 'throttle': sheet_2.cell_value(i, 15)})

    #longitude.append(sheet.cell_value(i, 2))
    #latitude.append(sheet.cell_value(i, 3))
    #speed.append(sheet.cell_value(i, 13))
    #throttle.append(sheet.cell_value(i, 14))

dictionary.pop(0)
dictionary_2.pop(0)
dictionary_database.pop(0)

print(dictionary_database[0])
print(dictionary[0])
print(dictionary_2[0])

r = 1
previous_longitude, previous_latitude = 0, 0

for i in dictionary:
    #if float(i['longitude']) != previous_longitude:
    ws_speed.write(r, 0, i['longitude']), ws_speed.write(r, 1, i['latitude'])
    ws_throttle.write(r, 0, i['longitude']), ws_throttle.write(r, 1, i['latitude'])

    ws_speed.write(r, 2, str(i['speed']))
    ws_throttle.write(r, 2, str(i['throttle']))

    previous_longitude = float(i['longitude'])
    previous_latitude = float(i['latitude'])
    r = r +1

print(previous_longitude, previous_latitude)

t = 1
for i in dictionary_2:
    '''
    if float(i['longitude']) != previous_longitude:
        ws_speed.write(r, 0, "(" + str(i['longitude']) + ", " + str(i['latitude']) + ")")
        ws_throttle.write(r, 0, "(" + str(i['longitude']) + ", " + str(i['latitude']) + ")")
    '''

    #ws.write(r, 1, i['latitude'])
    ws_speed.write(t, 3, str(i['speed']))
    ws_throttle.write(t, 3, str(i['throttle']))
    t = t + 1


print(dictionary_database[0])
print(dictionary_database[1])

a=1
distance = 0.00002
for i in dictionary_2:
    for j in dictionary:
        if i['longitude'] + distance >= j['longitude'] and i['longitude'] - distance <= j['longitude'] and i['latitude'] + distance >= j['latitude'] and i['latitude'] - distance <= j['latitude']:
            ws_speed.write(a, 5, "matching coordinates")
            break
    a = a + 1





wb.save('database_of_driving.xls')


'''
empty = [0] * len(longitude)
#graphing location vs speed
ax.bar3d(longitude, latitude, empty, 0.000001, 0.000001, speed)
ax.set_xlabel('longitude')
ax.set_ylabel('latitude')
ax.set_zlabel('speed')
plt.show()
'''


'''
for col in range(sheet.nrows):
    print (sheet.cell_value(0, col))
'''


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