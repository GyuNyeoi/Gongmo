import pandas as pd

def read_xlsx_to_dict(xlsx_file, sheet_names):
    data_dict = {}

    for sheet_name in sheet_names:
        df = pd.read_excel(xlsx_file, sheet_name=sheet_name, header=None)
        sheet_dict = {}
        for i, row in df.iterrows():
            sheet_dict[f"{i+1}통"] = row.iloc[0]  # 첫 번째 열의 데이터
        data_dict[sheet_name] = sheet_dict

    return data_dict

sheet_names = ['상망동', '하망동', '영주1동', '영주2동', '휴천1동', '휴천2동', '휴천3동', '가흥1동', '가흥2동']
xlsx_file = '/content/drive/MyDrive/shp2/leetong.xlsx'
data_dict = read_xlsx_to_dict(xlsx_file, sheet_names)

for sheet_name, sheet_dict in data_dict.items():
    print(f"{sheet_name}:")
    for row_index, row_data in sheet_dict.items():
        print(f"  {row_index}: {row_data}")
    print("\n")
