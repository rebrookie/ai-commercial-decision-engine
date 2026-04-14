from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.insight_generator import generate_insight
from src.recommendation_engine import generate_recommendation

def main():
    df = load_data("data/sales_data.csv")

    kpis = calculate_kpis(df)
    print("KPIs:\n", kpis)

    insight = generate_insight(kpis)
    print("\nInsight:\n", insight)

    recommendation = generate_recommendation(insight)
    print("\nRecommendation:\n", recommendation)

if __name__ == "__main__":
    main()

