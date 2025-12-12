import streamlit as st
import requests
import uuid

st.set_page_config(page_title="GeoMarket Advisor", layout="centered")

st.title("GeoMarket Advisor")
st.caption("AI-powered business location analysis")

business_type = st.text_input(
    "Business type",
    placeholder="e.g. Bakery, Coffee shop, Gym"
)

city = st.text_input(
    "City",
    placeholder="e.g. Málaga, Madrid, Barcelona"
)

analyze = st.button("Analyze")

if analyze and business_type and city:
    query = f"{business_type} in {city}"

    payload = {
        "query": query
    }

    resp = requests.post(
        "http://geomarket_advisor_runtime:8000/run",
        json=payload,
        timeout=120
    )

    st.write("STATUS:", resp.status_code)

    if resp.status_code == 200:
        try:
            st.markdown("### Result")
            st.write(resp.json()["response"])
        except Exception:
            st.error("Invalid response from backend")
            st.text(resp.text)
    else:
        st.error("Backend error")
        st.text(resp.text)

elif analyze:
    st.warning("Please fill in both fields.")
