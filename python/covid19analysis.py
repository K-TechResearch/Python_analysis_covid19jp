import numpy as np
#import pandas as pd
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt

#githubからcsv取得
summary = np.genfromtxt('https://github.com/kaz-ogiwara/covid19/raw/master/data/summary.csv',delimiter=',') #copyright TOYO KEIZAI ONLINE
prefectures = np.genfromtxt('https://github.com/kaz-ogiwara/covid19/raw/master/data/prefectures.csv',delimiter=',',names=True, dtype=None) #copyright TOYO KEIZAI ONLINE
#prefectures2 = np.genfromtxt('https://github.com/kaz-ogiwara/covid19/raw/master/data/prefectures-2.csv',delimiter=',',names=True, dtype=None) #copyright TOYO KEIZAI ONLINE
#demography = pd.read_csv('https://github.com/kaz-ogiwara/covid19/raw/master/data/demography.csv') #copyright TOYO KEIZAI ONLINE
csv_name = ['summary','prefecture','prefecture2']
print(prefectures.name)
#diff時のエラー処理のため文字列の列を抽出しリスト化
obj_pick = summary.select_dtypes(include=object)
index_list = list(obj_pick.columns)
#抽出した列を数値に変換し数値以外はNan
for i in index_list:
    summary[i] = pd.to_numeric(summary[i] , errors = 'coerce')
#prefecturs達も処理するが都道府県はそのまま
obj_pick = prefectures.select_dtypes(include=object)
index_list = list(obj_pick.columns)
for i in index_list:
    if i != '都道府県':
        prefectures[i] = pd.to_numeric(prefectures[i] , errors = 'coerce')
obj_pick = prefectures2.select_dtypes(include=object)
index_list = list(obj_pick.columns)
for i in index_list:
    if i != '都道府県':
        prefectures2[i] = pd.to_numeric(prefectures2[i] , errors = 'coerce')
#datetime型のindex
summary['yymmdd'] = summary['year'].astype(str) + '-' + summary['month'].astype(str) + '-' + summary['date'].astype(str)
summary['yymmdd'] = pd.to_datetime(summary['yymmdd'])
summary = summary.set_index('yymmdd')
prefectures['yymmdd'] = prefectures['年'].astype(str) + '-' + prefectures['月'].astype(str) + '-' + prefectures['日'].astype(str)
prefectures['yymmdd'] = pd.to_datetime(prefectures['yymmdd'])
prefectures = prefectures.set_index('yymmdd')
prefectures2['yymmdd'] = prefectures2['年'].astype(str) + '-' + prefectures2['月'].astype(str) + '-' + prefectures2['日'].astype(str)
prefectures2['yymmdd'] = pd.to_datetime(prefectures2['yymmdd'])
prefectures2 = prefectures2.set_index('yymmdd')

#check用コメントアウト
#print(prefectures2.dtypes)
#print(summary.isnull().any())

#prefecturesと2の県抽出して都道府県をNaNに
pre_pick = ['東京都','大阪府','愛知県'] #抽出する県をリストに追加
tokyo = prefectures[prefectures['都道府県'].isin([pre_pick[0]])]
tokyo['都道府県'] = pd.to_numeric(tokyo['都道府県'] , errors = 'coerce')
osaka = prefectures[prefectures['都道府県'].isin([pre_pick[1]])]
osaka['都道府県'] = pd.to_numeric(osaka['都道府県'] , errors = 'coerce')
aichi = prefectures[prefectures['都道府県'].isin([pre_pick[2]])]
aichi['都道府県'] = pd.to_numeric(aichi['都道府県'] , errors = 'coerce')
tokyo2 = prefectures2[prefectures2['都道府県'].isin([pre_pick[0]])]
tokyo2['都道府県'] = pd.to_numeric(tokyo2['都道府県'] , errors = 'coerce')
osaka2 = prefectures2[prefectures2['都道府県'].isin([pre_pick[1]])]
osaka2['都道府県'] = pd.to_numeric(osaka2['都道府県'] , errors = 'coerce')
aichi2 = prefectures2[prefectures2['都道府県'].isin([pre_pick[2]])]
aichi2['都道府県'] = pd.to_numeric(aichi2['都道府県'] , errors = 'coerce')
#summary差分dataframe
summary_diff = summary.diff() #日差分データ
summary_diff3 = summary.diff(3) #3日差分データ
summary_diff7 = summary.diff(7) #7日差分データ
#prefecture差分
tokyo_diff7 = tokyo.diff(7)
osaka_diff7 = osaka.diff(7)
aichi_diff7 = aichi.diff(7)
#prefecture2差分
tokyo2_diff7 = tokyo2.diff(7)
osaka2_diff7 = osaka2.diff(7)
aichi2_diff7 = aichi2.diff(7)

#列のインデックス(行は年月日)
#年,月,日,pcr_tested_positive,pcr_tested,有症状者,無症状者,症状有無確認中,入院治療を要する者,入院治療を要する者（無症状）,退院者,退院者（突合作業中を含む）,人工呼吸器又は集中治療室に入院している者,死亡者,死亡者（突合作業中を含む）,PCR検査数：国立感染症研究所,PCR検査数：検疫所,PCR検査数：地方衛生研究所・保健所,PCR検査数：民間検査会社,PCR検査数：民間検査会社のうち保険適用分,PCR検査数：大学等,PCR検査数：大学等のうち保険適用分,PCR検査数：医療機関,PCR検査数：医療機関のうち保険適用分,pcr_test_total,PCR検査数：保険適用分の合計,URL

#解析用dataframe作成
fig = plt.figure() #plot initializing
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9, 6)) #plot area
#summary
#陽性/PCR人数 1日差分だと誤差大のため7日平均で確認
#summary_diff['yosei/PCR_day'] = summary_diff['pcr_tested_positive'] / summary_diff['pcr_tested']
#summary_diff.plot(x = 'yymmdd', y = 'yosei/PCR_day' , kind='line')
#summary_diff3['yosei/PCR_3day'] = summary_diff3['pcr_tested_positive'] / summary_diff3['pcr_tested']
#summary_diff3.plot(x = 'yymmdd', y = 'yosei/PCR_3day' , kind='line')
summary_diff7['yosei/PCR_7day'] = summary_diff7['pcr_tested_positive'] / summary_diff7['pcr_tested']
summary_diff7['yosei/PCR_N_7day'] = summary_diff7['pcr_tested_positive'] / summary_diff7['pcr_tests_total']
summary_diff7[['yosei/PCR_7day','yosei/PCR_N_7day']].plot(ax = axes[0,0] , kind = 'line' , grid=True , legend =True)
#PCR人数と回数
summary_diff7[['pcr_tested','pcr_tests_total']].plot(ax = axes[1,0] , kind = 'line' , grid=True , legend =True)
#本来ICU入院者/ICU病床総数とのことなので廃止__重症病床率＝重病/(入院-退院-死亡)
#summary_diff['jusho/nyuin_all_now'] = summary['人工呼吸器又は集中治療室に入院している者'] / (summary['入院治療を要する者'] - summary['退院者'] - summary['死亡者'])
#summary_diff['jusho/nyuin_all_now'].plot(ax = axes[0,1] ,kind='line',grid=True , legend =True)

#prefecture
#prefecture2
tokyo2_diff7['tokyo_yosei/PCR_7d'] = tokyo2_diff7['PCR検査陽性者数'] / tokyo2_diff7['PCR検査人数']
osaka2_diff7['osaka_yosei/PCR_7d'] = osaka2_diff7['PCR検査陽性者数'] / osaka2_diff7['PCR検査人数']
aichi2_diff7['aichi_yosei/PCR_7d'] = aichi2_diff7['PCR検査陽性者数'] / aichi2_diff7['PCR検査人数']
tokyo2_diff7[['tokyo_yosei/PCR_7d']].plot(ax = axes[0,1] , kind = 'line' , grid=True , legend =True)
osaka2_diff7[['osaka_yosei/PCR_7d']].plot(ax = axes[0,1] , kind = 'line' , grid=True , legend =True)
aichi2_diff7[['aichi_yosei/PCR_7d']].plot(ax = axes[0,1] , kind = 'line' , grid=True , legend =True)
plt.show()
#参考；大阪独自基準0感染者先週比1.0以下・1感染経路不明10人未満・2陽性率7％未満・3重度病床使用率60％未満