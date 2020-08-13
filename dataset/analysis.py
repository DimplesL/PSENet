import json
import matplotlib.pyplot as plt
import pandas as pd


a = json.load(open('s.txt', 'r'))
t = pd.Series(a)
good_v_ssim = t.quantile(0.1)
fig = plt.figure(figsize=(10, 8))  # figsize=(10, 8)
plt.suptitle('show', fontsize=8)
plt.plot()
# plt.xlim(0, 1)
plt.hist(a, bins=50, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
# 显示横轴标签
plt.xlabel(": %6.8f" % good_v_ssim)
# 显示纵轴标签
plt.ylabel("number")
plt.show()
# plt.savefig(os.path.join('/Users/qiuyurui/Desktop/blurry_judge/{}_ssim.png'.format(name.split('.txt')[0])))
plt.close(fig)