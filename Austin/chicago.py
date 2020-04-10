
#importing dependencies and setting app token
import pandas as pd
import requests
from datetime import date, datetime
from sodapy import Socrata
MyAppToken = 'GuILMuJLLhVOQ8u9cyXPc56p3'

#checking the day of the month and printing the result, this is used to filter the dataframe later
today = date.today()
day = today.strftime("%d")
print("Day =", day)

client = Socrata("data.cityofchicago.org", MyAppToken, None, None )

#getting () results from the soda api
try:
    results = client.get("ijzp-q8t2", limit=20000)
                         
except requests.exceptions.Timeout:
  print("Timeout occurred")

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#dropping columns that have no use
clean_columns_df = results_df.drop(columns=['location','x_coordinate', 'y_coordinate','id','beat','district','ward','community_area','fbi_code','updated_on', 'case_number', 'block', 'iucr', 'location_description', 'arrest', ':@computed_region_awaf_s7ux', ':@computed_region_6mkv_f3dw', ':@computed_region_vrxf_vc4k', ':@computed_region_bdys_3d7i', ':@computed_region_43wa_7qmu' , ':@computed_region_rpca_8um6',':@computed_region_d9mm_jgwp',':@computed_region_d3ds_rm58'])
#adding chicago column for organization while grouping
clean_columns_df['city'] = "Chicago"
#formatting datetime to ease readability
clean_columns_df['month'] = pd.to_datetime(clean_columns_df['date']).dt.strftime('%m')
clean_columns_df['date'] = pd.to_datetime(clean_columns_df['date']).dt.strftime('%d')
clean_columns_df.rename(columns = {'date':'day'}, inplace = True)


#reorganizing columns to read easier left to right
clean_columns_df = clean_columns_df[["city",'primary_type','description','domestic', "day", "month", "year", "latitude", "longitude"]]

domestic_crimes = clean_columns_df['domestic'] == True
non_domestic_crimes = clean_columns_df['domestic'] == False

#storing filtered and sorted by crime variety data sets
domestic_crimes_df = clean_columns_df[domestic_crimes]
non_domestic_crimes_df = clean_columns_df[non_domestic_crimes]

#prints shape of both in terminal to make sure we are cooking with fire
print(f"Non Domestic Shape: {non_domestic_crimes_df.shape} and Domestic Shape: {domestic_crimes_df.shape}")





