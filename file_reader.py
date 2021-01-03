import base64
import io

import pandas as pd

def parse_contents(contents, filename):
    try:
        content_string = contents.split(',')[1]

        decoded = base64.b64decode(content_string)
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        
        if 'done' in df and 'date' in df and 'todo' in df:
            return df
        return
    except:
        print("erro")
        return
