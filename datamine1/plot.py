#coding:utf-8
import os
import pandas as pd
import matplotlib.pyplot as plt

data_path = './data/'
os.chdir(data_path)

df_protein_train    = pd.read_csv('df_protein_train.csv')#1653
df_protein_test     = pd.read_csv('df_protein_test.csv')#414
protein_concat = pd.concat([df_protein_train,df_protein_test])
df_molecule         = pd.read_csv('df_molecule.csv')#111216
df_affinity_train   = pd.read_csv('df_affinity_train.csv')#165084

df_affinity_test    = pd.read_csv('df_affinity_test_toBePredicted.csv')#41383
data  =  pd.concat([df_affinity_train,df_affinity_test])

df_affinity_train["Ki"].plot.hist()
plt.savefig("../data_visual/Ki distribution.png")
plt.clf()
df_molecule.fillna(0,inplace=True)
for col in df_molecule:
    try:
        df_molecule[col].plot.hist(bins= 5)
        plt.savefig("../data_visual/{} distribution.png".format(col))
        plt.clf()
    except Exception:
        pass











