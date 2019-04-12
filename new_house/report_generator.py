def report_generator(file_path1, file_path2):
    import numpy as np
    import pandas as pd
    from IPython.display import display

    df1 = pd.read_excel(file_path1, sheet_name = 1, index_col= 0, header = 1, usecols = range(41), skipfooter = 12)
    df2 = pd.read_excel(file_path2, sheet_name = 6, index_col= 0, header = 0, usecols = range(46), skipfooter = 32)
    
    display(df1.tail(2))
    display(df2.tail(2))
    report = pd.read_excel('一手住宅简报格式.xlsx', sheet_name = 1, header = 0, index_col = 0,
                      skipfooter = 33, usecols = range(0, 45))
    display(report.tail(2))
    
    cities = list(report.columns[4:])
    dict = {}
    for i in cities:
        dict[i] = [df1[i][-1], df2[i][-1]]


    result = pd.DataFrame(dict, index = ['40城住宅成交', '40城住宅供应'])
    
    result.to_excel('result.xlsx')
    return

print('运行 report_generator(40城，20城)')
