def calculate_kpis(df):
    kpis = {}

    df = df.copy()
    df['date'] = df['date'].astype(str)

    # ------------------------
    # Core KPIs
    # ------------------------
    total_revenue = df['revenue'].sum()
    total_volume = df['volume'].sum()
    avg_price = total_revenue / total_volume if total_volume != 0 else 0

    # ------------------------
    # Price Erosion (deal level)
    # ------------------------
    df['price_erosion'] = df.apply(
        lambda x: (x['price'] / x['last_year_price'] - 1)
        if x['last_year_price'] not in [0, None]
        else None,
        axis=1
    )

    # 👉 Revenue-weighted erosion（商业更合理）
    price_erosion = (
        (df['price_erosion'] * df['revenue']).sum() / total_revenue
        if total_revenue != 0 else None
    )

    # ------------------------
    # Formatted KPIs (for UI)
    # ------------------------
    kpis = {
        "Total Revenue": f"{total_revenue:,.0f}",
        "Total Volume": f"{total_volume:,.0f}",
        "Average Price": f"{avg_price:.2f}",
        "Price Erosion": f"{price_erosion:.2%}" if price_erosion is not None else "N/A"
    }

    # ------------------------
    # Monthly Trend
    # ------------------------
    df_sorted = df.sort_values('date')

    monthly = df_sorted.groupby('date').agg({
        'revenue': 'sum',
        'volume': 'sum'
    }).reset_index()

    monthly['revenue_growth'] = monthly['revenue'].pct_change()

    # ------------------------
    # Raw KPIs (for logic / AI)
    # ------------------------
    kpis['total_revenue'] = total_revenue
    kpis['total_volume'] = total_volume
    kpis['avg_price'] = round(avg_price, 2)
    kpis['price_erosion'] = price_erosion
    kpis['monthly_trend'] = monthly.to_dict(orient='records')

    return kpis