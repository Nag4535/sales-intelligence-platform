import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="Real-Time Sales Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# ── LOAD DATA ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df           = pd.read_csv('data/sales_clean.csv')
    monthly      = pd.read_csv('data/monthly_summary.csv')
    category     = pd.read_csv('data/category_summary.csv')
    region       = pd.read_csv('data/region_summary.csv')
    forecast     = pd.read_csv('data/sales_forecast.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    forecast['Date'] = pd.to_datetime(forecast['Date'])
    return df, monthly, category, region, forecast

df, monthly, category, region, forecast = load_data()

# ── SIDEBAR ───────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/combo-chart.png", width=80)
st.sidebar.title("Sales Intelligence")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Trends & Forecast", "Products & Customers", "Regional Analysis"]
)

year_filter = st.sidebar.multiselect(
    "Filter by Year",
    options=sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

category_filter = st.sidebar.multiselect(
    "Filter by Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Apply filters
df_filtered = df[
    (df['Year'].isin(year_filter)) &
    (df['Category'].isin(category_filter))
]

# ── PAGE 1: OVERVIEW ──────────────────────────────────────
if page == "Overview":
    st.title("Sales Intelligence Platform")
    st.markdown("### Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales",    f"${df_filtered['Sales'].sum():,.0f}")
    with col2:
        st.metric("Total Orders",   f"{len(df_filtered):,}")
    with col3:
        st.metric("Avg Order Value", f"${df_filtered['Sales'].mean():,.0f}")
    with col4:
        st.metric("Total Customers", f"{df_filtered['Customer Name'].nunique():,}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        cat_sales = df_filtered.groupby('Category')['Sales'].sum().reset_index()
        fig = px.pie(cat_sales, values='Sales', names='Category',
                     title='Sales by Category',
                     color_discrete_sequence=['#C8FF00', '#FF6B35', '#38BDF8'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        seg_sales = df_filtered.groupby('Segment')['Sales'].sum().reset_index()
        fig = px.bar(seg_sales, x='Segment', y='Sales',
                     title='Sales by Segment',
                     color='Segment',
                     color_discrete_sequence=['#C8FF00', '#FF6B35', '#38BDF8'])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Sales by Sub-Category")
    sub_sales = df_filtered.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(sub_sales, x='Sales', y='Sub-Category',
                 orientation='h',
                 title='Sales by Sub-Category',
                 color='Sales',
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

# ── PAGE 2: TRENDS & FORECAST ─────────────────────────────
elif page == "Trends & Forecast":
    st.title("Sales Trends & Forecasting")

    monthly_filtered = df_filtered.groupby('YearMonth')['Sales'].sum().reset_index()
    fig = px.line(monthly_filtered, x='YearMonth', y='Sales',
                  title='Monthly Sales Trend',
                  labels={'Sales': 'Total Sales ($)', 'YearMonth': 'Month'},
                  color_discrete_sequence=['#C8FF00'])
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 12-Month Sales Forecast")
    future_forecast = forecast[forecast['Date'] > df['Order Date'].max()]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast['Date'], y=forecast['ForecastedSales'],
        name='Forecast', line=dict(color='#C8FF00', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast['Date'], y=future_forecast['UpperBound'],
        fill=None, line=dict(color='rgba(200,255,0,0.3)'), name='Upper Bound'
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast['Date'], y=future_forecast['LowerBound'],
        fill='tonexty', line=dict(color='rgba(200,255,0,0.3)'), name='Lower Bound'
    ))
    fig.update_layout(title='Sales Forecast — Next 12 Months',
                      xaxis_title='Date', yaxis_title='Sales ($)')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Forecasted Daily Sales",
                  f"${future_forecast['ForecastedSales'].mean():,.0f}")
    with col2:
        st.metric("Max Forecasted Sales",
                  f"${future_forecast['UpperBound'].max():,.0f}")
    with col3:
        st.metric("Min Forecasted Sales",
                  f"${future_forecast['LowerBound'].min():,.0f}")

# ── PAGE 3: PRODUCTS & CUSTOMERS ──────────────────────────
elif page == "Products & Customers":
    st.title("Products & Customer Analysis")

    col1, col2 = st.columns(2)
    with col1:
        top_products = df_filtered.groupby('Product Name')['Sales'].sum()\
            .sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(top_products, x='Sales', y='Product Name',
                     orientation='h', title='Top 10 Products by Sales',
                     color_discrete_sequence=['#C8FF00'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_customers = df_filtered.groupby('Customer Name')['Sales'].sum()\
            .sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(top_customers, x='Sales', y='Customer Name',
                     orientation='h', title='Top 10 Customers by Sales',
                     color_discrete_sequence=['#FF6B35'])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Sales by Ship Mode")
    ship_sales = df_filtered.groupby('Ship Mode')['Sales'].sum().reset_index()
    fig = px.pie(ship_sales, values='Sales', names='Ship Mode',
                 title='Sales Distribution by Ship Mode',
                 color_discrete_sequence=['#C8FF00', '#FF6B35', '#38BDF8', '#A78BFA'])
    st.plotly_chart(fig, use_container_width=True)

# ── PAGE 4: REGIONAL ANALYSIS ─────────────────────────────
elif page == "Regional Analysis":
    st.title("Regional Sales Analysis")

    col1, col2 = st.columns(2)
    with col1:
        region_sales = df_filtered.groupby('Region')['Sales'].sum().reset_index()
        fig = px.bar(region_sales, x='Region', y='Sales',
                     title='Sales by Region',
                     color='Region',
                     color_discrete_sequence=['#C8FF00', '#FF6B35', '#38BDF8', '#A78BFA'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        state_sales = df_filtered.groupby('State')['Sales'].sum().reset_index()
        fig = px.choropleth(state_sales,
                            locations='State',
                            locationmode='USA-states',
                            color='Sales',
                            scope='usa',
                            title='Sales by State',
                            color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top 10 States by Sales")
    top_states = df_filtered.groupby('State')['Sales'].sum()\
        .sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_states, x='State', y='Sales',
                 title='Top 10 States by Sales',
                 color_discrete_sequence=['#C8FF00'])
    st.plotly_chart(fig, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Nagarajulu Reddy Nalla**")
st.sidebar.markdown("Data Analyst | Power BI | Python")