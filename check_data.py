import pandas as pd

# 读取Excel文件
df = pd.read_excel('c:/Users/Administrator/Desktop/txt/data/清洗后_广州_houses.xlsx')

print('图片链接示例:')
for i in range(3):
    print(f'{i+1}. {df.iloc[i]["图片链接"]}')

print('\n标签示例:')
for i in range(3):
    print(f'{i+1}. {df.iloc[i]["标签"]}')

print('\n房屋朝向示例:')
for i in range(3):
    print(f'{i+1}. {df.iloc[i]["房屋朝向"]}')

print('\n是否有电梯示例:')
for i in range(3):
    print(f'{i+1}. {df.iloc[i]["是否有电梯"]}')

print('\n所有唯一的标签值:')
print(df['标签'].unique()[:10])  # 显示前10个唯一标签

print('\n所有唯一的房屋朝向:')
print(df['房屋朝向'].unique())

print('\n所有唯一的是否有电梯:')
print(df['是否有电梯'].unique())