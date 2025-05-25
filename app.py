import streamlit as st
from utils.price_utils import load_price_data, area_based_price, regression_based_price

# Load data
df = load_price_data("data/base_prices.csv")

# Page config
st.set_page_config(page_title="Artika Price Builder", layout="centered")

st.title("🖼️ Artika Price Builder")

# 👉 Input fields with tooltips
col1, col2 = st.columns(2)
with col1:
    width = st.number_input("Width (cm)", min_value=10, step=1, value=30,
                            help="Enter the width of the artwork in centimeters.")
with col2:
    height = st.number_input("Height (cm)", min_value=10, step=1, value=40,
                             help="Enter the height of the artwork in centimeters.")

# Auto-detect shape
shape = "square" if width == height else "rectangle"

# Optional settings
markup = st.slider("Markup %", 0, 50, 0, help="Add a percentage markup to the final price.")
currency = st.selectbox("Currency", ["USD", "IQD"], index=1, help="Select which currency to view the price in.")

# Exchange rates (example values, replace with real ones)
exchange_rates = {"USD": 1500, "IQD": 1150}
exchange_rate = exchange_rates[currency]

# ℹ️ How it works
with st.expander("ℹ️ How Price is Calculated"):
    st.markdown("""
    This price builder uses two smart pricing methods:

    - 📐 **Area-Based**: Scales the price based on the area (width × height), using the nearest known size as reference.
    - 📊 **Regression-Based**: Uses a predictive trendline from all known sizes and prices to estimate the value.

    The **suggested price** is the average of both, plus any optional markup.
    """)

# Calculate prices
price_area = area_based_price(df, width, height, shape)
price_reg = regression_based_price(df, width, height, shape)
average_price = round((price_area + price_reg) / 2)

# Apply markup and currency conversion
def apply_markup(price):
    return round((price * (1 + markup / 100)) / exchange_rate)

# 💬 Show results
st.subheader(f"🔍 Estimated Price for {width}×{height} cm ({shape})")

st.markdown(f"• 📐 **Area-Based Price** (scaled from nearest known size): `{apply_markup(price_area)} {currency}`")
st.markdown(f"• 📊 **Regression Price** (learned from all known prices): `{apply_markup(price_reg)} {currency}`")
st.success(f"💡 **Suggested Final Price**: `{apply_markup(average_price)} {currency}`")
