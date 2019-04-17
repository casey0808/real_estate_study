def secondery_market_monthly(file_path):
    
    from IPython.display import display
    
    import numpy as np
    import pandas as pd
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    df = pd.read_excel(file_path)
    
    check = ['满懿（上海）房地产', '上海搜房房天下房地产']
    for a in df['中介公司']:
        if a in check:
            print('recheck agency!', a)
            break
    
    num = df['中介公司'].count()
    avg_price = df['总价'].mean()
    avg_area = df['面积'].mean()
    total_amount = df['总价'].sum()
    
    agency = ['上海中原物业', '上海汉宇房地产', '上海我爱我家房地产', '上海太平洋房屋', 
          '德佑房地产', '上海云房数据', '上海易居房地产', '上海志远房地产']
    
    dict1 = {}
    for a in agency:
        dict1[a] = [df['总价'][df['中介公司'] == a].count()/num, 
                   df['总价'][df['中介公司'] == a].sum()/total_amount]
    result1 = pd.DataFrame(dict1, index = ['单数市占', '金额市占'])
    
    x = [1, 6, 7, 8, 10, 11]
    y = ['宝原', '链家', '搜房', '满懿', '房多多', '房好多']
    
    for x1, y1 in zip(x, y):
        result1.insert(x1, y1, [0, 0])
    
    
    dict2 = {'成交套数': num, '套均价格': avg_price/10000, '套均面积': avg_area}
    result2 = pd.DataFrame(dict2, index = [file_path[2:4]])
    
    writer = pd.ExcelWriter('result.xlsx')
    result2.to_excel(writer, '成交量价')
    result1.to_excel(writer, '中介市占')
    writer.save()
    
    display(result2)
    print('全市场成交金额: ', total_amount/1e8)
    display(result1)
    
    
    
secondery_market_monthly('上海3月EDS数据.xlsx')
