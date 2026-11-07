
import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Farm2Market - Smart Mandi Price Dashboard
st.set_page_config(
    page_title="Farm2Market | Smart Agriculture",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "https://mandi-api.onrender.com/v1/prices"
STATE = "Maharashtra"
CROPS = ["Onion", "Tomato", "Soybean"]

FIELD_IMAGE = "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1000&q=80"
VEGETABLE_IMAGE = "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=900&q=80"
FARMER_IMAGE = "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1000&q=80"

# Modern Farm2Market design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f5f7f2;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1440px;
}

[data-testid="stSidebar"] {
    background: #103a28;
}

[data-testid="stSidebar"] * {
    color: #f7fbf5 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #173b2a !important;
}

.hero {
    padding: 2.5rem;
    border-radius: 24px;
    color: white;
    min-height: 330px;
    background:
        linear-gradient(
            90deg,
            rgba(7,37,23,.93),
            rgba(7,37,23,.68),
            rgba(7,37,23,.12)
        ),
        url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1800&q=85")
        center/cover;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 14px 40px rgba(19,54,33,.12);
}

.eyebrow {
    background: rgba(183,232,86,.18);
    border: 1px solid rgba(205,244,137,.5);
    color: #d8f7a0;
    padding: 7px 13px;
    border-radius: 99px;
    font-size: .82rem;
    width: fit-content;
    margin-bottom: 14px;
}

.hero h1 {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4rem);
    line-height: 1.05;
    margin: 0 0 14px 0;
    font-weight: 800;
}

.hero p {
    color: #edf5e8;
    max-width: 620px;
    font-size: 1.05rem;
}

.section-title {
    font-family: 'Manrope', sans-serif;
    color: #153c2b;
    font-weight: 800;
    font-size: 1.6rem;
    margin: 1.2rem 0 .2rem 0;
}

.section-sub {
    color: #64736a;
    margin-bottom: 1rem;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e4eadf;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(20,55,34,.04);
}

div[data-testid="stMetricLabel"] {
    color: #66756b;
}

div[data-testid="stMetricValue"] {
    color: #173e2b;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
}

.stButton > button {
    border-radius: 12px;
    border: 0;
    background: #b7e85a;
    color: #153820;
    font-weight: 700;
    padding: .65rem 1rem;
}

.stButton > button:hover {
    background: #a4d94b;
    color: #102e1e;
    border: 0;
}

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

.info-card {
    background: white;
    border: 1px solid #e5eadf;
    border-radius: 18px;
    padding: 20px;
    min-height: 145px;
}

.info-card h3 {
    color: #153c2b;
    margin: .6rem 0;
    font-size: 1.1rem;
}

.info-card p {
    color: #64736a;
    font-size: .92rem;
}

.pill {
    display: inline-block;
    background: #edf7df;
    color: #2c5a2d;
    border-radius: 50px;
    padding: 5px 10px;
    font-size: .78rem;
    font-weight: 700;
}

.footer {
    margin-top: 2rem;
    padding: 1.4rem;
    background: #103a28;
    color: #dce9dc;
    border-radius: 16px;
    font-size: .9rem;
}
</style>
""", unsafe_allow_html=True)

# Hero banner
st.markdown("""
<div class="hero">
    <div class="eyebrow">🌱 FARMER-FIRST • MARKET SMART</div>
    <h1>Farm2Market</h1>
    <p>
        Know your mandi prices. Compare markets.
        Make more confident selling decisions —
        all in one simple dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

# Sample prices used only if live API data is unavailable
SAMPLE_DATA = pd.DataFrame([
    {"Crop": "Onion", "Market": "Vashi APMC",
     "Price (₹/quintal)": 1800, "Data source": "Sample data"},
    {"Crop": "Onion", "Market": "Market B",
     "Price (₹/quintal)": 1650, "Data source": "Sample data"},
    {"Crop": "Onion", "Market": "Market C",
     "Price (₹/quintal)": 1920, "Data source": "Sample data"},
    {"Crop": "Tomato", "Market": "Vashi APMC",
     "Price (₹/quintal)": 2200, "Data source": "Sample data"},
    {"Crop": "Tomato", "Market": "Market B",
     "Price (₹/quintal)": 2050, "Data source": "Sample data"},
    {"Crop": "Tomato", "Market": "Market C",
     "Price (₹/quintal)": 2350, "Data source": "Sample data"},
    {"Crop": "Soybean", "Market": "Vashi APMC",
     "Price (₹/quintal)": 4600, "Data source": "Sample data"},
    {"Crop": "Soybean", "Market": "Market B",
     "Price (₹/quintal)": 4450, "Data source": "Sample data"},
    {"Crop": "Soybean", "Market": "Market C",
     "Price (₹/quintal)": 4725, "Data source": "Sample data"},
])


def first_value(record, candidates, default=None):
    lowered = {
        str(k).strip().lower(): v
        for k, v in record.items()
    }

    for candidate in candidates:
        value = lowered.get(candidate.lower())

        if value is not None and str(value).strip() not in (
            "", "None", "nan"
        ):
            return value

    return default


def extract_records(payload):
    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    for key in ("data", "records", "results", "items"):
        value = payload.get(key)

        if isinstance(value, list):
            return value

        if isinstance(value, dict):
            for nested_key in (
                "data", "records", "results", "items"
            ):
                nested = value.get(nested_key)

                if isinstance(nested, list):
                    return nested

    return []


def normalize_records(records, selected_crop):
    normalized = []

    for record in records:
        if not isinstance(record, dict):
            continue

        commodity = first_value(
            record,
            ["commodity", "crop", "commodity_name", "product"],
            selected_crop,
        )

        market = first_value(
            record,
            ["market", "market_name", "mandi", "apmc", "marketname"],
            "Market not specified",
        )

        district = first_value(
            record,
            ["district", "district_name", "districtname"],
            "",
        )

        state = first_value(
            record, ["state", "state_name"], STATE
        )

        arrival_date = first_value(
            record,
            ["arrival_date", "date", "price_date",
             "reported_date", "updated_at"],
            "Not provided",
        )

        variety = first_value(
            record, ["variety", "grade"], ""
        )

        modal = first_value(
            record,
            ["modal_price", "modalprice", "modal",
             "price", "modal_price_rs"],
        )

        minimum = first_value(
            record,
            ["min_price", "minprice", "minimum_price", "min"],
        )

        maximum = first_value(
            record,
            ["max_price", "maxprice", "maximum_price", "max"],
        )

        def as_number(value):
            if value is None:
                return np.nan

            try:
                return float(
                    str(value).replace(",", "")
                    .replace("₹", "").strip()
                )
            except (ValueError, TypeError):
                return np.nan

        modal = as_number(modal)
        minimum = as_number(minimum)
        maximum = as_number(maximum)

        if pd.isna(modal):
            continue

        crop_text = str(commodity).strip()

        if crop_text.lower() in ("soyabean", "soybean"):
            crop_text = "Soybean"
        elif crop_text:
            crop_text = crop_text.title()

        normalized.append({
            "Crop": crop_text or selected_crop,
            "Market": str(market),
            "District": str(district),
            "State": str(state),
            "Arrival date": str(arrival_date),
            "Variety": str(variety),
            "Min price (₹/quintal)": minimum,
            "Max price (₹/quintal)": maximum,
            "Price (₹/quintal)": modal,
            "Data source": "Third-party API",
        })

    return normalized


@st.cache_data(ttl=300, show_spinner=False)
def fetch_crop_prices(crop):
    crop_names = (
        ["Soybean", "Soyabean"]
        if crop == "Soybean" else [crop]
    )

    errors = []

    for crop_name in crop_names:
        try:
            response = requests.get(
                API_URL,
                params={
                    "state": STATE,
                    "commodity": crop_name,
                },
                headers={"Accept": "application/json"},
                timeout=(10, 30),
            )

            response.raise_for_status()
            payload = response.json()

            rows = normalize_records(
                extract_records(payload), crop
            )

            if rows:
                return rows, None

            errors.append(
                f"{crop_name}: no usable price records were found."
            )

        except requests.exceptions.Timeout:
            errors.append(f"{crop_name}: request timed out.")

        except requests.exceptions.RequestException as exc:
            errors.append(f"{crop_name}: {exc}")

        except ValueError:
            errors.append(
                f"{crop_name}: response was not valid JSON."
            )

    return [], " ".join(errors)


# Sidebar
st.sidebar.markdown("## 🌱 Farm2Market")
st.sidebar.caption("Your crop. Your market. Your choice.")
st.sidebar.divider()

st.sidebar.markdown("### Dashboard settings")

selected_crop = st.sidebar.selectbox(
    "Choose a crop",
    CROPS,
)

show_all_crops = st.sidebar.checkbox(
    "Load prices for all crops",
    value=True,
)

if st.sidebar.button(
    "↻ Refresh live prices",
    use_container_width=True,
):
    st.cache_data.clear()

st.sidebar.divider()
st.sidebar.markdown("### Why Farm2Market?")
st.sidebar.write("📍 Compare mandi prices")
st.sidebar.write("📈 Explore price trends")
st.sidebar.write("🔔 Check your target price")


# Feature cards
st.markdown(
    '<div class="section-title">A smarter way to sell</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">Simple tools designed to help '
    'farmers make informed market decisions.</div>',
    unsafe_allow_html=True,
)

feature_cols = st.columns(3)

feature_data = [
    (
        "📊", "Compare markets",
        "See listed prices side by side before deciding where to sell."
    ),
    (
        "🌿", "Farmer-first design",
        "A clean dashboard with easy-to-read crop information."
    ),
    (
        "🔔", "Price target alerts",
        "Check whether listed prices meet your target price."
    ),
]

for col, (emoji, title, description) in zip(
    feature_cols, feature_data
):
    with col:
        st.markdown(
            f'<div class="info-card">'
            f'<span class="pill">{emoji} FARM2MARKET</span>'
            f'<h3>{title}</h3>'
            f'<p>{description}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.write("")


# Fetch live data
crops_to_fetch = CROPS if show_all_crops else [selected_crop]

live_rows = []
fetch_errors = {}

with st.spinner("Fetching available mandi prices..."):
    for crop_name in crops_to_fetch:
        rows, error = fetch_crop_prices(crop_name)
        live_rows.extend(rows)

        if error:
            fetch_errors[crop_name] = error

live_df = pd.DataFrame(live_rows)

if not live_df.empty:
    st.success(
        f"Loaded {len(live_df)} price record(s) from the "
        "third-party API. Check arrival dates to confirm freshness."
    )
else:
    st.warning(
        "Live prices could not be loaded. The comparison uses "
        "sample demonstration data, not current mandi prices."
    )

for crop_name, error in fetch_errors.items():
    with st.expander(f"Connection details: {crop_name}"):
        st.caption(error)


if live_df.empty:
    market_data = SAMPLE_DATA.copy()

else:
    live_crops = set(
        live_df["Crop"].astype(str).str.lower().unique()
    )

    fallback_crops = [
        crop for crop in CROPS
        if crop.lower() not in live_crops
    ]

    market_data = live_df.copy()

    if fallback_crops:
        sample_fallback = SAMPLE_DATA[
            SAMPLE_DATA["Crop"].isin(fallback_crops)
        ].copy()

        market_data = pd.concat(
            [market_data, sample_fallback],
            ignore_index=True,
            sort=False,
        )

        st.info(
            "Sample prices are used for crops without usable "
            "live records: " + ", ".join(fallback_crops)
        )


# Market snapshot
crop_data = market_data[
    market_data["Crop"].astype(str).str.lower()
    == selected_crop.lower()
].copy()

st.markdown(
    '<div class="section-title">📍 Market snapshot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="section-sub">Listed prices for '
    f'<b>{selected_crop}</b> in {STATE}.</div>',
    unsafe_allow_html=True,
)

if not crop_data.empty:
    price_col = "Price (₹/quintal)"

    crop_data[price_col] = pd.to_numeric(
        crop_data[price_col],
        errors="coerce",
    )

    usable_prices = crop_data.dropna(subset=[price_col])

    if not usable_prices.empty:
        avg_price = float(
            usable_prices[price_col].mean()
        )

        low_idx = usable_prices[price_col].idxmin()
        high_idx = usable_prices[price_col].idxmax()

        low_price = float(
            usable_prices.loc[low_idx, price_col]
        )

        high_price = float(
            usable_prices.loc[high_idx, price_col]
        )

        low_market = str(
            usable_prices.loc[low_idx, "Market"]
        )

        high_market = str(
            usable_prices.loc[high_idx, "Market"]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average listed price",
            f"₹{avg_price:,.0f}",
        )

        col2.metric(
            "Lowest listed price",
            f"₹{low_price:,.0f}",
        )

        col3.metric(
            "Highest listed price",
            f"₹{high_price:,.0f}",
        )

        st.caption(
            f"Prices are per quintal. Lowest: {low_market} · "
            f"Highest: {high_market}. Listed prices may refer "
            "to different arrival dates."
        )

    else:
        st.info("No usable prices are available for this crop.")

else:
    st.info("No records are available for the selected crop.")


# Market comparison table and chart
st.markdown(
    '<div class="section-title">📊 Market price comparison</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">Compare mandi listings and '
    'spot the highest listed price.</div>',
    unsafe_allow_html=True,
)

if not crop_data.empty:
    display_cols = [
        col for col in [
            "Crop",
            "Market",
            "District",
            "State",
            "Arrival date",
            "Variety",
            "Min price (₹/quintal)",
            "Max price (₹/quintal)",
            "Price (₹/quintal)",
            "Data source",
        ]
        if col in crop_data.columns
    ]

    st.dataframe(
        crop_data[display_cols].sort_values(
            "Price (₹/quintal)",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )

    chart_data = crop_data[
        ["Market", "Price (₹/quintal)"]
    ].copy()

    chart_data["Price (₹/quintal)"] = pd.to_numeric(
        chart_data["Price (₹/quintal)"],
        errors="coerce",
    )

    chart_data = chart_data.dropna().set_index("Market")

    if not chart_data.empty:
        st.bar_chart(chart_data)

else:
    st.info(
        "The comparison chart will appear when price data is available."
    )


# Farm picture gallery
st.markdown(
    '<div class="section-title">🌾 From farm to market</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">Better information helps build '
    'a stronger connection between farms and markets.</div>',
    unsafe_allow_html=True,
)

img1, img2, img3 = st.columns(3)

with img1:
    st.image(
        FIELD_IMAGE,
        use_container_width=True,
        caption="Healthy fields, better harvests",
    )

with img2:
    st.image(
        VEGETABLE_IMAGE,
        use_container_width=True,
        caption="Know the value of your crop",
    )

with img3:
    st.image(
        FARMER_IMAGE,
        use_container_width=True,
        caption="Supporting farmer decisions",
    )


# Demonstration forecast
st.markdown(
    '<div class="section-title">🔮 7-day price trend</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">Illustrative demonstration forecast — '
    'not a trained model or a prediction from live market history.</div>',
    unsafe_allow_html=True,
)

seed = CROPS.index(selected_crop) + 17
rng = np.random.default_rng(seed)
today = date.today()

history_dates = [
    today - timedelta(days=day)
    for day in range(13, -1, -1)
]

if not crop_data.empty:
    current_prices = pd.to_numeric(
        crop_data["Price (₹/quintal)"],
        errors="coerce",
    ).dropna()

    base_price = (
        float(current_prices.mean())
        if not current_prices.empty else 2000.0
    )

else:
    base_price = float(
        SAMPLE_DATA.loc[
            SAMPLE_DATA["Crop"] == selected_crop,
            "Price (₹/quintal)",
        ].mean()
    )

synthetic_history = []

for i, day in enumerate(history_dates):
    trend = 1 + (i / 13) * 0.015
    variation = rng.normal(0, 0.025)

    synthetic_history.append({
        "Date": pd.Timestamp(day),
        "Price (₹/quintal)": max(
            1, base_price * (trend + variation)
        ),
    })

forecast_rows = []
last_history_price = synthetic_history[-1]["Price (₹/quintal)"]

for i, day in enumerate(
    [today + timedelta(days=day) for day in range(1, 8)],
    start=1,
):
    forecast_rows.append({
        "Date": pd.Timestamp(day),
        "Forecast price (₹/quintal)": max(
            1,
            last_history_price * (
                1 + 0.0015 * i + rng.normal(0, 0.012)
            ),
        ),
    })

fc1, fc2 = st.columns(2)

with fc1:
    st.markdown("**Illustrative recent trend**")
    st.line_chart(
        pd.DataFrame(synthetic_history).set_index("Date")
    )

with fc2:
    st.markdown("**Illustrative next 7 days**")
    st.line_chart(
        pd.DataFrame(forecast_rows).set_index("Date")
    )


# Price target checker
st.markdown(
    '<div class="section-title">🔔 Price target checker</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">Set a target and check prices '
    'loaded in this session. This does not send background '
    'notifications.</div>',
    unsafe_allow_html=True,
)

alert_col1, alert_col2 = st.columns([2, 1])

with alert_col1:
    target_price = st.number_input(
        "Alert me when listed price is at or below (₹/quintal)",
        min_value=1,
        value=max(1, int(round(base_price * 0.9))),
        step=50,
    )

with alert_col2:
    st.write("")
    st.write("")
    check_alert = st.button(
        "Check my target",
        use_container_width=True,
    )

if check_alert:
    if crop_data.empty:
        st.warning("No price records are available to check.")

    else:
        numeric_prices = pd.to_numeric(
            crop_data["Price (₹/quintal)"],
            errors="coerce",
        )

        matches = crop_data[
            numeric_prices <= target_price
        ]

        if not matches.empty:
            st.success(
                f"Target reached: {len(matches)} listed price(s) "
                f"for {selected_crop} are at or below "
                f"₹{target_price:,.0f}/quintal."
            )

            st.dataframe(
                matches,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info(
                f"No listed price for {selected_crop} is at or "
                f"below ₹{target_price:,.0f}/quintal right now."
            )


# Footer
st.markdown("""
<div class="footer">
    <b>🌱 Farm2Market</b> · Smart agriculture, clearer market choices.<br>
    Project note: Live records come from a third-party API.
    Sample prices are labelled when used.
    Forecast values are illustrative only.
</div>
""", unsafe_allow_html=True)
