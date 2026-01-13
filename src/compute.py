import pandas as pd

# ---------- Load CSV files ----------
pnl_actual = pd.read_csv("data/pnl_actual.csv")
pnl_budget = pd.read_csv("data/pnl_budget.csv")

bs_current = pd.read_csv("data/bs_current.csv")
bs_prior = pd.read_csv("data/bs_prior.csv")

# ---------- P&L Variance Analysis ----------
pnl = pnl_actual.merge(
    pnl_budget,
    on=["Account", "Category"],
    suffixes=("_actual", "_budget")
)

pnl["variance"] = pnl["Amount_actual"] - pnl["Amount_budget"]
pnl["pct_variance"] = pnl["variance"] / pnl["Amount_budget"]

print("\n==============================")
print("P&L VARIANCE ANALYSIS")
print("==============================")
print(pnl[["Account", "Amount_actual", "Amount_budget", "variance", "pct_variance"]])

# ---------- Top 3 Variance Drivers ----------
pnl["abs_variance"] = pnl["variance"].abs()
top_drivers = pnl.sort_values("abs_variance", ascending=False).head(3)

print("\n==============================")
print("TOP 3 VARIANCE DRIVERS")
print("==============================")
print(top_drivers[["Account", "variance"]])

# ---------- SaaS Margin Metrics ----------
revenue = pnl[pnl["Category"] == "Revenue"]["Amount_actual"].sum()
cogs = pnl[pnl["Category"] == "COGS"]["Amount_actual"].sum()
opex = pnl[pnl["Category"] == "Opex"]["Amount_actual"].sum()

gross_margin_pct = (revenue + cogs) / revenue
operating_margin_pct = (revenue + cogs + opex) / revenue

print("\n==============================")
print("SAAS MARGIN METRICS")
print("==============================")
print(f"Gross Margin %: {gross_margin_pct:.2%}")
print(f"Operating Margin %: {operating_margin_pct:.2%}")

# ---------- Balance Sheet Month-over-Month Changes ----------
bs = bs_current.merge(
    bs_prior,
    on=["Account", "Category"],
    suffixes=("_current", "_prior")
)

bs["change"] = bs["Amount_current"] - bs["Amount_prior"]

print("\n==============================")
print("BALANCE SHEET MoM CHANGES")
print("==============================")
print(bs[["Account", "Amount_prior", "Amount_current", "change"]])
