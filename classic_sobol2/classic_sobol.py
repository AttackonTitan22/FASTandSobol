import csv

from SALib.test_functions import Sobol_G
import numpy as np
from matplotlib import pyplot as plt
from numpy import mean

import constant_sobol
import recombination_sobol

# 切换group时，更改seq["group x"]以及求TAE的偏差式


# Define the model inputs
problem = {
    'num_vars': 8,
    'names': ['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8'],
    'bounds': [[0,1]]*8
}
# 预置参数
epoch=100
ST=[0]*8
TAE=[0]*epoch
TAE_Y=[0]*5
TAE_E=[0]*5

seq={"group A":[0,0,0,0,0,0,0,0],"group B":[99,99,99,99,99,99,99,99],"group C":[0,1,4.5,9,99,99,99,99],
     "group D":[99,0,9,0,99,4.5,1,99]}

for n in range(6,11):

    print(f"===================样本数为{2**n}的NEP实验开始===================")

    # Generate samples
    param_values,base_sequences = constant_sobol.sample(problem, 2 ** n, calc_second_order=False)

    for i in range(epoch):
        print(f"&&&&&&&&&&&&&样本数为{2**n}的第{i+1}次实验开始&&&&&&&&&&&&&&&&")
        # Run model
        Y = Sobol_G.evaluate(param_values, np.array(seq["group C"]))

        from SALib.analyze import sobol as sb
        # Perform analysis
        Si = sb.analyze(problem, Y, print_to_console=False,calc_second_order=False)

        # Run model again
        param_values = recombination_sobol.sample(problem, 2 ** n, calc_second_order=False, base_seq=base_sequences)
        # param_values = saltelli.sample(problem, 2 ** n, calc_second_order=False)

        # 敏感性的均值
        for j in range(8):
            ST[j]+=Si['ST'][j]
            # 如果是A组
            # TAE[i]+=abs(Si['ST'][j]-0.278)
            # 如果是B组
            # TAE[i]+=abs(Si['ST'][j]-0.125)

            # 如果是C组
            if j==0:
                TAE[i]+=abs(Si['ST'][j]-0.787)
            elif j==1:
                TAE[i]+=abs(Si['ST'][j]-0.242)
            elif j==2:
                TAE[i]+=abs(Si['ST'][j]-0.034)
            elif j==3:
                TAE[i]+=abs(Si['ST'][j]-0.010)
            else:
                TAE[i]+=abs(Si['ST'][j]-1.05e-4)

            # 如果是D组
            # if j==0 or j==4 or j==7:
            #     TAE[i]+=abs(Si['ST'][j]-6.82e-5)
            # elif j==1 or j==3:
            #     TAE[i]+=abs(Si['ST'][j]-0.512)
            # elif j==2:
            #     TAE[i]+=abs(Si['ST'][j]-0.007)
            # elif j==5:
            #     TAE[i]+=abs(Si['ST'][j]-0.022)
            # else:
            #     TAE[i]+=abs(Si['ST'][j]-0.158)
        print(ST)
        print(TAE)
        print("\n")
    # Print the first-order sensitivity indices
    ST=[i/epoch for i in ST]
    print(f"\033[31m        输入因子敏感性ST分别是{ST}\033[0m")
    print(f"        TAE分别是{TAE}")
    TAE_Y[n-6]=mean(TAE)
    print(f"\033[31m        TAE的平均值是{TAE_Y[n-6]}\033[0m")

    TAE_E[n-6]=np.std(TAE)
    print(f"        TAE的标准差是{TAE_E[n-6]}")
    if n!=10:
        ST = [0] * 8
        TAE = [0] * epoch

# 将本次数据存入文件中
csv_file = open('../sobol2_TAE/groupC_TAE.csv', 'w', newline='')
writer = csv.writer(csv_file)
writer.writerow(TAE_Y)
writer.writerow(TAE_E)
# for i in range(len(data['name'])):
#     writer.writerow([data['name'][i], data['age'][i]])
csv_file.close()


# # 绘制坐标轴标签plt.xlabel("Sample Size")
plt.xlabel("Sample Size")
plt.ylabel("Total Absolute Error")
plt.title("Case")
# x = np.arange(0, 200, 1200)

xpoints=[64,128,256,512,1024]
ypoints=TAE_Y

plt.xlim(0,1200,200)
plt.ylim(0,0.3)

plt.plot(xpoints,ypoints,linestyle="-",color="k")
plt.errorbar(xpoints,ypoints,yerr=TAE_E,capsize=10,capthick=1,fmt="k",ecolor="k",elinewidth=0.75)
plt.show()
