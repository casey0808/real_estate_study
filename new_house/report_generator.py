def report_generator(file_path1, file_path2):
    import numpy as np
    import pandas as pd
    from IPython.display import display
    
    # read excel files
    df1 = pd.read_excel(file_path1, sheet_name = 1, index_col= 0, header = 1, usecols = range(41), skipfooter = 17)
    df2 = pd.read_excel(file_path2, sheet_name = 6, index_col= 0, header = 0, usecols = range(46), skipfooter = 0)
    
    cols = [0, 3, 5, 8, 10, 13, 15, 18]
    df3 = pd.read_excel(file_path2, sheet_name = 1, header = 0, usecols = cols, skipfooter = 3)
    df4 = pd.read_excel(file_path2, sheet_name = 2, header = 0, usecols = cols, skipfooter = 6)
    df5 = pd.concat([df3.tail(2), df4.tail(2)], axis = 1)
    
    # check the data 
    display(df1.tail(2))
    display(df2.tail(2))
    display(df5.tail(2))
    
    report = pd.read_excel('一手住宅简报格式.xlsx', sheet_name = 1, header = 0, index_col = 0,
                      skipfooter = 33, usecols = range(0, 45))
    display(report.tail(2))
    
    # generate supply and sales data of new houses in 40 cities
    cities = list(report.columns[4:])
    dict = {}
    for i in cities:
        dict[i] = [df1[i][-1], df2[i][-1]]

    result = pd.DataFrame(dict, index = ['40城住宅成交', '40城住宅供应'])
    
    
    # generate new house prices in 8 major cities
    dict2 = {}
    k = 0
    j = 1
    while j <= 15:
        dict2[df5.columns[k]] = df5.iloc[-1, j]
        k = k + 2
        j = j + 2

    result2 = pd.DataFrame(dict2, index = [df5.iloc[-1, 0]])
    
    # write the results into one excel file
    writer = pd.ExcelWriter('result_newhouse.xlsx')
    result.to_excel(writer, sheet_name = 'supply_and_sales')
    result2.to_excel(writer, sheet_name = 'prices')
    writer.save()
    
    return

print('运行 report_generator(40城，20城)')
