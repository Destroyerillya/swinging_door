import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from itertools import groupby
import math

def swinging_door(data_x,data_y, E):
	first_i = 0 #index of door
	i_U = 1 #index of last element of upper line
	i_L = 1 #index of last element of lower line
	i = 2 #index of new point
	results_x = []
	results_y = []
	U = E + data_y[first_i] #выставили границы первые U,L
	L = data_y[first_i] - E

	while i < len(data_x):

		k_U = ((U - data_y[i_U]) / (data_x[first_i].timestamp() - data_x[i_U].timestamp()))

		k_L = ((L - data_y[i_L]) / (data_x[first_i].timestamp() - data_x[i_L].timestamp()))

		LINE_U_Y = k_U*data_x[i].timestamp() + (data_y[i_U] - k_U*data_x[i_U].timestamp()) #highst of upper line near new point

		LINE_L_Y = k_L*data_x[i].timestamp() + (data_y[i_L] - k_L*data_x[i_L].timestamp()) #highst of lower line near new point

		if data_y[i] >= LINE_U_Y:
			i_U = i # подняли выше линию U 

		if data_y[i] <= LINE_L_Y:
			i_L = i # опустили ниже линию L

		if k_U < k_L: # сравниваем больше двери или нет если больше то открылись
			i = i + 1
		else:# если открылись мы добавляем 2 точки первую, и предпоследнюю до открытия 
			results_x.append(data_x[first_i])
			results_y.append(data_y[first_i])
			first_i = i - 1
			i_U = i
			i_L = i
			i = i + 1
			U = E + data_y[first_i] 
			L = data_y[first_i] - E

	if len(results_x) == 0:
		results_x.append(data_x[first_i])
		results_y.append(data_y[first_i])
	results_x.append(data_x[i - 1])
	results_y.append(data_y[i - 1])

	return results_x,results_y

def test_sw_door():
    conn = sqlite3.connect('', detect_types=sqlite3.PARSE_DECLTYPES) # data

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM main.data")
    data_cpy = cursor.fetchall()
    data_x = [r[0] for r in data_cpy]
    data_y = [r[1] for r in data_cpy]
    E = 1 #e-coef
    results_x, results_y = swinging_door(data_x,data_y, E)
    print(len(data_x),len(results_x))
    plt.plot(data_x, data_y)
    plt.plot(results_x, results_y)
    plt.show()
    
if __name__ == '__main__':
    test_sw_door()
