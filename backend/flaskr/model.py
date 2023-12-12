# oil
#               value
# Date	
# 2004-01-30	33.16
# 2004-02-02	34.02
# 2004-02-03	34.20
# 2004-02-04	33.06
# 2004-02-05	33.26
# ...	...
# 2023-11-28	76.09
# 2023-11-29	77.56
# 2023-11-30	75.66
# 2023-12-01	73.70
# 2023-12-04	72.73

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_oil_price(oil_price: pd.DataFrame) -> pd.DataFrame:
    oil_price['Date'] = pd.to_datetime(oil_price['period'])
    oil_price = oil_price.set_index('Date')
    oil_price = oil_price[['value']]
    oil_price = oil_price.sort_index(ascending=True)
    # Convert oil.Value to numeric, coercing any errors
    oil_price['value'] = pd.to_numeric(oil_price['value'], errors='coerce')
    print(oil_price.head(10))
    # Drop any NaN values that may have been introduced by coercion
    oil_price.dropna(subset=['value'], inplace=True)

    model = ARIMA(oil_price['value'], order=(2, 2, 10))
    results_ARIMA = model.fit()

    # Forecast the next 7 time steps (One week)
    forecast_steps = 7
    forecast_values = results_ARIMA.forecast(steps=forecast_steps)

    print("Forecasted values for the next {} time steps:".format(forecast_steps))
    print(forecast_values)

    return forecast_values
