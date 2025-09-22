import pandas as pd

def save_to_excel(data, filename):
    import openpyxl  
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Veriler Excel'e kaydedildi: {filename}")