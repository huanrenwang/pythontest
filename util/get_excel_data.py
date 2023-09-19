dates=pd.date_range('20180310',periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=['A','B','C','D'])#生成6行4列位置
print(df)#输出6行4列的表格
'''
                   A         B         C         D
2018-03-10 -0.092889 -0.503172  0.692763 -1.261313
2018-03-11 -0.895628 -2.300249 -1.098069  0.468986
2018-03-12  0.084732 -1.275078  1.638007 -0.291145
2018-03-13 -0.561528  0.431088  0.430414  1.065939
2018-03-14  1.485434 -0.341404  0.267613 -1.493366
2018-03-15 -1.671474  0.110933  1.688264 -0.910599
  '''
print(df['B'])
'''
2018-03-10   -0.927291
2018-03-11   -0.406842
2018-03-12   -0.088316
2018-03-13   -1.631055
2018-03-14   -0.929926
2018-03-15   -0.010904
Freq: D, Name: B, dtype: float64
 '''
print()
#创建特定数据的DataFrame
df_1=pd.DataFrame({'A' : 1.,
                    'B' : pd.Timestamp('20180310'),
                    'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                    'D' : np.array([3] * 4,dtype='int32'),
                    'E' : pd.Categorical(["test","train","test","train"]),
                    'F' : 'foo'
                    })
print(df_1)
'''
     A          B    C  D      E    F
0  1.0 2018-03-10  1.0  3   test  foo
1  1.0 2018-03-10  1.0  3  train  foo
2  1.0 2018-03-10  1.0  3   test  foo
3  1.0 2018-03-10  1.0  3  train  foo
'''
print(df_1.dtypes)
'''
A           float64
B    datetime64[ns]
C           float32
D             int32
E          category
F            object
dtype: object
'''
print(df_1.index)#行的序号
#Int64Index([0, 1, 2, 3], dtype='int64')
print(df_1.columns)#列的序号名字
#Index(['A', 'B', 'C', 'D', 'E', 'F'], dtype='object')
print(df_1.values)#把每个值进行打印出来
'''
[[1.0 Timestamp('2018-03-10 00:00:00') 1.0 3 'test' 'foo']
 [1.0 Timestamp('2018-03-10 00:00:00') 1.0 3 'train' 'foo']
 [1.0 Timestamp('2018-03-10 00:00:00') 1.0 3 'test' 'foo']
 [1.0 Timestamp('2018-03-10 00:00:00') 1.0 3 'train' 'foo']]
 '''
print(df_1.describe())#数字总结
'''
         A    C    D
count  4.0  4.0  4.0
mean   1.0  1.0  3.0
std    0.0  0.0  0.0
min    1.0  1.0  3.0
25%    1.0  1.0  3.0
50%    1.0  1.0  3.0
75%    1.0  1.0  3.0
max    1.0  1.0  3.0
'''
print(df_1.T)#翻转数据
'''
                     0                    1                    2  \
A                    1                    1                    1   
B  2018-03-10 00:00:00  2018-03-10 00:00:00  2018-03-10 00:00:00   
C                    1                    1                    1   
D                    3                    3                    3   
E                 test                train                 test   
F                  foo                  foo                  foo   

                     3  
A                    1  
B  2018-03-10 00:00:00  
C                    1  
D                    3  
E                train  
F                  foo  
'''
print(df_1.sort_index(axis=1, ascending=False))#axis等于1按列进行排序 如ABCDEFG 然后ascending倒叙进行显示
'''
     F      E  D    C          B    A
0  foo   test  3  1.0 2018-03-10  1.0
1  foo  train  3  1.0 2018-03-10  1.0
2  foo   test  3  1.0 2018-03-10  1.0
3  foo  train  3  1.0 2018-03-10  1.0
'''
print(df_1.sort_values(by='E'))#按值进行排序
'''
     A          B    C  D      E    F
0  1.0 2018-03-10  1.0  3   test  foo
2  1.0 2018-03-10  1.0  3   test  foo
1  1.0 2018-03-10  1.0  3  train  foo
3  1.0 2018-03-10  1.0  3  train  foo
'''
