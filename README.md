# tushare-downloader
some silly functions used to download data from http://tushare.org

For easy understanding, there are two series of functions, including three functions each.

1. Downloading day,week,month,60minutes, 30minutes,15minutes and 5minutes date.including the following functions:

    1.1 ts_get_stock_data(code,start,end,destination,tools_dir,auto_rename)
        getting above-mentioned data of one particular stock code for specified period and saving accordingly.
        
    1.2 ts_get_list_stock_data(codes,start,end,destination,tools_dir,auto_rename)
        getting above-mentioned data for a list of stock codes for specified period and saving accrodingly.
        
    1.3 ts_get_all_stock_data(start,end,destination,tools_dir,auto_rename) 
        getting above-mentioned data for all stock codes listed in stock_code_list.csv(all for SH&SZ) for specified period and svaing accordingly

2. Downloading tick data

    2.1 ts_get_tick_data()
        getting tick data of one specified code for specified date period
        
    2.2 ts_get_list_tick_data()
        refer to 1.2
        
    2.3 ts_get_all_tick_data() 
        refer to 13
        
    note: destination: directory for saving data as .csv file. tools_dir: location of related files(i.e stock_code_list.csv).auto_rename: True or False. If True, it will rename the file by denoting real period of data downloaded, rather then the data period specified in parameters

ts_get_index_data() is a similar function as get_list_stock_data(). It is made purely for downloading Index Data(HS300....) in one shoot


