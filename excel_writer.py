import pandas as pd
import xlsxwriter
from pathlib import Path
import ntpath

tittle_dict = {'Time': '(s)',
            '%LOAD': '(%)',
            'degF': 'Melt Temperature',
            'RPM' : '(rpm)',
            'PSI' : '(psi)',
}

def write_to_xlsx(csv_path, dest_path):
    '''Reads the raw csv and converts it to an excel file, saving it to
    the destination provided.
    param   file_path   The location of the csv to be processed
    param   dest_path   The location where the excel file will be saved
    '''
    xlsx_name = csv_to_xlsx(csv_path)
    xlsx_file = Path(dest_path, xlsx_name)
    df_raw = pd.read_csv(csv_path, skiprows=25, usecols=[1,3,4,5,6,7,8])
    df_raw.dropna(inplace = True)
    date = df_raw.iloc[0]['Time'].split()
    date = date[0]
    df_raw['Time'] = df_raw['Time'].apply(func=convert_date_time)
    headers = list(df_raw.columns)

    for index, column in enumerate(df_raw):
        if column == 'Time':
            continue
        entries = len(df_raw[column])

    df_graphs = pd.DataFrame()
   
    try:
        with pd.ExcelWriter(xlsx_file, engine='xlsxwriter') as writer:

            df_graphs.to_excel(writer, index=False, sheet_name='Graphs')
            df_raw.to_excel(writer, index=False, sheet_name='Raw Data')
            workbook = writer.book
            worksheet = writer.sheets['Graphs']
            for index, column in enumerate(df_raw):
                if column == 'Time':
                    continue
                num_entries = len(df_raw[column])
                add_chart(workbook=workbook, worksheet=worksheet,column=column, index=index, num_entries=num_entries)

    except:
        #TODO: Exception handling
        print('Exextption')
        return False
    return True
    
def convert_date_time(cell):
    '''Strips the date from date time'''
    ls = cell.split()
    return ls.pop()

def csv_to_xlsx(file_path):
    '''Generates the new excel file name to be appened to the new save location'''
    head, tail = ntpath.split(file_path)
    new_name = tail or ntpath.basename(head)
    ls = str(new_name).split('.')
    ls.pop()
    ls.append('xlsx')
    new_name = '.'.join(ls)
    return new_name

def add_chart(workbook, worksheet, num_entries, index, column):
    '''
    Function to add a chart to a worksheet given
    num_entries == length of the data set
    index == The index of the data set
    column == the header of the data set
    '''      
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
                                #     [sheetname, first_row, first_col, last_row, last_col]
                        'categories': ['Raw Data', 1, 0, num_entries, 0],
                        'values':     ['Raw Data', 1, index, num_entries, index],
                        'line': {'width':2}
                    })
    chart.set_style(10)
    chart.set_title({'name':'{} vs Time'.format(column)})
    chart.set_x_axis({'name': 'Time', 'position_axis': 'on_tick', 'name_font': {'size': 16, 'bold': True}} )
    chart.set_y_axis({'name': column, 'name_font': {'size': 16, 'bold': True}})
    chart.set_legend({'position': 'none'})
    cell = 'A{}'.format(((index-1)*30)+1)
    worksheet.insert_chart(cell, chart, {'x_scale': 2, 'y_scale': 2})

def write_chart_info(worksheet, date):
    worksheet.write('A1', "Date:")
    worksheet.write('B1', str(date))

#Test line
#write_to_xlsx(r'C:\Users\kevin\Downloads\Test Lot#98232.csv', r'C:\Users\kevin\Desktop')

