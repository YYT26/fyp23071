# -*- coding: utf-8 -*-
import pandas as pd
import os

file = "LIHKG_News_HSBC.xlsx"

if os.path.isfile(file[:-5]+'_result'+'.xlsx'):
    cur_result = pd.read_excel(file[:-5]+'_result'+'.xlsx')
    #print(cur_result["content"].head().values)
    cur_result["content"] = [x.encode().decode('unicode_escape') if isinstance(x, str) else x for x in cur_result["content"].values ]
    cur_result["time"] = [x.encode().decode('unicode_escape') if isinstance(x, str) else x for x in cur_result["time"].values ]
    cur_result["title"] = [x.encode().decode('unicode_escape') if isinstance(x, str) else x for x in cur_result["title"].values ]
    #cur_result.map(lambda x: x.encode().decode('unicode_escape') if isinstance(x, str) else x)
    cur_result.to_excel(file[:-5]+'_result_'+"decoded"+".xlsx",index=False,engine='xlsxwriter')
    cur_result.to_excel(file[:-5]+'_result'+".xlsx",index=False,engine='xlsxwriter')