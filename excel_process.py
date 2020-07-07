import xlrd

data = xlrd.open_workbook('./NLP_human.xlsx')
table = data.sheet_by_name('Sheet1')

i = 1
filename = 'tech_news_human.txt'
while i < 51:
    with open(filename,'a') as f:
        f.write("第"+i.__str__()+"回\n")
        f.write(table.cell_value(i, 2))
        i += 1
