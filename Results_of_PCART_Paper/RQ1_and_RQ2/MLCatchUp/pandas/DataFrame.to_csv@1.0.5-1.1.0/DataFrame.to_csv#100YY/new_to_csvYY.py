import pandas as pd
df = pd.DataFrame({'name': ['Raphael', 'Donatello'], 'mask': ['red', 'purple'], 'weapon': ['sai', 'bo staff']})
df.to_csv(None,  ',',  '',  None,  None, header=True, index=False, index_label=None, mode='w', encoding=None, compression='infer', quoting=None, quotechar='"',line_terminator=None,chunksize=None,date_format=None,doublequote=True,escapechar=None,decimal='.')