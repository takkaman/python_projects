#coding:utf-8
import os
import pandas as pd
from gensim.models import Word2Vec
from multiprocessing import cpu_count
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

data_path = './data/'
os.chdir(data_path)

df_protein_train    = pd.read_csv('df_protein_train.csv')#1653
df_protein_test     = pd.read_csv('df_protein_test.csv')#414
protein_concat = pd.concat([df_protein_train,df_protein_test])
df_molecule         = pd.read_csv('df_molecule.csv')#111216
df_affinity_train   = pd.read_csv('df_affinity_train.csv')#165084
train_size = df_affinity_train.shape[0]
df_affinity_test    = pd.read_csv('df_affinity_test_toBePredicted.csv')#41383
data  =  pd.concat([df_affinity_train,df_affinity_test])


def to_vec(value ,model):
    vec = np.array([0] * 64,dtype=np.float32)
    for i in value:
        vec += model[i]
    vec_norm = vec / np.sqrt(np.sum(vec**2))
    vec_norm = vec_norm.tolist()
    return vec_norm

texts = [[char for char in line] for line in protein_concat['Sequence']]
model = Word2Vec(texts, window=5, min_count=5,size=64, workers=cpu_count())
protein_vec = protein_concat['Sequence'].apply(lambda x: pd.Series(to_vec(x,model)))
protein_info = pd.concat([protein_concat, protein_vec],axis=1).drop(['Sequence'], axis = 1)

feat = []
for i in range(0, len(df_molecule)):
    feat.append(df_molecule['Fingerprint'][i].split(','))
feat = pd.DataFrame(feat)
feat = feat.astype('int')
feat.columns = ["Fingerprint_{0}".format(i) for i in range(0, 167)]
feat["Molecule_ID"] = df_molecule['Molecule_ID']
data = data.merge(feat, on='Molecule_ID', how='left')

feat = df_molecule.drop('Fingerprint', axis=1)
data = data.merge(feat, on='Molecule_ID', how='left')
data = data.merge(protein_info, on='Protein_ID', how='left')

data.drop(['Protein_ID','Molecule_ID'], axis = 1, inplace=True)
data.fillna(value = 0, inplace=True)
train_data = data[0:train_size]
test_data = data[train_size:]
train_feat = train_data.drop('Ki',axis=1)
test_feat = test_data.drop('Ki',axis=1)
train_label = train_data['Ki']
for_train_feat = train_feat[0: int(0.8 * train_size)]
for_eval_feat = train_feat[int(0.8 * train_size):]
for_train_label = train_label[0: int(0.8 * train_size)]
for_eval_label = train_label[int(0.8 * train_size):]

rt = RandomForestRegressor()
rt.fit(for_train_feat,for_train_label)

pre_ki = np.array(rt.predict(for_eval_feat))
tru_ki = np.array(for_eval_label)



bins = np.linspace(-2, 20, 30)

plt.hist(pre_ki, bins, alpha=0.5, label='predict_ki')
plt.hist(tru_ki, bins, alpha=0.5, label='true_ki')
plt.legend(loc='upper right')
plt.show()
print "MSE Loss is {}".format(np.sqrt(np.sum((pre_ki - tru_ki)**2)))
















