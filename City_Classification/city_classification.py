import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats import pearsonr

cc = pd.read_excel('classify.xlsx', index_col = 'city', sheetname = 'first')
print(cc.head())

#model = PCA()
#pca_features = model.fit_transform(cc)
#plt.hist(pca_features)
#xs = pca_features[:, 0]
#ys = pca_features[:, 1]
#plt.scatter(xs, ys)
#plt.show()


from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

scaler = StandardScaler()

# Create a PCA instance: pca
pca = PCA()

# Create pipeline: pipeline
pipeline = make_pipeline(scaler, pca)

# Fit the pipeline to 'cc'
pipeline.fit(cc)

# Plot the explained variances
features = range(pca.n_components_)

plt.bar(features, pca.explained_variance_)
plt.xlabel('PCA feature')
plt.ylabel('variance')
plt.xticks(features)
plt.show()


scaler = StandardScaler()

# Create a PCA instance: pca
pca = PCA(n_components = 2)

# Create pipeline: pipeline
pipeline = make_pipeline(scaler, pca)

# Fit the pipeline to 'cc'
pipeline.fit(cc)

pca_features = pipeline.transform(cc)

get_ipython().magic('matplotlib inline')
from sklearn.cluster import KMeans
import seaborn as sns

#plt.style.use('ggplot')
plt.style.use('default')

plt.rcParams['font.sans-serif']=['SimHei'] #in order to display Chinese character
plt.rcParams['axes.unicode_minus']=False #in order to display the '-' sign

model = KMeans(n_clusters = 4)
model.fit(pca_features)
print(model.inertia_)
cc['pc1'] = pca_features[:, 0]
cc['pc2'] = pca_features[:, 1]
cc['label'] = model.labels_
plt.scatter(cc['pc1'], cc['pc2'], label = cc['label'], c = cc['label'], alpha = 0.7)
plt.axes().set_aspect(1/2)


#for label, pc1, pc2 in zip(cc['label'], cc['pc1'], cc['pc2']):
#    plt.annotate(label, xy=(pc1, pc2))     

for index, pc1, pc2, label in zip(cc.index, cc['pc1'], cc['pc2'], cc['label']):
    plt.annotate(index, xy=(pc1, pc2), xytext = (pc1*1.01, pc2*1.01), fontsize = 8) 
    plt.legend((label, 'label'), loc = 'best', fontsize = 'x-small')

plt.xticks([])
plt.yticks([])


plt.show()
plt.savefig('classify.png', dpi = 600)

import seaborn as sns

#plt.figure(figsize=(50,20))


sns.lmplot(x='pc1',y='pc2',data = cc, hue='label', fit_reg=False, aspect = 2, legend_out= True)


for index, pc1, pc2, label in zip(cc.index, cc['pc1'], cc['pc2'], cc['label']):
    plt.annotate(index, xy=(pc1, pc2), xytext = (pc1, pc2*1.05), fontsize = 9) 

plt.savefig('sns_classify.png', dpi = 800)

#sns.jointplot(cc['pc1'], cc['pc2'])
