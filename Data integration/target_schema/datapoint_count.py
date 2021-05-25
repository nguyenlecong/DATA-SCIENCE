import os
import pandas as pd
path = 'target_schema/data'
source_schemas = os.listdir(os.path.expanduser(path))
sum = 0
for i in range(len(source_schemas)):
    new_path = 'target_schema/data/' + source_schemas[i]
    df = pd.read_csv(new_path)
    print(len(df))
    sum += len(df)
print(sum)