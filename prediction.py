import pandas as pd
from statsmodels.tsa.api import ExponentialSmoothing

df = pd.read_excel(r"C:\Users\Mayank Subramanian\Downloads\grocery_dataset_eg.xlsx", index_col='PERIOD')
df.drop(['MONTH'], axis=1, inplace=True)
hw_mul = ExponentialSmoothing(
    df,
    seasonal_periods=4,
    trend="mul",
    seasonal="mul",
    use_boxcox=True,
    initialization_method="estimated",
).fit()
a = hw_mul.forecast(1)
b = a.to_string()
c = b[2:]
d = c.strip()
# print(d)
