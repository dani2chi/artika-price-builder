import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def load_price_data(csv_path):
    df = pd.read_csv(csv_path)
    df["area"] = df["width"] * df["height"]
    return df

def area_based_price(df, width, height, shape):
    area = width * height
    df_shape = df[df["shape"] == shape].copy()
    closest = df_shape.iloc[(df_shape["area"] - area).abs().argsort()[:1]]
    ref_area = closest["area"].values[0]
    ref_price = closest["price"].values[0]
    return round((area / ref_area) * ref_price)

def regression_based_price(df, width, height, shape):
    df_shape = df[df["shape"] == shape].copy()
    X = df_shape[["width", "height"]]
    y = df_shape["price"]
    model = LinearRegression().fit(X, y)
    input_df = pd.DataFrame([[width, height]], columns=["width", "height"])
    return round(model.predict(input_df)[0])
