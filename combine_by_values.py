import glob
import pandas as pd
path = r'C:/file/path' # use your path
all_files = glob.glob(path + "/*.xlsx")

#dataframe array li
li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0)
#     for troubleshooting file errors, can enable below    
#     df['file'] = filename
#     print(filename)
    li.append(df)

#array of all file headers, and filtered arrays    
headers = []
taken_filter = []
open_filter = []

#add to arrays
length = len(li)-1
for i in range(0,length):
    column_names = list(li[i].head(0))
    headers.append(column_names)
    taken_filter.append(li[i][li[i].apply(lambda r: r.str.contains('Taken', case=False).any(), axis=1)])
    open_filter.append(li[i][li[i].apply(lambda r: r.str.contains('Open', case=False).any(), axis=1)])   

#unnamed headers
data = []
length_headers = len(headers)-1
for n in range(0,length_headers):
    if any("Unnamed" in s for s in headers[n]):
        data.append(n)

#finds columns where top phrase is taken or open puts the order in nums, puts the header names in headers
nums = []
headers = []
for i in range (0,length):
    try:
        headers.append(li[i].describe(include="all").transpose().index[li[i].describe(include="all").transpose().top =="Taken"][0])
        nums.append(i)
    except IndexError:
        headers.append(li[i].describe(include="all").transpose().index[li[i].describe(include ="all").transpose().top =="Open"][0])
        nums.append(i)
        
#create dictionary of the taken open column headers/numbers        
dict = {}
for i in range(len(nums)):
    dict[nums[i]] = headers[i]

#use the dictionary to replace those headers mislabeled to one key column called 'status'
length2 = len(open)-1
for i in range (0,length2):
    open[i].columns = open[i].columns.str.replace(dict[i], 'status')

#combine all the files on the new key 'status' column
for i in range(0,length2):
    print(i)
    open[0] = pd.concat([open[0],open[i+1]], sort = False)
    
#may want to remove headers for text output
open[0].to_csv('full_list.csv')
open[0].to_csv('text_list.txt', sep='\t', index=False)
