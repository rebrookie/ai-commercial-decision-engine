def calculate_kpis(df):
    kpis = {}

    df['date'] = df['date'].astype(str)

    total_revenue = df['revenue'].sum()
    total_volume = df['volume'].sum()
    avg_price = total_revenue / total_volume
    #price_erosion = df['last_year_price'] / df['price'] - 1

    kpis = {
        "Total Revenue": f"{total_revenue:,.0f}",
        "Total Volume": f"{total_volume:,.0f}",
        "Average Price": f"{avg_price:.2f}"
        #"Price Development": f"{price_erosion:.2f}"
    }


    # 按时间排序
    df_sorted = df.sort_values('date')

    # 按月聚合
    monthly = df_sorted.groupby('date').agg({
        'revenue': 'sum',
        'volume': 'sum'
    }).reset_index()

    # 增长率计算
    monthly['revenue_growth'] = monthly['revenue'].pct_change()

    kpis['total_revenue'] = total_revenue
    kpis['total_volume'] = total_volume
    kpis['avg_price'] = round(avg_price, 2)
    kpis['monthly_trend'] = monthly.to_dict(orient='records')

    


    return kpis