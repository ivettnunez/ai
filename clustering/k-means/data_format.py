import pandas as pd
import numpy as np

X = pd.read_csv("./players4.csv")
newCol = X['TOI/GP'].apply(lambda x: float(x) if x == x else "")

X.loc[((X['TOI/GP'] >= 1.733333333) & (X['TOI/GP'] < 3.933333333)), 'test'] = 1
X.loc[((X['TOI/GP'] > 3.932333333) & (X['TOI/GP'] < 6.132333333)), 'test'] = 2
X.loc[((X['TOI/GP'] > 6.131333333) & (X['TOI/GP'] < 8.331333333)), 'test'] = 3
X.loc[((X['TOI/GP'] > 8.330333333) & (X['TOI/GP'] < 10.53033333)), 'test'] = 4
X.loc[((X['TOI/GP'] > 10.52933333) & (X['TOI/GP'] < 12.72933333)), 'test'] = 5
X.loc[((X['TOI/GP'] > 12.72833333) & (X['TOI/GP'] < 14.92833333)), 'test'] = 6
X.loc[((X['TOI/GP'] > 14.92733333) & (X['TOI/GP'] < 17.12733333)), 'test'] = 7
X.loc[((X['TOI/GP'] > 17.12633333) & (X['TOI/GP'] < 19.32633333)), 'test'] = 8
X.loc[((X['TOI/GP'] > 19.32533333) & (X['TOI/GP'] < 21.52533333)), 'test'] = 9
X.loc[((X['TOI/GP'] > 21.52433333) & (X['TOI/GP'] < 23.72433333)), 'test'] = 10
X.loc[((X['TOI/GP'] > 23.72333333) & (X['TOI/GP'] < 25.92333333)), 'test'] = 11

print(X['test'])
X['TOI/GP'] = X['test'].values
X.to_csv('players5.csv', encoding='utf-8', index=False)

'''
#Teams

#ANA  1
#ARI  2
#BOS  3
#BUF  4
#CAR 5
#CBJ 6
#CGY 7
#CHI 8
#COL 9
#DAL 10
#DET 11
#EDM 12
#FLA 13
#LAK 14
#MIN 15
#MTL 16
#NJD 17
#NSH 18
#NYI 19
#NYR 20
#OTT 21
#PHI 22
#PIT 23
#SJS 24
#STL 25
#TBL 26
#TOR 26
#VAN 28
#VGK 29
#WPG 30
#WSH 31

X = pd.read_csv("./players2.csv")

X.loc[X['Team'].str.contains("ANA"),'test'] = '1'
X.loc[X['Team'].str.contains("ARI"),'test'] = '2'
X.loc[X['Team'].str.contains("BOS"),'test'] = '3'
X.loc[X['Team'].str.contains("BUF"),'test'] = '4'
X.loc[X['Team'].str.contains("CAR"),'test'] = '5'
X.loc[X['Team'].str.contains("CBJ"),'test'] = '6'
X.loc[X['Team'].str.contains("CGY"),'test'] = '7'
X.loc[X['Team'].str.contains("CHI"),'test'] = '8'
X.loc[X['Team'].str.contains("COL"),'test'] = '9'
X.loc[X['Team'].str.contains("DAL"),'test'] = '10'
X.loc[X['Team'].str.contains("DET"),'test'] = '11'
X.loc[X['Team'].str.contains("EDM"),'test'] = '12'
X.loc[X['Team'].str.contains("FLA"),'test'] = '13'
X.loc[X['Team'].str.contains("LAK"),'test'] = '14'
X.loc[X['Team'].str.contains("MIN"),'test'] = '15'
X.loc[X['Team'].str.contains("MTL"),'test'] = '16'

X.loc[X['Team'].str.contains("NJD"),'test'] = '17'
X.loc[X['Team'].str.contains("NSH"),'test'] = '18'
X.loc[X['Team'].str.contains("NYI"),'test'] = '19'
X.loc[X['Team'].str.contains("NYR"),'test'] = '20'
X.loc[X['Team'].str.contains("OTT"),'test'] = '21'
X.loc[X['Team'].str.contains("PHI"),'test'] = '22'
X.loc[X['Team'].str.contains("PIT"),'test'] = '23'
X.loc[X['Team'].str.contains("SJS"),'test'] = '24'
X.loc[X['Team'].str.contains("STL"),'test'] = '25'
X.loc[X['Team'].str.contains("TBL"),'test'] = '26'
X.loc[X['Team'].str.contains("TOR"),'test'] = '27'
X.loc[X['Team'].str.contains("VAN"),'test'] = '28'
X.loc[X['Team'].str.contains("VGK"),'test'] = '29'
X.loc[X['Team'].str.contains("WPG"),'test'] = '30'
X.loc[X['Team'].str.contains("WSH"),'test'] = '31'

print(X['test'])
X['Team'] = X['test'].values
X.to_csv('players2.csv', encoding='utf-8', index=False)
'''



'''
#Position

#C  1
#R  2
#L  3
#D  4

X = pd.read_csv("./players2.csv")

X.loc[X['Position'].str.contains("C"),'test'] = '1'
X.loc[X['Position'].str.contains("R"),'test'] = '2'
X.loc[X['Position'].str.contains("L"),'test'] = '3'
X.loc[X['Position'].str.contains("D"),'test'] = '4'
#print(X['test'])
X['Position'] = X['test'].values
X.to_csv('players2.csv', encoding='utf-8', index=False)

'''


'''
# Time On Ice to float

X = pd.read_csv("./players2.csv")
new = X['TOI/GP'].str.split(":", n = 1, expand = True)
new[0] = new[0].apply(lambda x: int(x) if x == x else "")
new[2] = new[0] + (new[1]/60)

X['TOI/GP'] = new[2].values
print(X)
X.to_csv('players2.csv', encoding='utf-8', index=False)
'''


'''
#CSV format

dataFile = open('./players.csv','w')
i = 1;
with open('./players.txt') as f:
   for line in f:
       if(i%23 != 0):
           withCommas = line.replace('\n', ', ')
           dataFile.write(withCommas)
       else:
           dataFile.write(line)
       i+=1
'''
