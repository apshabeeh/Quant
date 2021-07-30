import pyodbc,requests
import pandas as pd
import datetime,time
import re,os,shutil,zipfile
from zipfile import ZipFile

start_time = datetime.datetime.now()

pc_username = os.getlogin()
Daily_Data_Path = f'C:/Users/{pc_username}/Desktop/Daily Data/'

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
			'referer':'https://www1.nseindia.com/'}

# PARSING THE DATE DETAILS FOR MAKING DYNAMIC URL'S:
today = datetime.date.today()					### 2021-03-08
month = today.strftime("%m")			### 03
day = today.strftime("%d")				### 08
MON = today.strftime("%b").upper()		### MAR
year = today.year 						### 2021
year_in_2_digit = today.strftime("%y")	### 21

# MAKING DYNAMIC URL'S:
NSE_Deliverables_url = f'https://www1.nseindia.com/archives/equities/mto/MTO_{day}{month}{year}.DAT'
NSE_Bhavcopy_url = f'https://www1.nseindia.com/content/historical/EQUITIES/{year}/{MON}/cm{day}{MON}{year}bhav.csv.zip'
icharts_url = 'https://www.icharts.in/includes/screener/EODScan.php?export=1'
BSE_Deliverables_url = f'https://www.bseindia.com/BSEDATA/gross/{year}/SCBSEALL{day}{month}.zip'
BSE_Bhavcopy_url = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE_{day}{month}{year_in_2_digit}.zip'

def clean_Daily_Data_Folder():
	if not os.path.exists(Daily_Data_Path):
		os.mkdir(Daily_Data_Path)
	for file in os.listdir(Daily_Data_Path):
		os.chdir(Daily_Data_Path)
		try:	
			os.remove(file)
		except:
			shutil.rmtree(Daily_Data_Path+file)
			pass
	print("Starting download...""\n")
	
def NSE_Deliverables():
	r = requests.get(NSE_Deliverables_url,headers=headers)
	if r.status_code == 200:
		with open(Daily_Data_Path + 'NSE_Deliverable_Data.csv','wb') as f:
			f.write(r.content)
			print("NSE Deliverables data download Complete")
	else:
		print(f"NSE Deliverables data download failed (Please change your system date or Check whether the data is available for {day}-{MON}-{year}")

def NSE_Bhavcopy():
	r = requests.get(NSE_Bhavcopy_url,headers=headers)
	if r.status_code == 200:
		with open(Daily_Data_Path + 'NSE_Bhavcopy.zip','wb') as f:
			f.write(r.content)
			print("NSE Bhavcopy download Complete")
	else:
		print(f"NSE Bhavcopy download failed (Please change your system date or Check whether the data is available for {day}-{MON}-{year}")
	
def icharts_data():
	r = requests.get(icharts_url,headers=headers)
	if r.status_code == 200:
		with open(Daily_Data_Path + 'Technical_Data.csv','wb') as f:
			f.write(r.content)
			print("Technical data download Complete")
	else:
		print("Something went wrong")
	
def BSE_Bhavcopy():
	r = requests.get(BSE_Bhavcopy_url,headers=headers)
	if r.status_code == 200:
		with open(Daily_Data_Path + 'BSE_Bhavcopy.zip','wb') as f:
			f.write(r.content)
			print("BSE Bhavcopy download Complete")
	else:
		print(f"BSE Bhavcopy download failed (Please change your system date or Check whether the data is available for {day}-{MON}-{year}")
	
def BSE_Deliverables():
	r = requests.get(BSE_Deliverables_url,headers=headers)
	if r.status_code == 200:
		with open(Daily_Data_Path + 'BSE_Deliverables.zip','wb') as f:
			f.write(r.content)
			print("BSE Deliverables data download Complete")
	else:
		print(f'BSE Deliverables data download failed (Please change your system date or Check whether the data is available for {day}-{MON}-{year}')

# EXTRACTING AND DELETING THE ZIP FILES
def extract_all():
	print("Extracting downloaded files...")
	os.chdir(Daily_Data_Path)

	for file in os.listdir(Daily_Data_Path):
		if file.endswith(".zip"):
			with ZipFile(file, 'r') as zipobj:
				zipobj.extractall()
			os.remove(file)	
	print("Extraction completed successfully.")
	print()			
	
# FUNCTION TO CLEAN ALL THE UNWANTED HEADERS FROM NSE DELIVERABLES DATA AND ADD NECESSARY ONES
def clean_NSE_Deliverables():
		
	if os.path.exists(Daily_Data_Path + 'NSE_Deliverable_Data.csv'):
		print("Cleaning NSE Deliverables Data...")
		rawNSEDeliverablesfile = open(Daily_Data_Path + 'NSE_Deliverable_Data.csv','r')
		lines = rawNSEDeliverablesfile.readlines()
		rawNSEDeliverablesfile.close()
		del lines[:4]
		new_NSE_Deliverables_Data = open(f"C:/Users/{pc_username}/Desktop/Daily Data/NSE_Deliverables1.csv",'w')
		for line in lines:
			new_NSE_Deliverables_Data.write(line)
		new_NSE_Deliverables_Data.close()
		os.remove(Daily_Data_Path + 'NSE_Deliverable_Data.csv')

	if os.path.exists(Daily_Data_Path + 'NSE_Deliverables1.csv'):	
		df = pd.read_csv(Daily_Data_Path + 'NSE_Deliverables1.csv',names=["Record Type","Sr No","Name of Security","Series","Volume","Delivery Volume","Delivery Percentage"])
		df = df.drop(['Record Type','Sr No'],axis = 1)
		df.to_csv(Daily_Data_Path + f'MTO_{day}{month}{year}.csv',index = False)
		os.remove(Daily_Data_Path + 'NSE_Deliverables1.csv')
		print("Cleaning Complete.")
		print()

def clean_BSE_Deliverables():
		if os.path.exists(Daily_Data_Path + f'SCBSEALL{day}{month}.TXT'):
			print("Cleaning BSE Deliverables Data...")
			df = pd.read_csv(Daily_Data_Path + f'SCBSEALL{day}{month}.TXT',delimiter='|')
			df = df.drop(['DATE'],axis = 1)
			df.to_csv(Daily_Data_Path + f'SCBSEALL{day}{month}.csv',index = False)
			os.remove(Daily_Data_Path + f'SCBSEALL{day}{month}.TXT')
			print("Cleaning Complete.")
			print()
			print()

def Zipfiles(path):
	os.chdir(path)
	files = os.listdir(path)
	Zip_file_name =f"{day}{MON}{year_in_2_digit}.zip" 

	if len(files)==0:				
		print("Directory is empty.Nothing to Zip")
	else:
		with zipfile.ZipFile(Zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
			for file in files:
				zf.write(file)
		print("==== Packed and ready for backup ====""\n")		
								
try:
	clean_Daily_Data_Folder()
	NSE_Bhavcopy()
	NSE_Deliverables()
	BSE_Bhavcopy()
	BSE_Deliverables()
except Exception as e:
	print(e)

if len(os.listdir(Daily_Data_Path))==4:
	icharts_data()
	print()
	extract_all()
	clean_NSE_Deliverables()
	clean_BSE_Deliverables()
	Zipfiles(Daily_Data_Path)
else:
	print('\n'f'Data not available to download for {day}-{MON}-{year}')	


Driver = 'Microsoft Access Driver (*.mdb, *.accdb)'
DB_Path = "C:/Users/BASIL P S/Desktop/Test_DB.accdb"

conn = pyodbc.connect(Driver = Driver, DBQ = DB_Path, Autocommit = True)
cursor = conn.cursor()

# Using Regex to find the right files
NSE_Bhav_pattern = re.compile(r'cm(\d{2})(\S{3})(\d{4})bhav\.csv')
NSE_Deli_pattern = re.compile(r'MTO_\d{8}\.csv')
BSE_Bhav_pattern = re.compile(r'EQ_ISINCODE_(\d{6})\.CSV')
BSE_Deli_pattern = re.compile(r'SCBSEALL\d{4}\.csv')

files_list = os.listdir(Daily_Data_Path)

NSE_Bhavcopy_name = list(filter(NSE_Bhav_pattern.match, files_list))[0]   # Regex filter method
NSE_Deliverables_name = list(filter(NSE_Deli_pattern.match, files_list))[0]
BSE_Bhavcopy_name = list(filter(BSE_Bhav_pattern.match, files_list))[0]
BSE_Deliverables_name = list(filter(BSE_Deli_pattern.match, files_list))[0]


NSE_Bhav = pd.read_csv(Daily_Data_Path + NSE_Bhavcopy_name)
NSE_Date = NSE_Bhav['TIMESTAMP'][0]
print(NSE_Date,'\n')
def append_NSE_Bhavcopy():
	for row in NSE_Bhav.itertuples():
		SQL = """INSERT INTO tbl1A_Bhavcopy_NSE (Symbol,Series,Open,High,Low,Close,Last,PrevClose,Volume,Turnover,`Timestamp`,
		TotalTrades,ISIN) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""

		params =row.SYMBOL,row.SERIES,row.OPEN,row.HIGH,row.LOW,row.CLOSE,row.LAST,row.PREVCLOSE,str(row.TOTTRDQTY),str(row.TOTTRDVAL),row.TIMESTAMP,str(row.TOTALTRADES),row.ISIN
		cursor.execute(SQL, params)
		print(row.Index+1,'- NSE Bhavcopy updated ===>',row.SYMBOL)

NSE_Deli = pd.read_csv(Daily_Data_Path + NSE_Deliverables_name)
def append_NSE_Deliverables():
	for row in NSE_Deli.itertuples():
		SQL = "INSERT INTO [tbl1A_Deliverable_NSE] VALUES (?,?,?,?,?,?)"

		params = row[1],row[2],str(row[3]),str(row[4]),row[5],NSE_Date
		cursor.execute(SQL,params)
		print(row.Index+1,'- NSE Deliverables updated ===>',row[1])

BSE_Bhav = pd.read_csv(Daily_Data_Path + BSE_Bhavcopy_name)
BSE_Date = BSE_Bhav['TRADING_DATE'][0]
def append_BSE_Bhavcopy():
	for row in BSE_Bhav.itertuples():
		SQL = "INSERT INTO [tbl1B_Bhavcopy_BSE] VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

		params = row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],str(row[11]),str(row[12]),str(row[13]),None,row[15],row[16]
		cursor.execute(SQL,params)
		print(row.Index+1,'- BSE Bhavcopy updated ===>',row[2])

BSE_Deli = pd.read_csv(Daily_Data_Path + BSE_Deliverables_name)
def append_BSE_Deliverables():
	for row in BSE_Deli.itertuples():
		SQL = "INSERT INTO [tbl1B_Deliverable_BSE] VALUES (?,?,?,?,?,?,?)"
		params = row[1],str(row[2]),str(row[3]),str(row[4]),str(row[5]),row[6],BSE_Date
		cursor.execute(SQL,params)
		print(row.Index+1,'- BSE Deliverables updated ===>',row[1])

Technical_Data = pd.read_csv(Daily_Data_Path + 'Technical_Data.csv')
Technical_Data['trix'].fillna(0,inplace = True)
Technical_Data['candle'].fillna('',inplace = True)
def append_Technical_Data():
	for row in Technical_Data.itertuples():				
		SQL = """INSERT INTO [tbl3A_TechnicalData] VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
		?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

		params = row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44],row[45],row[46]
		cursor.execute(SQL,params)
		print(row.Index+1,'- Technical Data updated ===>',row[1])
	print()	

def append_NSE_Data():
	SQL = """INSERT INTO tbl2A_NSEData ( [Timestamp], Symbol, Series, [Open], High, Low, [Close], [Last], PrevClose, Volume,
	 Turnover, TurnoverRsCr, TotalTrades, ISIN, DeliVolume, [Deli%], AvgOrderWorthRs, AvgQtyPerOrder, AvgPrice, DeliTurnover,
	  DeliTurnoverRsCr ) SELECT tbl1A_Bhavcopy_NSE.Timestamp, tbl1A_Bhavcopy_NSE.Symbol, tbl1A_Bhavcopy_NSE.Series, 
	  tbl1A_Bhavcopy_NSE.Open, tbl1A_Bhavcopy_NSE.High, tbl1A_Bhavcopy_NSE.Low, tbl1A_Bhavcopy_NSE.Close, tbl1A_Bhavcopy_NSE.Last, 
	  tbl1A_Bhavcopy_NSE.PrevClose, tbl1A_Bhavcopy_NSE.Volume, tbl1A_Bhavcopy_NSE.Turnover, ([tbl1A_Bhavcopy_NSE].[turnover])/10000000 
	  AS TurnoverRsCr, tbl1A_Bhavcopy_NSE.TotalTrades, tbl1A_Bhavcopy_NSE.ISIN, tbl1A_Deliverable_NSE.DeliVolume, 
	  tbl1A_Deliverable_NSE.[Deli%], (tbl1A_Bhavcopy_NSE.Turnover)/[TotalTrades] AS AvgOrderWorthRs, (tbl1A_Bhavcopy_NSE.Volume)/[TotalTrades] 
	  AS AvgQtyPerOrder, ([tbl1A_Bhavcopy_NSE].[Turnover])/([tbl1A_Bhavcopy_NSE].[Volume]) AS AvgPrice, 
	  ([DeliVolume]*([tbl1A_Bhavcopy_NSE].[Turnover])/([tbl1A_Bhavcopy_NSE].[Volume])) AS DeliTurnover, ([Turnover]/([tbl1A_Bhavcopy_NSE]![Volume]))*[DeliVolume]/10000000 
	  AS DeliTurnoverRsCr FROM tbl1A_Bhavcopy_NSE INNER JOIN tbl1A_Deliverable_NSE ON (tbl1A_Bhavcopy_NSE.Timestamp = tbl1A_Deliverable_NSE.Timestamp) 
	  AND (tbl1A_Bhavcopy_NSE.Symbol = tbl1A_Deliverable_NSE.Symbol) AND (tbl1A_Bhavcopy_NSE.Series = tbl1A_Deliverable_NSE.Series) WHERE (((tbl1A_Bhavcopy_NSE.Timestamp)=Date()));"""
	cursor.execute(SQL)
	print('===> NSE_Data appended')

def append_BSE_Data():
	SQL = """INSERT INTO tbl2B_BSEData ( [TIMESTAMP], ScCode, ScName, [GROUP], TYPE, [OPEN], HIGH, LOW, [CLOSE], [Last], PREVCLOSE, 
	Volume, Turnover, TurnoverRsCr, TOTALTRADES, DeliVolume, [Deli%], AvgOrderWorthRs, AvgQtyPerOrder, AvgPrice, DeliTurnover, 
	DeliTurnoverRsCr, ISIN ) SELECT tbl1B_Bhavcopy_BSE.TIMESTAMP, tbl1B_Bhavcopy_BSE.ScCode, tbl1B_Bhavcopy_BSE.ScName, 
	tbl1B_Bhavcopy_BSE.GROUP, tbl1B_Bhavcopy_BSE.TYPE, tbl1B_Bhavcopy_BSE.OPEN, tbl1B_Bhavcopy_BSE.HIGH, tbl1B_Bhavcopy_BSE.LOW, 
	tbl1B_Bhavcopy_BSE.CLOSE, tbl1B_Bhavcopy_BSE.Last, tbl1B_Bhavcopy_BSE.PREVCLOSE, tbl1B_Deliverable_BSE.Volume, tbl1B_Deliverable_BSE.Turnover, 
	([tbl1B_Bhavcopy_BSE].[turnover])/10000000 AS TurnoverRsCr, tbl1B_Bhavcopy_BSE.TOTALTRADES, tbl1B_Deliverable_BSE.DeliVolume, 
	tbl1B_Deliverable_BSE.[Deli%], ([tbl1B_Bhavcopy_BSE].[Turnover])/[TOTALTRADES] AS AvgOrderWorthRs, ([tbl1B_Bhavcopy_BSE].[Volume])/[TOTALTRADES] 
	AS AvgQtyPerOrder, ([tbl1B_Bhavcopy_BSE].[Turnover])/([tbl1B_Bhavcopy_BSE].[Volume]) AS AvgPrice, ([delivolume]*[Avgprice]) 
	AS DeliTurnover, [DeliTurnover]/10000000 AS DeliTurnoverRsCr, tbl1B_Bhavcopy_BSE.ISIN FROM tbl1B_Bhavcopy_BSE INNER JOIN tbl1B_Deliverable_BSE 
	ON (tbl1B_Bhavcopy_BSE.ScCode = tbl1B_Deliverable_BSE.ScCode) AND (tbl1B_Bhavcopy_BSE.TIMESTAMP = tbl1B_Deliverable_BSE.Timestamp) 
	WHERE (((tbl1B_Bhavcopy_BSE.TIMESTAMP)=Date()));"""
	cursor.execute(SQL)
	print('===> BSE_Data appended')

def append_NSE_Plus_BSE_Data():
	SQL = """INSERT INTO [tbl5A_Combined_NSE+BSE_Data] ( [Timestamp], ScCode, ScName, Symbol, Series, [Open], High, Low, [Close], 
	[Last], PrevClose, ISIN, [BSE+NSE_Volume], [BSE+NSE_Turnover], [BSE+NSE_TurnoverRsCr], [BSE+NSE_TotalTrades], [BSE+NSE_DeliVolume], 
	AvgOrderWorthRs, AvgQtyPerOrder, AvgPrice, DeliTurnover, DeliTurnoverRsCr, [BSE+NSE_Deli%] ) SELECT qry1A_Combined_NSE.Timestamp, 
	qry1B_Combined_BSE.ScCode, qry1B_Combined_BSE.ScName, qry1A_Combined_NSE.Symbol, qry1A_Combined_NSE.Series, qry1A_Combined_NSE.Open, 
	qry1A_Combined_NSE.High, qry1A_Combined_NSE.Low, qry1A_Combined_NSE.Close, qry1A_Combined_NSE.Last, qry1A_Combined_NSE.PrevClose, 
	qry1A_Combined_NSE.ISIN, [qry1A_Combined_NSE]![Volume]+[qry1B_Combined_BSE]![Volume] AS [BSE+NSE_Volume], [qry1A_Combined_NSE]![Turnover]+[qry1B_Combined_BSE]![Turnover] 
	AS [BSE+NSE_Turnover], [qry1A_Combined_NSE]![TurnoverRsCr]+[qry1B_Combined_BSE]![TurnoverRsCr] AS [BSE+NSE_TurnoverRsCr], 
	[qry1A_Combined_NSE]![TotalTrades]+[qry1B_Combined_BSE]![TotalTrades] AS [BSE+NSE_TotalTrades], [qry1A_Combined_NSE]![DeliVolume]+[qry1B_Combined_BSE]![DeliVolume] 
	AS [BSE+NSE_DeliVolume], ([qry1A_Combined_NSE]![Turnover]+[qry1B_Combined_BSE]![Turnover])/([qry1A_Combined_NSE]![TotalTrades]+[qry1B_Combined_BSE]![TotalTrades]) 
	AS AvgOrderWorthRs, ([qry1A_Combined_NSE]![Volume]+[qry1B_Combined_BSE]![Volume])/([qry1A_Combined_NSE]![TotalTrades]+[qry1B_Combined_BSE]![TotalTrades]) AS AvgQtyPerOrder, 
	([qry1A_Combined_NSE].[Turnover]+[qry1B_Combined_BSE].[Turnover])/([qry1A_Combined_NSE]![Volume]+[qry1B_Combined_BSE]![Volume]) 
	AS AvgPrice, [AvgPrice]*[BSE+NSE_DeliVolume] AS DeliTurnover, [DeliTurnover]/10000000 AS DeliTurnoverRsCr, ([BSE+NSE_DeliVolume]/[BSE+NSE_Volume])*100 AS [BSE+NSE_Deli%] 
	FROM qry1A_Combined_NSE INNER JOIN qry1B_Combined_BSE ON (qry1A_Combined_NSE.ISIN = qry1B_Combined_BSE.ISIN) AND (qry1A_Combined_NSE.Timestamp = qry1B_Combined_BSE.TIMESTAMP);"""
	cursor.execute(SQL)
	print('===> NSE+BSE_Data appended')

def append_MultiTimeFrame_Analysis_Data():
	print(f'===> Appending Multi Timeframe Data\n\nThis may take a while, So please wait....')

	SQL = """INSERT INTO tbl7A_FormData ( [Timestamp], Symbol, ScCode, Series, [GROUP], TYPE, [Open], High, Low, [Close], [Last], 
	PrevClose, DeliVolume, Volume, TotalTrades, DeliTurnoverRsCr, TurnoverRsCr, AvgOrderWorthRs, [Deli%], AvgQtyperTrade, AvgDeliPrice, 
	ISIN, 1WeekHigh, 1WeekLow, 1WeekAvgOfAvgDeliPrice, 1WeekAvgOfDeliVolume, 1WeekAvgOfVolume, 1WeekAvgOfTotalTrades, 1WeekAvgOfDeliTurnoverRsCr, 
	1WeekAvgOfTurnoverRsCr, 1WeekAvgOfAvgOrderWorthRs, [1WeekAvgOfDeli%], 1WeekAvgOfAvgQtyPerTrade, 1MonthHigh, 1MonthLow, 1MonthAvgOfAvgDeliPrice, 
	1MonthAvgOfDeliVolume, 1MonthAvgOfVolume, 1MonthAvgOfTotalTrades, 1MonthAvgOfDeliTurnoverRsCr, 1MonthAvgOfTurnoverRsCr, 1MonthAvgOfAvgOrderWorthRs, 
	[1MonthAvgOfDeli%], 1MonthAvgOfAvgQtyPerTrade, 3MonthsHigh, 3MonthsLow, 3MonthAvgOfAvgDeliPrice, 3MonthAvgOfDeliVolume, 3MonthAvgOfVolume, 
	3MonthAvgOfTotalTrades, 3MonthAvgOfDeliturnoverRsCr, 3MonthAvgOfTurnoverRsCr, 3MonthAvgOfAvgOrderWorthRs, [3MonthAvgOfDeli%], 3MonthAvgOfAvgQtyPerTrade, 
	1YearHigh, 1YearLow, 1YearAvgOfAvgDeliPrice, 1YearAvgOfDeliVolume, 1YearAvgOfVolume, 1YearAvgOfTotalTrades, 1YearAvgOfDeliTurnoverRsCr, 1YearAvgOfTurnoverRsCr,
	1YearAvgOfAvgOrderWorthRs, [1YearAvgOfDeli%], 1YearAvgOfAvgQtyPerTrade ) SELECT qry1A_Combined_NSE.Timestamp, qry1A_Combined_NSE.Symbol, 
	qry1B_Combined_BSE.ScCode, qry1A_Combined_NSE.Series, qry1B_Combined_BSE.GROUP, qry1B_Combined_BSE.TYPE, qry1A_Combined_NSE.Open, qry1A_Combined_NSE.High,
	qry1A_Combined_NSE.Low, qry1A_Combined_NSE.Close, qry1A_Combined_NSE.Last, qry1A_Combined_NSE.PrevClose, [qry1A_Combined_NSE].[delivolume]+[qry1B_Combined_BSE].[delivolume] 
	AS DeliVolume, [qry1A_Combined_NSE].[volume]+[qry1B_Combined_BSE].[volume] AS Volume, [qry1A_Combined_NSE].[Totaltrades]+[qry1B_Combined_BSE].[totaltrades] 
	AS TotalTrades, [qry1A_Combined_NSE].[DeliTurnoverRsCr]+[qry1B_Combined_BSE].[DeliTurnoverRsCr] AS DeliTurnoverRsCr, [qry1A_Combined_NSE].[TurnoverRsCr]+[qry1B_Combined_BSE].[TurnoverRsCr] 
	AS TurnoverRsCr, ([qry1A_Combined_NSE].[turnover]+[qry1B_Combined_BSE].[turnover])/([qry1A_Combined_NSE].[TotalTrades]+[qry1B_Combined_BSE].[totaltrades]) 
	AS AvgOrderWorthRs, ([qry1A_Combined_NSE].[delivolume]+[qry1B_Combined_BSE].[delivolume])/([qry1A_Combined_NSE].[volume]+[qry1B_Combined_BSE].[volume])*100 
	AS [Deli%], ([qry1A_Combined_NSE].[volume]+[qry1B_Combined_BSE].[volume])/([qry1A_Combined_NSE].[totaltrades]+[qry1B_Combined_BSE].[totaltrades]) 
	AS AvgQtyperTrade, ([qry1A_Combined_NSE].[DeliTurnover]+[qry1B_Combined_BSE].[DeliTurnover])/([qry1A_Combined_NSE].[Delivolume]+[qry1B_Combined_BSE].[Delivolume]) 
	AS AvgDeliPrice, qry1A_Combined_NSE.ISIN, qry6C_1Week_Data.MaxOfHIGH AS 1WeekHigh, qry6C_1Week_Data.MinOfLOW AS 1WeekLow, qry6C_1Week_Data.[Total Of AvgDeliPrice] 
	AS 1WeekAvgOfAvgDeliPrice, qry6C_1Week_Data.[total of delivolume] AS 1WeekAvgOfDeliVolume, qry6C_1Week_Data.[total of volume] AS 1WeekAvgOfVolume, qry6C_1Week_Data.[total of totaltrades] 
	AS 1WeekAvgOfTotalTrades, qry6C_1Week_Data.[total of Deliturnoverrscr] AS 1WeekAvgOfDeliTurnoverRsCr, qry6C_1Week_Data.[total of TurnoverrsCr] 
	AS 1WeekAvgOfTurnoverRsCr, qry6C_1Week_Data.[total of avgorderworthrs] AS 1WeekAvgOfAvgOrderWorthRs, qry6C_1Week_Data.[Total Of Deli%] 
	AS [1WeekAvgOfDeli%], qry6C_1Week_Data.[Total Of AvgQtyPerTrade] AS 1WeekAvgOfAvgQtyPerTrade, qry6D_1Month_Data_Crosstab.MaxOfHIGH 
	AS 1MonthHigh, qry6D_1Month_Data_Crosstab.MinOfLOW AS 1MonthLow, qry6D_1Month_Data_Crosstab.[Total Of AvgDeliPrice] 
	AS 1MonthAvgOfAvgDeliPrice, qry6D_1Month_Data_Crosstab.[Total Of DeliVolume] AS 1MonthAvgOfDeliVolume, qry6D_1Month_Data_Crosstab.[Total Of Volume] 
	AS 1MonthAvgOfVolume, qry6D_1Month_Data_Crosstab.[Total Of TotalTrades] AS 1MonthAvgOfTotalTrades, qry6D_1Month_Data_Crosstab.[Total of DeliTurnoverRsCr] 
	AS 1MonthAvgOfDeliTurnoverRsCr, qry6D_1Month_Data_Crosstab.[Total Of TurnoverRsCr] AS 1MonthAvgOfTurnoverRsCr, qry6D_1Month_Data_Crosstab.[Total Of AvgOrderWorthRs] 
	AS 1MonthAvgOfAvgOrderWorthRs, qry6D_1Month_Data_Crosstab.[Total Of Deli%] AS [1MonthAvgOfDeli%], qry6D_1Month_Data_Crosstab.[Total Of AvgQtyPerTrade] 
	AS 1MonthAvgOfAvgQtyPerTrade, qry6E_3Months_Data_Crosstab.MaxOfHIGH AS 3MonthsHigh, qry6E_3Months_Data_Crosstab.MinOfLOW AS 3MonthsLow, qry6E_3Months_Data_Crosstab.[Total Of AvgDeliPrice] 
	AS 3MonthAvgOfAvgDeliPrice, qry6E_3Months_Data_Crosstab.[Total Of DeliVolume] AS 3MonthAvgOfDeliVolume, qry6E_3Months_Data_Crosstab.[Total Of Volume] 
	AS 3MonthAvgOfVolume, qry6E_3Months_Data_Crosstab.[Total Of TotalTrades] AS 3MonthAvgOfTotalTrades, qry6E_3Months_Data_Crosstab.[Total of DeliTurnoverRsCr] 
	AS 3MonthAvgOfDeliturnoverRsCr, qry6E_3Months_Data_Crosstab.[Total Of TurnoverRsCr] AS 3MonthAvgOfTurnoverRsCr, qry6E_3Months_Data_Crosstab.[Total Of AvgOrderWorthRs] 
	AS 3MonthAvgOfAvgOrderWorthRs, qry6E_3Months_Data_Crosstab.[Total Of Deli%] AS [3MonthAvgOfDeli%], qry6E_3Months_Data_Crosstab.[Total Of AvgQtyPerTrade] 
	AS 3MonthAvgOfAvgQtyPerTrade, qry6F_1Year_Data_Crosstab.MaxOfHIGH AS 1YearHigh, qry6F_1Year_Data_Crosstab.MinOfLOW AS 1YearLow, qry6F_1Year_Data_Crosstab.[Total Of AvgDeliPrice] 
	AS 1YearAvgOfAvgDeliPrice, qry6F_1Year_Data_Crosstab.[Total Of DeliVolume] AS 1YearAvgOfDeliVolume, qry6F_1Year_Data_Crosstab.[Total Of Volume] 
	AS 1YearAvgOfVolume, qry6F_1Year_Data_Crosstab.[Total Of TotalTrades] AS 1YearAvgOfTotalTrades, qry6F_1Year_Data_Crosstab.[Total of DeliTurnoverRsCr] 
	AS 1YearAvgOfDeliTurnoverRsCr, qry6F_1Year_Data_Crosstab.[Total Of TurnoverRsCr] AS 1YearAvgOfTurnoverRsCr, qry6F_1Year_Data_Crosstab.[Total Of AvgOrderWorthRs] 
	AS 1YearAvgOfAvgOrderWorthRs, qry6F_1Year_Data_Crosstab.[Total Of Deli%] AS [1YearAvgOfDeli%], qry6F_1Year_Data_Crosstab.[Total Of AvgQtyPerTrade] 
	AS 1YearAvgOfAvgQtyPerTrade FROM ((((((qry1A_Combined_NSE INNER JOIN qry1B_Combined_BSE ON (qry1A_Combined_NSE.ISIN = qry1B_Combined_BSE.ISIN) 
	AND (qry1A_Combined_NSE.Timestamp = qry1B_Combined_BSE.TIMESTAMP)) INNER JOIN tbl3A_TechnicalData ON (qry1A_Combined_NSE.Timestamp = tbl3A_TechnicalData.TIMESTAMP) 
	AND (qry1A_Combined_NSE.Symbol = tbl3A_TechnicalData.SYMBOLEOD)) INNER JOIN tbl4A_Fundamentals ON qry1A_Combined_NSE.ISIN = tbl4A_Fundamentals.ISIN) 
	INNER JOIN qry6C_1Week_Data_Crosstab AS qry6C_1Week_Data ON qry1A_Combined_NSE.Symbol = qry6C_1Week_Data.SYMBOL) INNER JOIN qry6D_1Month_Data_Crosstab 
	ON qry1A_Combined_NSE.Symbol = qry6D_1Month_Data_Crosstab.SYMBOL) INNER JOIN qry6E_3Months_Data_Crosstab ON qry1A_Combined_NSE.Symbol = qry6E_3Months_Data_Crosstab.SYMBOL) 
	INNER JOIN qry6F_1Year_Data_Crosstab ON qry1A_Combined_NSE.Symbol = qry6F_1Year_Data_Crosstab.SYMBOL;"""
	cursor.execute(SQL)
	print('===> Multi Timeframe data appended''\n')

if len(files_list)==6:
	append_NSE_Bhavcopy()
	append_NSE_Deliverables()
	append_BSE_Bhavcopy()
	append_BSE_Deliverables()
	append_Technical_Data()
else:
	print("Files not found in Daily Data Folder")	

today = datetime.date.today()
today = today.strftime('%d-%b-%Y').upper()			#dd-MMM-yyyy
BSE_Date = datetime.datetime.strptime(BSE_Date,'%d-%b-%y')
BSE_Date = BSE_Date.strftime('%d-%b-%Y').upper()

if BSE_Date == today and NSE_Date == today:
	append_NSE_Data()
	append_BSE_Data()
	append_NSE_Plus_BSE_Data()
	append_MultiTimeFrame_Analysis_Data()
else:
	print(f'Cant execute queries if NSE or BSE date is not equal to Todays date ({today})\n')

cursor.close()

end_time = datetime.datetime.now()

print(f'Finished in {end_time-start_time}')

input()