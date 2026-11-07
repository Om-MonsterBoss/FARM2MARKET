
import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Krishi Market",
    page_icon="🌾",
    layout="wide",
)

st.title("🌾 Smart Krishi Market")
st.subheader("Maharashtra Live Mandi Prices")

API_URL = "https://mandi-api.onrender.com/v1/prices"

crop = st.selectbox(
    "Select crop",
    ["Onion", "Tomato", "Soybean"],
)

if st.button("Fetch Mandi Prices", type="primary"):
    try:
        with st.spinner("Fetching mandi prices..."):
            response = requests.get(
                API_URL,
                params={
                    "state": "Maharashtra",
                    "commodity": crop,
                },
                headers={"Accept": "application/json"},
                timeout=45,
            )

            st.write("HTTP status:", response.status_code)
            response.raise_for_status()
            result = response.json()

        records = result.get("data", [])

        if records:
            df = pd.DataFrame(records)

            st.success(f"Received {len(df)} price records!")

            preferred = [
                "state", "district", "market", "commodity",
                "variety", "arrival_date", "min_price",
                "max_price", "modal_price",
            ]
            columns = [c for c in preferred if c in df.columns]

            if columns:
                df = df[columns]

            st.dataframe(df, use_container_width=True)

            if "modal_price" in df.columns:
                prices = pd.to_numeric(
                    df["modal_price"], errors="coerce"
                ).dropna()

                if not prices.empty:
                    st.metric(
                        "Average modal price",
                        f"₹{prices.mean():,.0f} per quintal",
                    )

            st.caption(
                "Source: community Mandi Price API, "
                "which reports data sourced from data.gov.in. "
                "Check arrival dates; data may not be from today."
            )
        else:
            st.warning("No matching records were returned.")
            st.json(result)

    except requests.exceptions.RequestException as error:
        st.error("The API request failed.")
        st.code(str(error))

    except ValueError:
        st.error("The API response was not valid JSON.")

