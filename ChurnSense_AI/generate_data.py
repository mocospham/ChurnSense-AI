"""Create fictitious, privacy-safe tabular data for an educational bank churn demo."""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / 'data'
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(20261015)
n = 1200

tenure = rng.integers(1, 97, n)
products = np.clip(rng.poisson(1.7, n) + 1, 1, 6)
logins = np.clip(np.rint(rng.normal(13, 7, n)), 0, 30).astype(int)
digital = np.clip(np.rint(logins * 2.6 + rng.normal(18, 17, n)), 0, 100).astype(int)
transactions = np.clip(rng.poisson(4 + 0.75 * logins + 1.2 * products), 0, 65)
balance = np.clip(rng.lognormal(2.6, 0.95, n), 0.2, 250).round(1)
complaints = np.clip(rng.poisson(0.27 + (logins < 5) * .55, n), 0, 6)
inactive = np.clip(np.rint(31 - logins * .67 + rng.normal(0, 10, n)), 0, 60).astype(int)

# Not an empirical / regulated-bank model. This deliberately specified relationship
# is ONLY used to produce plausible toy labels for a reproducible demo.
logit = (
    -1.15 + .038 * (inactive - 18) + .54 * complaints
    - .045 * (logins - 13) - .18 * (products - 2.5)
    - .018 * (transactions - 16) - .008 * (tenure - 40)
    - .003 * (digital - 50) - .012 * (balance - 15)
    + rng.normal(0, .50, n)
)
prob = 1 / (1 + np.exp(-logit))
churn = rng.binomial(1, prob, n)

df = pd.DataFrame({
    'customer_id': [f'KH{i:04d}' for i in range(1, n + 1)],
    'tenure_months': tenure,
    'monthly_transactions': transactions,
    'avg_balance_million_vnd': balance,
    'app_login_days_30d': logins,
    'complaints_90d': complaints,
    'product_count': products,
    'digital_usage_pct': digital,
    'inactive_days': inactive,
    'churn_next_30d': churn,
})
df.to_csv(OUT / 'customers_synthetic.csv', index=False, encoding='utf-8-sig')
print(f'Created {len(df):,} synthetic customers | simulated churn rate: {churn.mean():.1%}')
