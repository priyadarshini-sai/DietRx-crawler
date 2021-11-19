import glob
import os,sys
import pandas as pd   


folder= sys.argv[1]
sv_file = folder+".csv"
df = pd.concat(map(pd.read_csv, glob.glob(os.path.join('',folder+ "/*.csv"))))
print(df.head())

print(df.shape)
df.to_csv(sv_file,index=False)