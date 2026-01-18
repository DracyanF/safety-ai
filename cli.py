import typer
from app.qdrant_client import create_collection
from app.ingest import ingest_crime_reports
from app.search import search_similar_crimes
from app.hotspots import detect_hotspots
from app.trends import detect_trends
from app.risk import compute_risk_scores
from app.patrol import recommend_patrols
from app.explain import explain_patrol_recommendation





app = typer.Typer()

@app.command()
def setup():
    create_collection()
    ingest_crime_reports()

@app.command()
def search(
    query: str,
    lat: float = typer.Option(None),
    lon: float = typer.Option(None),
    radius_km: float = typer.Option(None),
    days: int = typer.Option(None)
):
    results = search_similar_crimes(
        query=query,
        lat=lat,
        lon=lon,
        radius_km=radius_km,
        days=days
    )

    for point in results:
        print(point.payload)

@app.command()
def hotspots(
    days: int = typer.Option(30),
    threshold: int = typer.Option(3)
):
    """
    Detect crime hotspots in the last N days.
    """
    results = detect_hotspots(days=days, threshold=threshold)

    if not results:
        print("✅ No hotspots detected.")
        return

    for hotspot in results:
        print("\n🚨 HOTSPOT DETECTED 🚨")
        print(f"Area: {hotspot['area']}")
        print(f"Incidents: {hotspot['incident_count']}")

        for inc in hotspot["incidents"]:
            print(
                f" - {inc['crime_type']} | severity={inc['severity']} | ts={inc['timestamp']}"
            )

@app.command()
def trends(
    window_days: int = typer.Option(15)
):
    """
    Detect crime trends (rising / stable / declining).
    """
    results = detect_trends(window_days=window_days)

    if not results:
        print("No trend data available.")
        return

    for t in results:
        emoji = "🔺" if t["trend"] == "rising" else "🔻" if t["trend"] == "declining" else "➖"

        print(
            f"{emoji} {t['area']} | "
            f"recent={t['recent_count']} | "
            f"previous={t['previous_count']} | "
            f"delta={t['delta']}"
        )

@app.command()
def risk(
    days: int = typer.Option(30)
):
    """
    Compute crime risk scores per area.
    """
    results = compute_risk_scores(days=days)

    if not results:
        print("No risk data available.")
        return

    for r in results:
        level = (
            "HIGH" if r["risk_score"] >= 60
            else "MEDIUM" if r["risk_score"] >= 30
            else "LOW"
        )

        print(
            f"🚦 {r['area']} | "
            f"Risk={r['risk_score']} ({level}) | "
            f"Crimes={r['crime_count']} | "
            f"Avg Severity={r['avg_severity']} | "
            f"Trend={r['trend']}"
        )

@app.command()
def patrols(
    days: int = typer.Option(30)
):
    """
    Generate patrol recommendations based on crime risk.
    """
    results = recommend_patrols(days=days)

    for rec in results:
        print("\n🚓 PATROL RECOMMENDATION")
        print(f"Area: {rec['area']}")
        print(f"Risk Score: {rec['risk_score']}")
        print(f"Priority: {rec['priority']}")
        print(f"Patrol Units: {rec['patrol_units']}")
        print(f"Recommended Time: {rec['recommended_time']}")
        print(f"Trend: {rec['trend']}")

@app.command()
def patrols(
    days: int = typer.Option(30)
):
    """
    Generate patrol recommendations with explanations.
    """
    results = recommend_patrols(days=days)

    for rec in results:
        print("\n🚓 PATROL RECOMMENDATION")
        print(f"Area: {rec['area']}")
        print(f"Risk Score: {rec['risk_score']}")
        print(f"Priority: {rec['priority']}")
        print(f"Patrol Units: {rec['patrol_units']}")
        print(f"Recommended Time: {rec['recommended_time']}")
        print(f"Trend: {rec['trend']}")
        print("\n🧠 Explanation:")
        print(explain_patrol_recommendation(rec))


if __name__ == "__main__":
    app()
