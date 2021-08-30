import os
import pandas as pd
import xlsxwriter
from pathlib import Path
import ntpath
from configuration import ScriptVars

def write_to_xlsx(csv_path, dest_path):
    '''Reads the raw csv and converts it to an excel file, saving it to
    the destination provided.
    param   file_path   The location of the csv to be processed
    param   dest_path   The location where the excel file will be saved
    '''
    xlsx_name = csv_to_xlsx(csv_path)
    xlsx_file = Path(dest_path, xlsx_name)
    xlsx_file = check_file_name(xlsx_file)
    config = ScriptVars()      
    df_raw = pd.read_csv(
        csv_path, 
        skiprows=config.config['HEADER_ROW'] - 1, 
        usecols=config.config['COLUMNS']
        )
    df_raw.dropna(inplace = True)
    try:
        date = df_raw.iloc[0]['Time'].split()
    except:
        config.write_error('Time column was not found in the provided csv.  Check HEADER_ROW and COLUMNS', True)
        return False
    date = date[0]
    df_raw['Time'] = df_raw['Time'].apply(func=convert_date_time)
    headers = list(df_raw.columns)
    df_graphs = pd.DataFrame()
   
    try:
        with pd.ExcelWriter(xlsx_file, engine='xlsxwriter') as writer:

            df_graphs.to_excel(writer, index=False, sheet_name='Graphs')
            df_raw.to_excel(writer, index=False, sheet_name='Raw Data')
            workbook = writer.book
            worksheet = writer.sheets['Graphs']
            worksheet.write(0,0,'Line 7')
            worksheet.write(1,0, xlsx_name.split('.')[0])
            worksheet.write(2,0, 'Date(Y-M-D): {}'.format(date))
            offset = 4
            chart_num = 0
            for index, column in enumerate(df_raw):
                if column == 'Time' or column == 'degF.1' or column == 'degF.2':
                    continue
                num_entries = len(df_raw[column])                    
                chart = make_chart(workbook=workbook, worksheet=worksheet,column=column, index=index, num_entries=num_entries)
                cell = 'A{}'.format(((index-1)*30)+offset)
                worksheet.insert_chart(cell, chart, {'x_scale': 2, 'y_scale': 2})
                chart_num += 1
            #determine a way to make this programtically, could use single columns, mulichart in settings
            cols = ['degF.1', 'degF.2']
            pairs = [[x,y] for x, y in enumerate(df_raw) if y in cols]
            mulit_chart  = make_multi_chart(workbook=workbook, 
                worksheet=worksheet, columns=['degF.1', 'degF.2'], 
                data_frame=df_raw, num_entries=num_entries, chart_title='Temperature vs Time', 
                y_axis='Temperature (F)'
                )
            cell = 'A{}'.format((chart_num*30)+offset)
            worksheet.insert_chart(cell, mulit_chart, {'x_scale': 2, 'y_scale': 2})

    except:
        ScriptVars().write_error('Error encountered when attempting to write the excell file.  Ensure that the file is not open.')
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

def make_chart(workbook, worksheet, num_entries, index, column):
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
    chart.set_title({'name':'{} vs Time'.format(to_title(column))})
    chart.set_x_axis({'name': 'Time', 'position_axis': 'on_tick', 'name_font': {'size': 16, 'bold': True}} )
    chart.set_y_axis({'name': column, 'name_font': {'size': 16, 'bold': True}})
    chart.set_legend({'position': 'none'})
    return chart

def make_multi_chart(workbook, worksheet, num_entries, columns, data_frame, chart_title, y_axis):
    """
    Parameters
    ----------
    workbook  :  workbook
    worksheet  :  worksheet
    num_entries  :  int
        `num_entries` is the number of row elements to use
    columns  :  list
        `indexs` a list of column names to be plotted
    data_frame  :  data frame
        `data_frame` is that data frame to be refernced
    chart_title  :  str
        `chart_title` is the string to be used as the tittle
    y_axis  :  str
        `y_axis` is the title for the y-axis
    """
    
    chart = workbook.add_chart({'type': 'line'})
    pairs = [[x,y] for x, y in enumerate(data_frame) if y in columns]
    for index, column in pairs:    
        chart.add_series({
                        'name': to_title(column),
                                #     [sheetname, first_row, first_col, last_row, last_col]
                        'categories': ['Raw Data', 1, 0, num_entries, 0],
                        'values':     ['Raw Data', 1, index, num_entries, index],
                        'line': {'width':2}
                    })
    chart.set_style(10)
    chart.set_title({'name': chart_title})
    chart.set_x_axis({'name': 'Time', 'position_axis': 'on_tick', 'name_font': {'size': 16, 'bold': True}} )
    chart.set_y_axis({'name': y_axis, 'name_font': {'size': 16, 'bold': True}})
    chart.set_legend({'font': {'size': 9, 'bold': True}})
    return chart

def write_chart_info(worksheet, date):
    worksheet.write('A1', "Date:")
    worksheet.write('B1', str(date))

def to_title(column):
    tittle_dict = {
        'Time': 'Time',
        '%LOAD': '% Load',
        'degF': 'Melt Temperature',
        'RPM' : 'RPM',
        'PSI' : 'PSI',
        'degF.1':'degF.1',
        'degF.2':'degF.2',
    }
    try:
        return tittle_dict[column]
    except:
        return column

def check_file_name(file_name):
    """ Checks if a file with this name already exists in the directoy.
        Appends a version string if it does, and upadates if a version is already there.
        Returns the new file name
    """
    if Path(file_name).exists():
        ls = list(os.path.splitext(file_name))
        if(ls[0].endswith(')')):
            ls[0] = ls[0].rsplit('(', 1)
            version = int(''.join(c for c in ls[0][1] if c.isdigit()))
            version += 1
            version = '({})'.format(version)
            ls[0][1] = version
            ls[0] = ''.join(ls[0])
        else:
            ls[0] += '(1)'
        new_name =  ''.join(ls)
        next_name = check_file_name(new_name)
        if new_name == next_name:
            return new_name
        else:
            return check_file_name(next_name)
    else:
        return file_name

