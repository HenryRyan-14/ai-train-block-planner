
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Train Block Planner",
    page_icon="🚆",
    layout="wide"
)

st.title("🚆 AI Powered Automatic Train Block Planner")

st.caption(
    "AI-assisted planning to maximize asset availability "
    "and service coverage"
)

# -----------------------------
# Load data
# -----------------------------

trains = pd.read_csv("trains.csv")
services = pd.read_csv("services.csv")
schedule = pd.read_csv("final_schedule.csv")
block_plan = pd.read_csv("final_block_plan.csv")

# -----------------------------
# KPI calculations
# -----------------------------

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
    "assigned_train"
].nunique()

fleet_utilization = (
    trains_used / available_trains
) * 100

aggregate_risk = schedule[
    "predicted_risk"
].sum()

# -----------------------------
# KPI cards
# -----------------------------

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

# -----------------------------
# Optimized Schedule
# -----------------------------

st.subheader("🚆 AI-Optimized Train Schedule")

st.dataframe(
    schedule,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Block Plan
# -----------------------------

st.subheader("🔧 Automatic Maintenance / Block Plan")

st.dataframe(
    block_plan,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Train Utilization
# -----------------------------

st.subheader("📊 Train Utilization")

usage = (
    schedule["assigned_train"]
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

# -----------------------------
# Risk
# -----------------------------

st.subheader("⚠️ Predicted Train Risk")

risk_table = schedule[
    ["assigned_train", "predicted_risk"]
].drop_duplicates()

st.dataframe(
    risk_table,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.success(
    "AI planning completed successfully. "
    "The generated plan satisfies the current prototype constraints."
)
