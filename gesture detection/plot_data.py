import matplotlib.pyplot as plt 
import math

file_path = 'data/wave_down/wave_down_3.txt'
data_file = open(file_path, 'r')

x_acc = []
y_acc = []
z_acc = []
acc = []

lines_num = 0

for line in data_file.readlines():
    lines_num += 1
    line_list = line.split()
    x_ac = float(line_list[2][:-1])
    y_ac = float(line_list[3][:-1])
    z_ac = float(line_list[4])
    x_acc.append(x_ac)
    y_acc.append(y_ac)
    z_acc.append(z_ac)
    acc.append(math.sqrt(x_ac * x_ac + y_ac * y_ac + z_ac * z_ac))


x_axis = list(range(0, lines_num))

plt.plot(x_axis, acc)
plt.show()


