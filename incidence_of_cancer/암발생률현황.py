#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

#데이터 로드
cancer=pd.read_csv('E:/프로젝트/분석/24개_암종_성_연령_5세_별_암발생자수__발생률.csv',encoding='cp949')

#데이터 확인
display(cancer)

#'-'로 채워진 결측치 데이터값 nan값으로 변경
for col in cancer.columns:
    cancer.loc[cancer[col] == '-',col] = np.nan
    
#결측치 변경 후 데이터 확인
display(cancer)
#결측치 확인
print(cancer.isnull().sum())  #조발생률 컬럼에서 다수의 결측치확인
#결측치 데이터 확인
pd.set_option('display.max_rows', None) #결측치 데이터 행을 파악하기 위한 설정
display(cancer.loc[cancer['조발생률 (명/10만명)'].isnull(),])
pd.reset_option('display.max_rows') # 설정 초기화
#결측치 행 제거
cancer.dropna(inplace=True)
#인덱스 재정의
cancer.reset_index(drop=True, inplace=True)
display(cancer)

#데이터 형태 확인
cancer.info()
#형변환
cancer = cancer.astype({'시점':'int','발생자수 (명)':'int','조발생률 (명/10만명)':'float'})


#2020년 성별 암 발생자수
c_m = cancer.loc[(cancer['시점']==2020)&(cancer['성별']=='남자')
                 &(cancer['연령별']=='계')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 ,['성별','발생자수 (명)']]

c_w = cancer.loc[(cancer['시점']==2020)&(cancer['성별']=='여자')
                 &(cancer['연령별']=='계')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 ,['성별','발생자수 (명)']]

c_m.reset_index(drop=True, inplace=True)
c_w.reset_index(drop=True, inplace=True)

c_mw_2020 = pd.concat([c_m,c_w], ignore_index=True)
display(c_mw_2020)


import matplotlib.pyplot as plt

plt.style.use('bmh')

#한글 폰트적용
from matplotlib import font_manager, rc 
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name() 
rc('font', family=font_name)

# 그래프 크기 설정
fig,ax = plt.subplots(figsize = (9, 9), dpi = 50)

#원형그래프
wedgeprops={'width': 0.5, 'edgecolor': 'white', 'linewidth': 3}

patches, texts, pcts =ax.pie(c_mw_2020['발생자수 (명)']
       ,labels= ['남자\n('+c_mw_2020.loc[c_mw_2020['성별']=='남자'
                                       ,'발생자수 (명)'].to_string(index=False)+'명)'
                 ,'여자\n('+c_mw_2020.loc[c_mw_2020['성별']=='여자'
                                        ,'발생자수 (명)'].to_string(index=False)+'명)'] 
       ,autopct = '%1.1f%%',pctdistance=0.8,shadow = True,startangle=50
       ,counterclock=False,colors =['#00BFFF','#FF69B4']
                             ,textprops={'fontsize': 28},wedgeprops=wedgeprops)

plt.setp(pcts, fontweight='bold')
plt.setp(texts, fontweight=600)
# 제목 설정
plt.title('2020년 성별 암 발생자수',size = 45,fontweight = 'bold')

# 이미지 삽입 
# 이미지 출처 : www.flaticon.com 
im = plt.imread('E:/프로젝트/분석/tumor.png') 
newax = fig.add_axes([0.2,0.39,0.41,0.2], anchor='NE', zorder=1)
newax.imshow(im)
newax.axis('off')

plt.show()

#2020년 성별 암 조발생률
c_m = cancer.loc[(cancer['시점']==2020)&(cancer['성별']=='남자')
                 &(cancer['연령별']=='계')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 ,['성별','조발생률 (명/10만명)']]

c_w = cancer.loc[(cancer['시점']==2020)&(cancer['성별']=='여자')
                 &(cancer['연령별']=='계')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 ,['성별','조발생률 (명/10만명)']]

c_t = cancer.loc[(cancer['시점']==2020)&(cancer['성별']=='계')
                 &(cancer['연령별']=='계')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 ,['성별','조발생률 (명/10만명)']]

c_m.reset_index(drop=True, inplace=True)
c_w.reset_index(drop=True, inplace=True)
c_t.reset_index(drop=True, inplace=True)

c_mwt_2020 = pd.concat([c_m,c_w,c_t], ignore_index=True)
display(c_mwt_2020)


#막대그래프
bar = plt.bar(c_mwt_2020['성별'],c_mwt_2020['조발생률 (명/10만명)'],0.3
              , alpha=0.5, color =['#00BFFF','#FF69B4','#696969'])
plt.xticks(fontweight='bold')


# 그래프 제목 설정
plt.title("2020년 성별 암 조발생률",size=20, fontweight='bold',pad=10)

#막대 그래프에 숫자 표기
for val in bar:
    plt.text(val.get_x() + val.get_width()/2.0, val.get_height(), f'{val.get_height()}'
             , ha='center', va='bottom', size = 10,fontweight='bold')

plt.show()

#시트설정으로 변경된 음수표시 선언
import matplotlib
matplotlib.rcParams['axes.unicode_minus']=False

#남녀합,모든암 데이터를 제외한 테이블 재정의 
cancer2 = cancer.copy().loc[(cancer['시점']==2020)
                 &(cancer['성별']!='계')
                 &(cancer['24개 암종별']!='모든 암(C00-C96)')
                 &(cancer['연령별']=='계')
                 ,]

#2020년 성별 암 발생자수 순위 컬럼 생성
cancer2['성별 발생자수 순위'] = cancer2.groupby('성별')['발생자수 (명)'].rank(method='min', ascending=False)
cancer_m_r = cancer2.loc[(cancer2['성별 발생자수 순위']<=10.0)&(cancer2['성별']=='남자'),['24개 암종별','발생자수 (명)']]
cancer_w_r = cancer2.loc[(cancer2['성별 발생자수 순위']<=10.0)&(cancer2['성별']=='여자'),['24개 암종별','발생자수 (명)']]

#정렬
cancer_m_r = cancer_m_r.sort_values('발생자수 (명)', ascending=False)
cancer_w_r = cancer_w_r.sort_values('발생자수 (명)', ascending=False)

#좌표평면 크기
plt.subplots(figsize = (20, 10), dpi = 100)

#양방향 그래프 Y축 설정 
rank=np.arange(1,11) #(1~10위)

#양방향 그래프
plt.barh(rank, cancer_m_r['발생자수 (명)'],color='#00BFFF',label='남자')
plt.barh(rank, -cancer_w_r['발생자수 (명)'],color='#FF69B4',label='여자')

#y축 반전
plt.gca().invert_yaxis()

#Y축 눈금 간격 조절
plt.yticks(np.arange(1,11),fontsize=20)

#x축 제거
plt.gca().axes.xaxis.set_visible(False)

#막대 그래프에 숫자 표기(가로 그래프라 x축 y축 치환)
for i, x in enumerate(rank):
    plt.text(list(cancer_m_r['발생자수 (명)'])[i]     #x축
             ,x                                                     #y축
             ,' '+str(list(cancer_m_r['발생자수 (명)'])[i])+' ',              #표시 = y[0]..y[1]
             fontsize = 13, 
             color='black',
             horizontalalignment='right' ,
             verticalalignment='center')
    
    
for i, x in enumerate(rank):
    plt.text(list(cancer_m_r['발생자수 (명)'])[i]
             ,x
             ,' '+str(list(cancer_m_r['24개 암종별'])[i])+' ', 
             fontsize = 11, 
             color='blue',
             horizontalalignment='left' ,
             verticalalignment='center')

for i, x in enumerate(rank):
    plt.text(list(-cancer_w_r['발생자수 (명)'])[i]       
             ,x                                                
             ,' '+str(list(cancer_w_r['24개 암종별'])[i])+' ',    
             fontsize = 11, 
             color='red',
             horizontalalignment='right' ,
             verticalalignment='center') 
    

for i, x in enumerate(rank):
    plt.text(list(-cancer_w_r['발생자수 (명)'])[i]       
             ,x                                                    
             ,' '+str(list(cancer_w_r['발생자수 (명)'])[i])+' ',    
             fontsize = 13, 
             color='black',
             horizontalalignment='left' ,
             verticalalignment='center')    

#타이틀
plt.title('2020년 성별 암 발생자수 순위',size = 30,pad = 15,weight='bold')

#범례 설정
plt.legend(loc = 'lower left',fontsize = 13 ,facecolor ='white')
    
plt.show()





#2020년 연령별(10세별) 남녀 암발생자수 순위(1~5)
cancer_age = cancer.copy().loc[(cancer['성별']=='계')
                 &(cancer['24개 암종별']!='모든 암(C00-C96)')
                 &(cancer['연령별']!='계')
                 &(cancer['시점']==2020) 
                 ,]

#연령컬럼 전처리
cancer_age.loc[cancer_age['연령별'].str[0:2]=='5-','연령별']='05-09세'

for i in range(1,7):
    cancer_age.loc[cancer_age['연령별'].str[:1]==str(i),'연령별']=str(i*10)+'대'

cancer_age.loc[cancer_age['연령별'].str[:1]=='0','연령별']='유아(10세 미만)'

cancer_age_sub = cancer_age.loc[cancer_age['연령별']=='유아(10세 미만)',]

cancer_age = cancer_age.loc[cancer_age['연령별'].str[1:3]=='0대',]
    
cancer_age = pd.concat([cancer_age_sub,cancer_age])
    
cancer_age=cancer_age.groupby(['연령별','24개 암종별'])['발생자수 (명)'].sum().reset_index()
    
cancer_age['연령별 발생자수 순위']=cancer_age.groupby('연령별')['발생자수 (명)'].rank(method='min'
                                                                     , ascending=False)

cancer_age_rank5 = cancer_age.loc[cancer_age['연령별 발생자수 순위'] <=5,]

display(cancer_age_rank5)

#연령별 top5암 원형그래프 라벨 함수
def pie_labels(age):
    temp_labels=[]
    
    if age == 0:
        lable_if=cancer_age_rank5['연령별']=='유아(10세 미만)'
    else:
        lable_if=cancer_age_rank5['연령별']==str(age*10)+'대'
        
    for i in range(1,6):
        temp_labels.append(str(i)+'위 ('+cancer_age_rank5.loc[(cancer_age_rank5['연령별 발생자수 순위']==i*1.0)
                                           &(lable_if)
                                           ,'24개 암종별'].to_string(index=False)+'명)')

    return temp_labels


#연령별 top5암 원형그래프
for i in range(7):
    fig,ax = plt.subplots(figsize = (9, 9), dpi = 50)
    
    if i ==0:
        x=cancer_age_rank5.loc[cancer_age_rank5['연령별']=='유아(10세 미만)','발생자수 (명)']
        title ='유아(10세 미만) top5암'
    else:
        x=cancer_age_rank5.loc[cancer_age_rank5['연령별']==str(i*10)+'대','발생자수 (명)']
        title =str(i*10)+'대 top5암'

    patches, texts, pcts =ax.pie(x
           ,labels= pie_labels(i) 
           ,autopct = '%1.1f%%',pctdistance=0.8,shadow = True,startangle=50
           ,counterclock=False,colors =['blue','red','purple','green','orange']
                                 ,textprops={'fontsize': 28})

    plt.setp(pcts, fontweight='bold')
    plt.setp(texts, fontweight=600)

    plt.title(title, size = 45,fontweight = 'bold')
    plt.show()

#행렬전환
cancer_age_rank5_1 = cancer_age_rank5.pivot(index='연령별',
                                            columns='연령별 발생자수 순위',
                                            values='발생자수 (명)').reset_index()

cancer_age_rank5_2 = cancer_age_rank5.pivot(index='연령별',
                                            columns='연령별 발생자수 순위',
                                            values='24개 암종별').reset_index()

    
# #컬럼정리
cancer_age_rank5_1.columns=cancer_age_rank5_1.columns.values
cancer_age_rank5_2.columns=cancer_age_rank5_2.columns.values

cancer_age_rank5_1=cancer_age_rank5_1.reindex([6,0,1,2,3,4,5])
cancer_age_rank5_2=cancer_age_rank5_2.reindex([6,0,1,2,3,4,5])

display(cancer_age_rank5_1)  

display(cancer_age_rank5_2)
    
#다중막대그래프
cancer_age_rank5_1.plot(kind='bar',x='연령별', rot=0,figsize=(17,6))
plt.ylabel('발생자수')
plt.legend().remove()
plt.title('연령별 top5암 발생자수',size=25,pad=15)

plt.show()
    
#연도별 전체 암 발생 추이    
cancer_all = cancer.copy().loc[(cancer['성별']=='계')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 &(cancer['연령별']=='계') 
                 ,]
cancer_m = cancer.copy().loc[(cancer['성별']=='남자')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 &(cancer['연령별']=='계') 
                 ,]
cancer_w = cancer.copy().loc[(cancer['성별']=='여자')
                 &(cancer['24개 암종별']=='모든 암(C00-C96)')
                 &(cancer['연령별']=='계') 
                 ,]

fig, ax1 = plt.subplots()
ax1.plot(cancer_all['시점'], cancer_all['조발생률 (명/10만명)'],marker='o',color='#696969',label='남녀')
ax1.plot(cancer_w['시점'], cancer_w['조발생률 (명/10만명)'],marker='o',color='#FF69B4',label='여자')
ax1.plot(cancer_m['시점'], cancer_m['조발생률 (명/10만명)'],marker='o',color='#00BFFF',label='남자')
ax1.set_xticks(np.arange(2016,2021))
ax1.set_yticks(np.arange(0,750,50))
ax1.set_xlabel('시점')
ax1.set_ylabel('10만 명당 암 발생률')

ax2 = ax1.twinx()
ax2.bar(cancer_all['시점'], cancer_all['발생자수 (명)'], color='#696969', label='남녀', alpha=0.2, width=0.5)
ax2.set_ylabel(f'발생자수')
ax2.set_yticks(np.arange(0,500000,50000))
ax1.legend(title = "발생률",loc='upper left')
ax2.legend(title = "발생자수",loc='upper right')

plt.show()

