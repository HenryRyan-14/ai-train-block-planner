import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Train Block Planner",
    page_icon="🚆",
    layout="wide"
)

st.title("🚆 AI Powered Automatic Train Block Planner")

st.caption(
    "AI-assisted planning to maximize asset availability, "
    "service coverage and maintenance coordination"
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

trains = pd.read_csv("trains.csv")
services = pd.read_csv("services.csv")
schedule = pd.read_csv("final_schedule.csv")
block_plan = pd.read_csv("final_block_plan.csv")
maintenance = pd.read_csv("maintenance.csv")
failure_history = pd.read_csv("failure_history.csv")

# ---------------------------------------------------------
# BASIC METRICS
# ---------------------------------------------------------

total_services = len(services)

served_services = len(
    schedule[schedule["status"] == "Assigned"]
)

service_coverage = (
    served_services / total_services
) * 100

available_trains = len(
    trains[trains["status"] == "Available"]
)

trains_used = schedule[
    schedule["status"] == "Assigned"
]["assigned_train"].nunique()

fleet_utilization = (
    trains_used / available_trains
) * 100

aggregate_risk = schedule[
    "predicted_risk"
].sum()

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Service Coverage",
    f"{service_coverage:.1f}%"
)

col2.metric(
    "Available Assets",
    f"{available_trains}/{len(trains)}"
)

col3.metric(
    "Fleet Utilization",
    f"{fleet_utilization:.1f}%"
)

col4.metric(
    "Prototype Risk Score",
    f"{aggregate_risk:.0f}"
)

st.divider()

# ---------------------------------------------------------
# AI OPTIMIZED SCHEDULE
# ---------------------------------------------------------

st.subheader("🚆 AI-Optimized Train Schedule")

st.dataframe(
    schedule,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# WHY WAS THIS TRAIN SELECTED?
# ---------------------------------------------------------

st.subheader("🧠 Why was this train assigned?")

assigned_services = schedule[
    schedule["status"] == "Assigned"
].copy()

if len(assigned_services) > 0:

    selected_service = st.selectbox(
        "Select a service",
        assigned_services["service_id"].tolist()
    )

    selected_row = assigned_services[
        assigned_services["service_id"] == selected_service
    ].iloc[0]

    train_id = selected_row["assigned_train"]

    service_row = services[
        services["service_id"] == selected_service
    ].iloc[0]

    train_row = trains[
        trains["train_id"] == train_id
    ].iloc[0]

    st.write(
        f"### Service {selected_service} → Train {train_id}"
    )

    reason_col1, reason_col2 = st.columns(2)

    with reason_col1:

        st.markdown("#### Service requirements")

        st.write(
            f"📍 **Origin:** {service_row.get('origin', 'From route data')}"
        )

        st.write(
            f"🎯 **Required capacity:** "
            f"{service_row['required_capacity']}"
        )

        st.write(
            f"⚡ **Priority:** "
            f"{service_row['priority']}"
        )

    with reason_col2:

        st.markdown("#### Selected train")

        st.write(
            f"🚆 **Train:** {train_id}"
        )

        st.write(
            f"👥 **Capacity:** {train_row['capacity']}"
        )

        st.write(
            f"📍 **Current location:** "
            f"{train_row['current_location']}"
        )

        st.write(
            f"⚠️ **Predicted prototype risk:** "
            f"{selected_row['predicted_risk']}"
        )

   

# ---------------------------------------------------------
# MAINTENANCE / BLOCK PLAN
# ---------------------------------------------------------

st.subheader("🔧 Automatic Maintenance / Block Plan")

st.dataframe(
    block_plan,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# TRAIN UTILIZATION
# ---------------------------------------------------------

st.subheader("📊 Train Utilization")

usage = (
    schedule[
        schedule["status"] == "Assigned"
    ]["assigned_train"]
    .value_counts()
    .reset_index()
)

usage.columns = [
    "train_id",
    "services_operated"
]

st.bar_chart(
    usage.set_index("train_id")
)

# ---------------------------------------------------------
# PREDICTED RISK
# ---------------------------------------------------------

st.subheader("⚠️ Predicted Train Risk")

risk_table = schedule[
    ["assigned_train", "predicted_risk"]
].drop_duplicates()

risk_table = risk_table.sort_values(
    "predicted_risk",
    ascending=False
)

st.dataframe(
    risk_table,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# FAILURE HISTORY
# ---------------------------------------------------------

st.subheader("🔍 Historical Failure Overview")

failure_summary = (
    failure_history
    .groupby("train_id")
    .agg(
        failures=("record_id", "count"),
        downtime_hours=("downtime_hours", "sum")
    )
    .reset_index()
)

failure_summary = failure_summary.sort_values(
    "failures",
    ascending=False
)

st.dataframe(
    failure_summary,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# BEFORE VS AFTER
# ---------------------------------------------------------

st.subheader("🔄 Planning Improvement")

comparison = pd.DataFrame({
    "Metric": [
        "Services served",
        "Service coverage",
        "Trains used",
        "Aggregate prototype risk"
    ],
    "AI Optimized": [
        f"{served_services}/{total_services}",
        f"{service_coverage:.1f}%",
        trains_used,
        f"{aggregate_risk:.0f}"
    ]
})

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)

st.info(
    "The AI-optimized plan maintains service coverage while "
    "considering train eligibility, maintenance conflicts, "
    "service priority and prototype risk."
)


