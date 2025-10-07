import pandas as pd
from thefuzz import fuzz

df = pd.read_excel("customer_data_real_addresses.xlsx")
df = df.sort_values(by=["Name"])

def is_duplicate(row1, row2):
  name_simalirity = fuzz.ratio(row1["Name"],row2["Name"])
  dept_similarity = fuzz.ratio(row1["Department"],row2["Department"])

  address_similarity = (
      fuzz.ratio(row1["Address1"], row2["Address1"])+
      fuzz.ratio(row1["Address2"], row2["Address2"])+
      fuzz.ratio(row1["Address3"], row2["Address3"])
  ) / 3

  # floor_similarity = fuzz.ratio(str(row1["Floor Number"]),str(row2["Floor Number"]))

  return name_simalirity > 80 and dept_similarity > 80 and address_similarity > 85 #and floor_similarity > 85

#Indentify the duplicates
filtered_data = []
seen = set()

for i, row in df.iterrows():
    is_dup = False
    for existing in filtered_data:
              if is_duplicate(row, existing):
                            is_dup = True
                                        break
              if not is_dup:
                        filtered_data.append(row)# Convert list back to DataFramedf_fuzzy_unique = pd.DataFrame(filtered_data)


df_fuzzy_unique.to_excel("customer_data_fuzzy_unique.xlsx", index=False)