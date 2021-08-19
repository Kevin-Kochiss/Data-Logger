import pandas as pd
import xlsxwriter
from pathlib import Path
import ntpath

def write_to_xlsx(csv_path, dest_path):
    '''Reads the raw csv and converts it to an excel file, saving it to
    the destination provided.
    param   file_path   The location of the csv to be processed
    param   dest_path   The location where the excel file will be saved
    '''
    xlsx_name = csv_to_xlsx(csv_path)
    xlsx_file = Path(dest_path, xlsx_name)
    df_raw = pd.read_csv(csv_path, skiprows=25, usecols=[1,3,4,5,6,7,8])
    date = df_raw.iloc[0]['Time'].split()
    date = date[0]
    df_raw['Time'] = df_raw['Time'].apply(func=convert_date_time)
    df_graphs = pd.DataFrame()
    try:
        with pd.ExcelWriter(xlsx_file, engine='xlsxwriter') as writer:

            df_graphs.to_excel(writer, index=False, sheet_name='Graphs')
            df_raw.to_excel(writer, index=False, sheet_name='Raw Data')
            workbook = writer.book
            worksheet = writer.sheets['Graphs']
            chart = workbook.add_chart({'type': 'line'})
            
            chart.add_series({
                                'categories': ['Raw Data', 1, 0, 7, 0],
                                'values':     ['Raw Data', 1, 1, 7, 1],
                            })
            chart.set_title({'name':'Test Chart'})
            chart.set_style(10)
            chart.set_x_axis({'name': 'Time', 'position_axis': 'on_tick'})
            chart.set_y_axis({'name': 'Load'})
            chart.set_legend({'position': 'none'})
            worksheet.write('A1', "Date:")
            worksheet.write('B1', str(date))
            worksheet.insert_chart('A2', chart)

    except:
        #TODO: Exception handling
        print('Exextption')
        pass
    workbook = xlsxwriter.Workbook('chart_line.xlsx')
    worksheet = workbook.add_worksheet()
    
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

write_to_xlsx(r'C:\Users\kevin\Downloads\Test Lot#98232.csv', r'C:\Users\kevin\Desktop')
#csv_to_xlsx(r'C:\Users\kevin\Downloads\Test Lot#98232.csv')