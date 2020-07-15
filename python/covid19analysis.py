#%%
import numpy as np
import pandas as pd
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt

#githubからcsv取得
summary = pd.read_csv('https://github.com/kaz-ogiwara/covid19/raw/master/data/summary.csv') #copyright TOYO KEIZAI ONLINE
prefectures = pd.read_csv('https://github.com/kaz-ogiwara/covid19/raw/master/data/prefectures.csv') #copyright TOYO KEIZAI ONLINE
csv_name = ['summary','prefecture']
#check
print(prefectures.iloc[:,[0,1,2]])

#%%
#diff時のエラー処理のため文字列の列を抽出しリスト化
obj_pick = summary.select_dtypes(include=object)
index_list = list(obj_pick.columns)
#check
print(index_list)

#%%
#抽出した列を数値に変換し数値以外はNan
for i in index_list:
    summary[i] = pd.to_numeric(summary[i] , errors = 'coerce')
#prefecturs達も処理するが都道府県はそのまま
obj_pick = prefectures.select_dtypes(include=object)
index_list = list(obj_pick.columns)
#check
print(index_list)
for i in index_list:
    if i != 'prefectureNameE':
        prefectures[i] = pd.to_numeric(prefectures[i] , errors = 'coerce')
#check
print(prefectures['prefectureNameE'])

#%%
#datetime型のindex
summary['yymmdd'] = summary['year'].astype(str) + '-' + summary['month'].astype(str) + '-' + summary['date'].astype(str)
summary['yymmdd'] = pd.to_datetime(summary['yymmdd'])
summary = summary.set_index('yymmdd')
prefectures['yymmdd'] = prefectures['year'].astype(str) + '-' + prefectures['month'].astype(str) + '-' + prefectures['date'].astype(str)
prefectures['yymmdd'] = pd.to_datetime(prefectures['yymmdd'])
prefectures = prefectures.set_index('yymmdd')

#%%
#prefecturesの県抽出して都道府県をNaNに
pre_pick = ['Tokyo','Osaka','Aichi'] #抽出する県をリストに追加
tokyo = prefectures[prefectures['prefectureNameE'].isin([pre_pick[0]])]
tokyo['prefectureNameE'] = pd.to_numeric(tokyo['prefectureNameE'] , errors = 'coerce')
osaka = prefectures[prefectures['prefectureNameE'].isin([pre_pick[1]])]
osaka['prefectureNameE'] = pd.to_numeric(osaka['prefectureNameE'] , errors = 'coerce')
aichi = prefectures[prefectures['prefectureNameE'].isin([pre_pick[2]])]
aichi['prefectureNameE'] = pd.to_numeric(aichi['prefectureNameE'] , errors = 'coerce')
tokyo
#%%
#summary差分dataframe
summary_diff = summary.diff() #日差分データ
summary_diff3 = summary.diff(3) #3日差分データ
summary_diff7 = summary.diff(7) #7日差分データ
#prefecture差分
tokyo_diff7 = tokyo.diff(7)
osaka_diff7 = osaka.diff(7)
aichi_diff7 = aichi.diff(7)
#check
print(osaka_diff7)
print(osaka_diff7.columns)
#%%
#列のインデックス(行は年月日)
#解析用dataframe作成
fig = plt.figure() #plot initializing
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9, 6)) #plot area
#summary
#陽性/PCR人数 1日差分だと誤差大のため7日平均で確認
summary_diff7['yosei/PCR_7day'] = summary_diff7['tested_positive'] / summary_diff7['people_tested']
summary_diff7['yosei/PCR_N_7day'] = summary_diff7['tested_positive'] / summary_diff7['pcr_tests_total']
summary_diff7[['yosei/PCR_7day','yosei/PCR_N_7day']].plot(ax = axes[0,0] , kind = 'line' , grid=True , legend =True)
#PCR人数と回数
summary_diff7[['people_tested','pcr_tests_total']].plot(ax = axes[1,0] , kind = 'line' , grid=True , legend =True)
#%%
#県別比較_ave7daysを新設
ave7days = summary_diff7
ave7days['testedPositive'] = summary_diff7['tested_positive']/7
ave7days.rename(columns={'testedPositive' : 'Alljp'}, inplace = True)
ave7days['tokyo'] = tokyo_diff7['testedPositive']/7
ave7days['osaka'] = osaka_diff7['testedPositive']/7
ave7days['aichi'] = aichi_diff7['testedPositive']/7
ave7days[['Alljp','tokyo','osaka','aichi']].plot(ax = axes[0,1] , kind = 'line' , grid=True , legend =True)
#%%
plt.show()