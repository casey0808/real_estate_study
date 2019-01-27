import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats import pearsonr

cc = pd.read_excel('classify.xlsx', index_col = 'city', sheet_name = 'first')
print(cc.head())

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

scaler = StandardScaler()
cc_scaled = scaler.fit_transform(cc)

pca = PCA()
pca.fit(cc_scaled)

# Plot the explained variances
features = range(pca.n_components_)
exp_variance = pca.explained_variance_ratio_

plt.bar(features, exp_variance)
plt.plot(features, exp_variance, c = 'red')
plt.xlabel('PCA feature')
plt.ylabel('variance ratio')
plt.xticks(features)
plt.show()


# ## 3. Further visualization of PCA
# There's no clear 'elbow' showed in the plot above, which means it is not straightforward to find the number of intrinsic dimensions using this method.
# Instead, I look at the cumulative explained variance plot to determine how many features are required to explain 80% of the variance. 

# Calculate the cumulative explained variance
cum_exp_variance = np.cumsum(exp_variance)

# Plot the cumulative explained variance and draw a dashed line at 0.80.
fig, ax = plt.subplots()
ax.plot(cum_exp_variance)
ax.axhline(y=0.8, linestyle='--', c = 'red')
plt.show()


# ## 4. PCA
# 3 components can already explain 80% of the variance.

n_components = 3

# Perform PCA with the chosen number of components and project data onto components
pca = PCA(n_components, random_state= 10)
pca.fit(cc_scaled)
pca_features = pca.transform(cc_scaled)
print(pca_features.shape)


# ## 5. K-Means Clustering

get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.cluster import KMeans
import seaborn as sns

model = KMeans(n_clusters = 3)
model.fit(pca_features)
print(model.inertia_)

# ## 6. Visualize the model

plt.style.use('ggplot')
#plt.style.use('default')
#plt.style.use('fivethirtyeight')

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签

pc1 = pca_features[:, 0]
pc2 = pca_features[:, 1]
pc3 = pca_features[:, 2]
labels = model.labels_

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize = (15, 8))
ax = Axes3D(fig, elev= 25, azim= 130)

ax.scatter(pc2, pc1, pc3,
           c = labels, edgecolor = 'k', s = 30, label = labels)

# plot each point's index as text above
for i in range(len(pc1)): 
    ax.text(pc2[i], pc1[i], pc3[i]*1.05, '%s'%(cc.index[i]), ha = 'right', va = 'center', fontsize=10, color='k')
    
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('pc2')
ax.set_ylabel('pc1')
ax.set_zlabel('pc3')
ax.set_title('City Classification', size = 24)
ax.dist = 10

plt.show()
fig.savefig('classify.png', dpi = 300)


dict = {}

for i in range(54):
    if labels[i] == 1:
        dict[cc.index[i]] = '三线城市'
    elif labels[i] == 2:
        dict[cc.index[i]] = '一线城市'
    else:
        dict[cc.index[i]] = '二线城市'
        

print(dict)
