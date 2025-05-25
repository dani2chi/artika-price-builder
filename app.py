import streamlit as st
import pandas as pd
import io
import os
from utils.price_utils import load_price_data, area_based_price, regression_based_price

# ───────────────────────────────────────────────────────
# SETUP
# ───────────────────────────────────────────────────────
df = load_price_data("data/base_prices.csv")
st.set_page_config(page_title="Artika Price Builder", layout="centered")

# Optional Logo
if os.path.exists("artika_logo.png"):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("artika_logo.png", width=450)



# Language Switch
language = st.selectbox("🌐 Language", ["English", "Arabic"])
is_arabic = language == "Arabic"

# ───────────────────────────────────────────────────────
# UI Inputs
# ───────────────────────────────────────────────────────
st.title("🖼️ Artika Price Builder" if not is_arabic else "🖼️ منشئ أسعار آرتيكا")

col1, col2 = st.columns(2)
with col1:
    width = st.number_input(
        "Width (cm)" if not is_arabic else "العرض (سم)",
        min_value=10,
        step=1,
        value=30,
        help="📏 Enter the width of the artwork (e.g., 60)" if not is_arabic else "📏 أدخل عرض العمل الفني بالسنتيمتر"
    )
with col2:
    height = st.number_input(
        "Height (cm)" if not is_arabic else "الارتفاع (سم)",
        min_value=10,
        step=1,
        value=40,
        help="📐 Enter the height of the artwork (e.g., 90)" if not is_arabic else "📐 أدخل ارتفاع العمل الفني بالسنتيمتر"
    )

shape = "square" if width == height else "rectangle"

markup = st.slider(
    "Markup %" if not is_arabic else "نسبة الربح",
    0, 50, 0,
    help="💰 Add profit margin or fees (e.g., 10 means +10%)" if not is_arabic else "💰 أضف نسبة الربح إلى السعر"
)

currency = st.selectbox(
    "Currency" if not is_arabic else "العملة",
    ["USD", "IQD"],
    index=1,
    help="💱 Choose which currency to display the price in" if not is_arabic else "💱 اختر العملة التي تفضلها"
)

exchange_rates = {"USD": 1500, "IQD": 1150}
exchange_rate = exchange_rates[currency]

# ───────────────────────────────────────────────────────
# Info / Help Section
# ───────────────────────────────────────────────────────
with st.expander("ℹ️ How Price is Calculated" if not is_arabic else "ℹ️ كيف يتم حساب السعر"):
    st.markdown("""
    This builder uses two smart methods to calculate price:
    - 📐 **Area-Based**: Proportional to nearest known size
    - 📊 **Regression-Based**: Uses a predictive formula
    Final price = average of both + markup
    """ if not is_arabic else """
    يستخدم النظام طريقتين لحساب السعر:
    - 📐 حسب المساحة: نسبة إلى أقرب حجم معروف
    - 📊 حسب الاتجاهات: باستخدام معادلة تنبؤية
    السعر النهائي = متوسط الطريقتين + الربح
    """)

# ───────────────────────────────────────────────────────
# Price Calculations
# ───────────────────────────────────────────────────────
price_area = area_based_price(df, width, height, shape)
price_reg = regression_based_price(df, width, height, shape)
average_price = round((price_area + price_reg) / 2)

def apply_markup(price):
    return round((price * (1 + markup / 100)) / exchange_rate)

# ───────────────────────────────────────────────────────
# Output
# ───────────────────────────────────────────────────────
st.subheader(
    f"🔍 Estimated Price for {width}×{height} cm ({shape})"
    if not is_arabic else f"🔍 السعر المقدر لـ {width}×{height} سم ({'مربع' if shape == 'square' else 'مستطيل'})"
)

st.markdown(f"• 📐 **Area-Based Price**: `{apply_markup(price_area)} {currency}`" if not is_arabic
            else f"• 📐 **السعر حسب المساحة**: `{apply_markup(price_area)} {currency}`")

st.markdown(f"• 📊 **Regression Price**: `{apply_markup(price_reg)} {currency}`" if not is_arabic
            else f"• 📊 **السعر حسب الاتجاه**: `{apply_markup(price_reg)} {currency}`")

st.success(f"💡 Suggested Final Price: `{apply_markup(average_price)} {currency}`" if not is_arabic
            else f"💡 السعر النهائي المقترح: `{apply_markup(average_price)} {currency}`")

# ───────────────────────────────────────────────────────
# CSV Download
# ───────────────────────────────────────────────────────
csv_output = io.StringIO()
csv_output.write("Width (cm),Height (cm),Shape,Area-Based,Regression,Suggested,Currency\n")
csv_output.write(f"{width},{height},{shape},{apply_markup(price_area)},{apply_markup(price_reg)},{apply_markup(average_price)},{currency}\n")

st.download_button(
    label="📥 Download Quote as CSV" if not is_arabic else "📥 تحميل التسعيرة",
    data=csv_output.getvalue(),
    file_name=f"artika_quote_{width}x{height}.csv",
    mime="text/csv"
)

# ───────────────────────────────────────────────────────
# WhatsApp Inquiry Button
# ───────────────────────────────────────────────────────
whatsapp_number = "9647707838768"  
whatsapp_link = f"https://wa.me/{whatsapp_number}?text=Hello, I have a pricing inquiry for a {width}x{height} cm artwork from Artika."

st.markdown(f"[📱 Contact Us on WhatsApp]({whatsapp_link})" if not is_arabic
            else f"[📱 تواصل معنا عبر واتساب]({whatsapp_link})")

# ───────────────────────────────────────────────────────
# Footer
# ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("🖌 **Powered by Artika**" if not is_arabic else "🖌 **مشغل بواسطة آرتيكا**")

