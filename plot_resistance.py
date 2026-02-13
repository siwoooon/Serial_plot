import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read CSV
csv_path = "EDA_20260211_183305.csv"
df = pd.read_csv(csv_path)

# Ensure expected columns
if df.shape[1] < 2:
    raise SystemExit("CSV does not have expected 2 columns: Time and Resistance")

df.columns = [c.strip() for c in df.columns[:2]]

time_col = df.columns[0]
res_col = df.columns[1]

# Parse resistance numeric value
def parse_res(s):
    if pd.isna(s):
        return None
    s = str(s)
    # Try to find a number before 'ohm'
    m = re.search(r"([0-9]+\.?[0-9]*)\s*ohm", s)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    # Fallback: find any number
    m2 = re.search(r"([0-9]+\.?[0-9]*)", s)
    if m2:
        return float(m2.group(1))
    return None

df['res_ohm'] = df[res_col].apply(parse_res)

# Parse time (only hh:mm:ss[.ms])
try:
    df['time_dt'] = pd.to_datetime(df[time_col], format='%H:%M:%S.%f')
except Exception:
    df['time_dt'] = pd.to_datetime(df[time_col], errors='coerce')

# If parsing produced times without a date, convert to elapsed seconds
if df['time_dt'].notna().any():
    t0 = df['time_dt'].iloc[0]
    df['elapsed_s'] = (df['time_dt'] - t0).dt.total_seconds()
else:
    df['elapsed_s'] = df.index.astype(float)

# Drop rows without numeric resistance
plot_df = df.dropna(subset=['res_ohm'])

# Plot
plt.figure(figsize=(10,4))
plt.plot(plot_df['elapsed_s'], plot_df['res_ohm'], marker='.', linestyle='-', markersize=3)
plt.xlabel('Elapsed time (s)')
plt.ylabel('Resistance (Ohm)')
#plt.title('Resistance vs Time')
plt.grid(alpha=0.4)
plt.tight_layout()

out_png = 'resistance_plot2.png'
plt.savefig(out_png, dpi=150)
print(f"Saved plot to {out_png}")
