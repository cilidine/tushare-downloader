#-*- coding: UTF-8 -*-
def ts_get_all_stock_data(start='',end='',destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',auto_rename=True):
	'''
	description: get month, week, day, 60 minutes, 30 minutes, 15 minutes, 5 minutes data for  all stocks(stored in .../tools/stock_code_list.csv)
	during period indicated by para:start and para:end, and save as local files into designated location(see para:destination)
	parameters:
	codes(list) - a group of codes 
	
	'''
	import sys
	import pandas as pd

	sys.path.append(tools_dir)
	stock_code_list=pd.read_csv(tools_dir+'stock_code_list.csv',dtype=str)
	if stock_code_list.shape[0]==0:# empty list
		print 'no stock code to download, quit'
		return

	for i in range(0,stock_code_list.shape[0]):
		ts_get_stock_data(stock_code_list['code'][i],start,end,destination=destination,tools_dir=tools_dir,auto_rename=auto_rename)
		print str(i+1)+'finished/'+str(stock_code_list.shape[0])+'in total'
	
def ts_get_list_stock_data(codes,start='',end='',destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',auto_rename=True):
	'''
	description: get month, week, day, 60 minutes, 30 minutes, 15 minutes, 5 minutes data for  a group of specified stocks(see para:codes)
	during period indicated by para:start and para:end, and save as local files into designated location(see para:destination)
	parameters:
	codes(list) - a group of codes 

	'''
	codes=list(codes)#in case user give non-list parameter
	if len(codes)==0:# empty list
		print 'no stock code to download, quit'
		return
	if len(codes)==1:# only one code in list
		ts_get_stock_data(codes[0],start,end,destination=destination,tools_dir=tools_dir,auto_rename=auto_rename)

	for code in codes:
		ts_get_stock_data(code,start,end,destination=destination,tools_dir=tools_dir,auto_rename=auto_rename)

	print 'data of '+codes[0]+'...'+codes[-1]+' ['+str(len(codes))+'] stock(s) in total have been downloaded and saved!' 

def ts_get_stock_data(code,start='',end='',destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',auto_rename=True):
	'''
	description: get month, week, day, 60 minutes, 30 minutes, 15 minutes, 5 minutes data for one specified stock(see para:code)
	during period indicated by para:start and para:end, and save as local files into designated location(see para:destination)
	parameters:
	auto_rename(bool) - default True. if True, a date period will be attachd onto file name indicating the real period of records that file contents. 
	start&end(str) -  default(either of them is '') will get three year back from today
	'''
	import tushare as ts
	if start=='' or end=='':
		_Day=ts.get_hist_data(code,ktype='D',retry_count=10)
		_Week=ts.get_hist_data(code,ktype='W',retry_count=10)
		_Month=ts.get_hist_data(code,ktype='M',retry_count=10)
		_5minutes=ts.get_hist_data(code,ktype='5',retry_count=10)
		_15minutes=ts.get_hist_data(code,ktype='15',retry_count=10)
		_30minutes=ts.get_hist_data(code,ktype='30',retry_count=10)
		_60minutes=ts.get_hist_data(code,ktype='60',retry_count=10)
	else:
		_Day=ts.get_hist_data(code,start=start,end=end,ktype='D',retry_count=10)
		_Week=ts.get_hist_data(code,start=start,end=end,ktype='W',retry_count=10)
		_Month=ts.get_hist_data(code,start=start,end=end,ktype='M',retry_count=10)
		_5minutes=ts.get_hist_data(code,start=start,end=end,ktype='5',retry_count=10)
		_15minutes=ts.get_hist_data(code,start=start,end=end,ktype='15',retry_count=10)
		_30minutes=ts.get_hist_data(code,start=start,end=end,ktype='30',retry_count=10)
		_60minutes=ts.get_hist_data(code,start=start,end=end,ktype='60',retry_count=10)
	
	pre_name=code
	names=locals()#get variable name space(list), in order to access variables(dataframes return back from ts.get_hist_data())
	cur_file_name=''
	for each in ['_Day','_Week','_Month','_5minutes','_15minutes','_30minutes','_60minutes']:
		if names[each] is None:#got no data back
			print '['+pre_name+each+'_'+start+'-'+end+'] got no feed back from ts.get_hist_data(), skip'
			continue
		if names[each].shape[0]==0:
			print '['+pre_name+each+'_'+start+'-'+end+'] got no record back, skip'
			continue
		if auto_rename==True:#if user want the file name to be automatically revised(date period section) according to real data content
			cur_file_name = pre_name+each+'_'+names[each].index[-1][:10]+'-'+names[each].index[0][:10]+'(orig_period:'+start+'-'+end+')'
		else:
			cur_file_name = pre_name+each+'_'+start+'-'+end

		ts_save_data(names[each],filename=cur_file_name,destination=destination,append=False,dl_registration=True)
	print code+' history data(_D _W _M _5 _15 _30 _60) has been downloaded and saved successfully!!'


def ts_get_index_data(start='',end='',destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',auto_rename=True):
	'''
	notice: in order to save memory, this function could be revised: save immediately after one index(SH,SZ,HS300...) is downloaded.
	description: get index data of SH,SZ,HS300,SZ50,ZXB and CYB by different periods(month,weak,day,60,30,15,5),
	during period indicated by para:start and para:end, and save as local files into designated location(see para:destination)
	'''
	import tushare as ts
	import sys

	sys.path.append(tools_dir)
	if start=='' or end=='':
		SH_Day=ts.get_hist_data('sh',ktype='D',retry_count=10)
		SH_Week=ts.get_hist_data('sh',ktype='W',retry_count=10)
		SH_Month=ts.get_hist_data('sh',ktype='M',retry_count=10)
		SH_5minutes=ts.get_hist_data('sh',ktype='5',retry_count=10)
		SH_15minutes=ts.get_hist_data('sh',ktype='15',retry_count=10)
		SH_30minutes=ts.get_hist_data('sh',ktype='30',retry_count=10)
		SH_60minutes=ts.get_hist_data('sh',ktype='60',retry_count=10)
		SZ_Day=ts.get_hist_data('sz',ktype='D',retry_count=10)
		SZ_Week=ts.get_hist_data('sz',ktype='W',retry_count=10)
		SZ_Month=ts.get_hist_data('sz',ktype='M',retry_count=10)
		SZ_5minutes=ts.get_hist_data('sz',ktype='5',retry_count=10)
		SZ_15minutes=ts.get_hist_data('sz',ktype='15',retry_count=10)
		SZ_30minutes=ts.get_hist_data('sz',ktype='30',retry_count=10)
		SZ_60minutes=ts.get_hist_data('sz',ktype='60',retry_count=10)
		HS300_Day=ts.get_hist_data('hs300',ktype='D',retry_count=10)
		HS300_Week=ts.get_hist_data('hs300',ktype='W',retry_count=10)
		HS300_Month=ts.get_hist_data('hs300',ktype='M',retry_count=10)
		HS300_5minutes=ts.get_hist_data('hs300',ktype='5',retry_count=10)
		HS300_15minutes=ts.get_hist_data('hs300',ktype='15',retry_count=10)
		HS300_30minutes=ts.get_hist_data('hs300',ktype='30',retry_count=10)
		HS300_60minutes=ts.get_hist_data('hs300',ktype='60',retry_count=10)
		SZ50_Day=ts.get_hist_data('sz50',ktype='D',retry_count=10)
		SZ50_Week=ts.get_hist_data('sz50',ktype='W',retry_count=10)
		SZ50_Month=ts.get_hist_data('sz50',ktype='M',retry_count=10)
		SZ50_5minutes=ts.get_hist_data('sz50',ktype='5',retry_count=10)
		SZ50_15minutes=ts.get_hist_data('sz50',ktype='15',retry_count=10)
		SZ50_30minutes=ts.get_hist_data('sz50',ktype='30',retry_count=10)
		SZ50_60minutes=ts.get_hist_data('sz50',ktype='60',retry_count=10)
		ZXB_Day=ts.get_hist_data('zxb',ktype='D',retry_count=10)
		ZXB_Week=ts.get_hist_data('zxb',ktype='W',retry_count=10)
		ZXB_Month=ts.get_hist_data('zxb',ktype='M',retry_count=10)
		ZXB_5minutes=ts.get_hist_data('zxb',ktype='5',retry_count=10)
		ZXB_15minutes=ts.get_hist_data('zxb',ktype='15',retry_count=10)
		ZXB_30minutes=ts.get_hist_data('zxb',ktype='30',retry_count=10)
		ZXB_60minutes=ts.get_hist_data('zxb',ktype='60',retry_count=10)
		CYB_Day=ts.get_hist_data('cyb',ktype='D',retry_count=10)
		CYB_Week=ts.get_hist_data('cyb',ktype='W',retry_count=10)
		CYB_Month=ts.get_hist_data('cyb',ktype='M',retry_count=10)
		CYB_5minutes=ts.get_hist_data('cyb',ktype='5',retry_count=10)
		CYB_15minutes=ts.get_hist_data('cyb',ktype='15',retry_count=10)
		CYB_30minutes=ts.get_hist_data('cyb',ktype='30',retry_count=10)
		CYB_60minutes=ts.get_hist_data('cyb',ktype='60',retry_count=10)
	else:
		SH_Day=ts.get_hist_data('sh',start=start,end=end,ktype='D',retry_count=10)
		SH_Week=ts.get_hist_data('sh',start=start,end=end,ktype='W',retry_count=10)
		SH_Month=ts.get_hist_data('sh',start=start,end=end,ktype='M',retry_count=10)
		SH_5minutes=ts.get_hist_data('sh',start=start,end=end,ktype='5',retry_count=10)
		SH_15minutes=ts.get_hist_data('sh',start=start,end=end,ktype='15',retry_count=10)
		SH_30minutes=ts.get_hist_data('sh',start=start,end=end,ktype='30',retry_count=10)
		SH_60minutes=ts.get_hist_data('sh',start=start,end=end,ktype='60',retry_count=10)
		SZ_Day=ts.get_hist_data('sz',start=start,end=end,ktype='D',retry_count=10)
		SZ_Week=ts.get_hist_data('sz',start=start,end=end,ktype='W',retry_count=10)
		SZ_Month=ts.get_hist_data('sz',start=start,end=end,ktype='M',retry_count=10)
		SZ_5minutes=ts.get_hist_data('sz',start=start,end=end,ktype='5',retry_count=10)
		SZ_15minutes=ts.get_hist_data('sz',start=start,end=end,ktype='15',retry_count=10)
		SZ_30minutes=ts.get_hist_data('sz',start=start,end=end,ktype='30',retry_count=10)
		SZ_60minutes=ts.get_hist_data('sz',start=start,end=end,ktype='60',retry_count=10)
		HS300_Day=ts.get_hist_data('hs300',start=start,end=end,ktype='D',retry_count=10)
		HS300_Week=ts.get_hist_data('hs300',start=start,end=end,ktype='W',retry_count=10)
		HS300_Month=ts.get_hist_data('hs300',start=start,end=end,ktype='M',retry_count=10)
		HS300_5minutes=ts.get_hist_data('hs300',start=start,end=end,ktype='5',retry_count=10)
		HS300_15minutes=ts.get_hist_data('hs300',start=start,end=end,ktype='15',retry_count=10)
		HS300_30minutes=ts.get_hist_data('hs300',start=start,end=end,ktype='30',retry_count=10)
		HS300_60minutes=ts.get_hist_data('hs300',start=start,end=end,ktype='60',retry_count=10)
		SZ50_Day=ts.get_hist_data('sz50',start=start,end=end,ktype='D',retry_count=10)
		SZ50_Week=ts.get_hist_data('sz50',start=start,end=end,ktype='W',retry_count=10)
		SZ50_Month=ts.get_hist_data('sz50',start=start,end=end,ktype='M',retry_count=10)
		SZ50_5minutes=ts.get_hist_data('sz50',start=start,end=end,ktype='5',retry_count=10)
		SZ50_15minutes=ts.get_hist_data('sz50',start=start,end=end,ktype='15',retry_count=10)
		SZ50_30minutes=ts.get_hist_data('sz50',start=start,end=end,ktype='30',retry_count=10)
		SZ50_60minutes=ts.get_hist_data('sz50',start=start,end=end,ktype='60',retry_count=10)
		ZXB_Day=ts.get_hist_data('zxb',start=start,end=end,ktype='D',retry_count=10)
		ZXB_Week=ts.get_hist_data('zxb',start=start,end=end,ktype='W',retry_count=10)
		ZXB_Month=ts.get_hist_data('zxb',start=start,end=end,ktype='M',retry_count=10)
		ZXB_5minutes=ts.get_hist_data('zxb',start=start,end=end,ktype='5',retry_count=10)
		ZXB_15minutes=ts.get_hist_data('zxb',start=start,end=end,ktype='15',retry_count=10)
		ZXB_30minutes=ts.get_hist_data('zxb',start=start,end=end,ktype='30',retry_count=10)
		ZXB_60minutes=ts.get_hist_data('zxb',start=start,end=end,ktype='60',retry_count=10)
		CYB_Day=ts.get_hist_data('cyb',start=start,end=end,ktype='D',retry_count=10)
		CYB_Week=ts.get_hist_data('cyb',start=start,end=end,ktype='W',retry_count=10)
		CYB_Month=ts.get_hist_data('cyb',start=start,end=end,ktype='M',retry_count=10)
		CYB_5minutes=ts.get_hist_data('cyb',start=start,end=end,ktype='5',retry_count=10)
		CYB_15minutes=ts.get_hist_data('cyb',start=start,end=end,ktype='15',retry_count=10)
		CYB_30minutes=ts.get_hist_data('cyb',start=start,end=end,ktype='30',retry_count=10)
		CYB_60minutes=ts.get_hist_data('cyb',start=start,end=end,ktype='60',retry_count=10)

	names=locals()#get variable name space(list), in order to access variables(dataframes return back from ts.get_hist_data())
	cur_file_name=''
	for each_index in ['SH','SZ','HS300','SZ50','ZXB','CYB']:
		pre_name=each_index
		for each in ['_Day','_Week','_Month','_5minutes','_15minutes','_30minutes','_60minutes']:
			if auto_rename==True:#if user want the file name to be automatically revised(date period section) according to real data content
				cur_file_name = pre_name+each+'_'+names[pre_name+each].index[-1][:10]+'-'+names[pre_name+each].index[0][:10]+'(orig_period:'+start+'-'+end+')'
			else:
				cur_file_name = pre_name+each+'_'+start+'-'+end

			ts_save_data(names[pre_name+each],filename=cur_file_name,destination=destination,append=False,dl_registration=True)



def ts_get_all_tick_data(start,end,destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',continue_missed_allowed=90):
	'''
	description: download tick data for all stocks listed in file stock_code_list.csv(stored in .../tools/)
	parameters: 
	codes(list/Series/ndarray) - stock codes list to be downloaded
	start & end(str) - starting date and ending date
	destination(str) -  directory for file to be save and tools to be used
	continue_missed_allowed(int) - number of days allowed to miss(got no records), if exceed,
	function will quit and rename the data file(in consideration of having no further records there after)

	'''
	import pandas as pd
	import sys
	sys.path.append(tools_dir)
	stock_code_list=pd.read_csv(tools_dir+'stock_code_list.csv',dtype=str)
	for i in range(stock_code_list.shape[0]-1,-1,-1):
		print 'start downloading '+stock_code_list['code'][i]+' tick data...'
		ts_get_tick_data(stock_code_list['code'][i],start,end,destination=destination+'data/',continue_missed_allowed=continue_missed_allowed)
		if i ==0:
			print 'all stocks tick data downloaded successfully!!!!!'

def ts_get_list_tick_data(codes,start,end,destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',continue_missed_allowed=90,max_buffer=10000):
	'''
	description: download tick data for a list of stock (see para:codes)
	parameters: 
	codes(list/Series/ndarray) - stock codes list to be downloaded
	start & end(str) - starting date and ending date
	destination(str) -  directory for file to be save and tools to be used
	continue_missed_allowed(int) - number of days allowed to miss(got no records), if exceed,
	function will quit and rename the data file(in consideration of having no further records there after)

	'''

	import pandas as pd
	from pandas import Series,DataFrame
	#transfer list or ndarray into DataFrame type
	stock_code_list=Series(codes)
	stock_code_list.name='code'
	stock_code_list=DataFrame(stock_code_list)
	
	# if codes list contents only on code, call ts_get_tick_data()
	if stock_code_list.shape[0]==1:
		print 'only one stock code is given, calling ts_get_tick_data()...'
		ts_get_tick_data(stock_code_list['code'][0],start,end,destination=destination,continue_missed_allowed=continue_missed_allowed,max_buffer=max_buffer)
		return
	import sys
	sys.path.append(tools_dir)

	for i in range(stock_code_list.shape[0]-1,-1,-1):
		print 'start downloading '+stock_code_list['code'][i]+' tick data...'
		ts_get_tick_data(stock_code_list['code'][i],start,end,destination=destination,continue_missed_allowed=continue_missed_allowed)
		if i ==0:
			print 'all ['+str(len(stock_code_list))+'] stocks tick data downloaded successfully!!!!!'
def ts_get_tick_data(code,start,end,destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',continue_missed_allowed=90,auto_rename=False,max_buffer=10000):
	'''
	description: this function is designed to download tick data for one specified stock(see para:code), 
	during the period indicated by para:start and para:end.
	It will save downloaded data into local file acoording the directory given by para:destination, and
	name the file according to the period(para:start,end). the file name may vary in case downloading process is ceased 
	for diffirent reasons(continuelly got empty records for many days difined by para:continue_missed_allowed, or network failure...) 

	para: 
		code(str) - stock code to be downloaded(str), 
	    start & end(str) - starting and ending date(str)
	    destination(str) - directory for file to be save and tools(.py files including functions code, .csv files including necessary data) to be used
	    continue_missed_allowed(int) - number of days allowed to miss(got no records), if exceed, function will quit and rename the data file(in 
	      	consideration of having no further records there after)
		auto_rename(bool) - 
		max_buffer(int) - maximum lines allowed for df before save df into local file
	'''
	#check whether the data of same period has been downloaded and saved
	import os
	file_name=code+'_Tick_'+start+'-'+end#make up the file name first, for checking existence and final saving process
	revised_file_name=''
	
	if os.path.exists(destination+file_name+'.csv'):
		print 'file:['+destination+file_name+'.csv'+'] already exists, auto quit!!'
		return
	#import relative mudoles
	import tushare as ts
	import pandas as pd
	from pandas import DataFrame,Series
	import datetime
	from datetime import date,time
	import sys
    #make up a list of dates, in order to download everyday tick data acoording to datelist order
	start_date=datetime.datetime.strptime(start, "%Y-%m-%d").date()#data type transformation from str to datetime
	end_date=datetime.datetime.strptime(end, "%Y-%m-%d").date()#data type transformation from str to datetime
	dates=[start]#put the starting date in to the date list first
	new_date=start_date
	while True:
		new_date=new_date+datetime.timedelta(1)
		if new_date >=end_date:
			dates.append(end)
			break
		else:
			dates.append(new_date.strftime('%Y-%m-%d'))
	dates.reverse()#reverse the datelist order(download the recent days first, from ending date to starting date)
 	#downloading tick data day by day
	df=DataFrame()
	counter=0#counting how many days has ben tried to download(including all success and fail ones)
	size_counter=0#counting how many rows of records has been downloaded(including those have been saved)
	missed_counter=0#counting how may days failed
	continue_missed_counter=0#counting how may days have been continuelly failed(will be reseted once encounter one success)
	continue_missed_marker=False#marker for continue_missed_counter
	first_save_marker=True
	#file_name=code+'_Tick_'+start+'-'+end
	columns=[]
	for each in dates:
		counter+=1
		df_new = ts.get_tick_data(code,date=each)#calling tushare function to actually download data of a percific day
		if df_new is not None and df_new.shape[0]>2:#if df_new got something and records amount exceed 2
			if df_new['time'][1]!='window.close();':#if the records are not standerd response from tushare indicating "no data"
				df_new[u'date']=each#add new column for data frame, including date column(tushare.get_tick_data() returns no date info)
				#re-order the columns, to make 'date' at front
				temp=df_new['date']
				df_new.drop(labels=['date'],axis=1,inplace=True)
				df_new.insert(0,'date',temp)
				#append df_new into df
				df=df.append(df_new,ignore_index=True)#append data of current day into one dataframe for one stock(see para:code)
				continue_missed_marker=False#a new data has been gotten for a new day, mark the marker for continue_missed_counter
				continue_missed_counter=0#and reset continue_missed_counter
				size_counter+=df_new.shape[0]
				#print out info for success
				sys.stdout.write('\r'+' ['+code+'] tick data   got    on date:['+each+'][No.'+str(counter)+'/'+str(len(dates))+', '+str(counter-missed_counter)+'got'+'/'+str(missed_counter)+'missed'+']current data size: ['+str(df.shape[0])+'/'+str(size_counter)+'lines]...')
				sys.stdout.flush()

			else:
				missed_counter+=1
				continue_missed_marker=True
				continue_missed_counter+=1
				#print out info of failure for current day
				sys.stdout.write('\r'+' ['+code+'] tick data [missed] on date:['+each+'][No.'+str(counter)+'/'+str(len(dates))+', '+str(counter-missed_counter)+'got'+'/'+str(missed_counter)+'missed'+']current data size: ['+str(df.shape[0])+'/'+str(size_counter)+'lines]...')
				sys.stdout.flush()
				#check if continues_missed_counter has excced the tolerance(see para:continue_missed_allowed,default=90)
				if continue_missed_counter>continue_missed_allowed:
					#print out info, notice the user that the function is going to quit due to continuous missing of data
					print '\n'+code+' many days tick data unavailable, auto break!!!! (file name will be adjusted)'
					revised_file_name=code+'_Tick_'+each+'-'+end#revise the file name, mainly the period.
					break#quit iteration
		else:
			continue_missed_marker=True
			continue_missed_counter+=1
			missed_counter+=1
			#print out info of failure for current day
			sys.stdout.write('\r'+' ['+code+'] tick data missed on date:['+each+'][No.'+str(counter)+'/'+str(len(dates))+', '+str(counter-missed_counter)+'got'+'/'+str(missed_counter)+'missed'+']current data size: ['+str(df.shape[0])+'/'+str(size_counter)+'lines]...')
			sys.stdout.flush()
			#check if continues_missed_counter has excced the tolerance(see para:continue_missed_allowed,default=90)
			if continue_missed_counter>continue_missed_allowed:
				print '\n'+code+' many days tick data unavailable, auto break!!!! (file name will be adjusted)'
				revised_file_name=code+'_Tick_'+each+'-'+end#revise the file name, mainly the period.
				break#quit iteration

		#if df size exceed some amount, shall save it and clear it
		if df.shape[0]>max_buffer:
			if first_save_marker:
				ts_save_data(df,filename=file_name,destination=destination,tools_dir=tools_dir,append=False,dl_registration=True)
				first_save_marker=False#
				df=DataFrame()
			else:
				ts_save_data(df,filename=file_name,destination=destination,tools_dir=tools_dir,append=True,dl_registration=True)
				df=DataFrame()
	#after loop, save df again in case there might be same data left in df			
	if df is not None:
		if df.shape[0]>0:
			sys.stdout.write('\r'+' ['+code+'] tick data [missed] on date:['+each+'][No.'+str(counter)+'/'+str(len(dates))+', '+str(counter-missed_counter)+'got'+'/'+str(missed_counter)+'missed'+']current data size: ['+str(df.shape[0])+'/'+str(size_counter)+'lines]...')
			sys.stdout.flush()
			ts_save_data(df,filename=file_name,revised_name=revised_file_name,destination=destination,tools_dir=tools_dir,append=True,dl_registration=True)
	print code+' tick data download completed!!'

			



def ts_save_data(df,filename,revised_name='',destination='/Users/zhuyu/Documents/stock_data/tushare_data/data/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',append=False,dl_registration=True):
	'''
	description: 
	this function is designed to save data(DataFrame, see para:df) into specified location(see para:destination) and by given name(see para:filename)
	there are to modes of saving. one is create new file(use para:filename) and save the data, another is append data into existing file(para:filename) while 
	para append=Ture. However, in this mode, if file is not found, still it will create a new file and save the data(exactly like mode one). 
	

	This function will access dl_records_*.csv(download registration files) and registrate download records(number of records gotten 
	for one stock and on one date). this shall be controlled by para:dl_registration
    
    para: df(pandas.DataFrame) - data to be saved
          columns(list) - df shall be saved according to the column order given by this para. if no re-order of columns is required, it can be ignored
          destination(str) - location to save data and to get tools
          filename(str) -  filename to be created or append
          append(bool) - append mode on/off
          dl_registration(bool) - access dl_records_*.csv and registrate the downloading records. on/off

	'''
	import pandas as pd
	from pandas import DataFrame
	#check df valid
	if df is None:
		print '\ndf is None, return'
		return
	if type(df)!=pd.DataFrame:
		print '\ndf is not DataFrame type, return'
		return
	if df.shape[0]==0:
		print '\ndf is empty, return'
	import os
	#check file existence,create/append save
	if append==False:#aim to create new file 
		if os.path.exists(destination+filename+'.csv'):#file exists
			print '\nfile: .../'+filename+' already exists, return(if need to recreate the file, please delete file and try again)'
			print 'fail to create and save!'
			return
		else:#file not exists, create and save
			df.to_csv(destination+filename+'.csv',index=True,header=True)#normal save
			print '\nfile: .../'+filename+'.csv'+' created and saved!'
	else:#aim to append into existing file
		if os.path.exists(destination+filename+'.csv'):#file exists
			df.to_csv(destination+filename+'.csv',mode='a',index=True,header=False)
			print '\nfile: .../'+filename+'.csv'+' appended and saved!'
		else:#file not exists, create and save
			print '\nfile: .../'+filename+' dose not exists, cannot append, creating new file and saving...'
			df.to_csv(destination+filename+'.csv',index=True,header=True)#normal save
			print '\nfile: .../'+filename+'.csv'+' created and saved!'


	#registrate download 
	if dl_registration==True:
		pass
	#revise name while revised_name!=''
	if revised_name!='':
		os.rename(destination+filename+'.csv',destination+revised_name+'.csv')
		print '\nfile name['+filename+'.csv] is revised to ['+revised_name+'.csv]'

def ts_auto_rename(filename):
	pass
def ts_get_today_all(destination='/Users/zhuyu/Documents/stock_data/tushare_data/data1/get_today_all/',tools_dir='/Users/zhuyu/Documents/stock_data/tushare_data/tools/',dl_registration=False):
	'''
	description: get today(if not trading day, get previous trading day) all stock data(daily format) and save 
	'''
	import tushare as ts
	from datetime import date

	df=ts.get_today_all()
	df=df.drop('name',axis=1)
	ts_save_data(df,filename='get_today_all_'+date.strftime(date.today(),'%Y-%m-%d'),revised_name='',destination=destination,tools_dir=tools_dir,append=False,dl_registration=dl_registration)

def ts_quotes_listenner(codes=[],save=True,show=False,sleep=3,destination='/Users/zhuyu/Documents/stock_data/tushare_data/data1/real_time_quotes/'):
	'''
	parameters:
	codes(list) - 
	save(bool) -  whether save data
	show(bool) - whether show(print) data on screen
	sleep(int) - how many second interval(request data) 
	'''
	if type(codes)!=list:
		print 'list-type codes is required, return'
		return
	if len(codes)==0:
		print 'no code given, return'
		return
	if save:#need to record, create df and file
		df=DataFrame()

	import time
	#start listenning and recording
	while True:
		df_new=ts.get_realtime_quotes(codes)
		time.sleep(sleep)



