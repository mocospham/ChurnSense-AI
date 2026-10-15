"""Reproducible churn model training + export for a no-install browser demo."""
from pathlib import Path
import csv
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score, accuracy_score, confusion_matrix

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
RESULTS = ROOT / 'results'
RESULTS.mkdir(exist_ok=True)

FEATURES = [
    'tenure_months', 'monthly_transactions', 'avg_balance_million_vnd',
    'app_login_days_30d', 'complaints_90d', 'product_count',
    'digital_usage_pct', 'inactive_days'
]
TARGET = 'churn_next_30d'

df = pd.read_csv(DATA / 'customers_synthetic.csv', encoding='utf-8-sig')
X_train, X_test, y_train, y_test = train_test_split(
    df[FEATURES], df[TARGET], test_size=0.25,
    stratify=df[TARGET], random_state=42
)
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000, random_state=42))
])
pipe.fit(X_train, y_train)
y_proba = pipe.predict_proba(X_test)[:, 1]
y_pred = (y_proba >= 0.5).astype(int)
cm = confusion_matrix(y_test, y_pred)
metrics = {
    'n_customers': int(len(df)),
    'training_samples': int(len(X_train)),
    'test_samples': int(len(X_test)),
    'synthetic_churn_rate': round(float(df[TARGET].mean()), 4),
    'roc_auc_test': round(float(roc_auc_score(y_test, y_proba)), 4),
    'precision_test_at_0_5': round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
    'recall_test_at_0_5': round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
    'accuracy_test_at_0_5': round(float(accuracy_score(y_test, y_pred)), 4),
    'confusion_matrix_tn_fp_fn_tp': [int(cm[0,0]), int(cm[0,1]), int(cm[1,0]), int(cm[1,1])],
    'risk_threshold': 0.5,
    'disclaimer': 'Toy exercise on synthetically generated records. Scores do not validate bank use or performance on real customers.'
}

scaler, model = pipe.named_steps['scaler'], pipe.named_steps['model']
coef = model.coef_[0]
with (RESULTS/'model_parameters.json').open('w', encoding='utf-8') as f:
    json.dump({
        'features': FEATURES,
        'means': scaler.mean_.tolist(),
        'scales': scaler.scale_.tolist(),
        'coefficients': coef.tolist(),
        'intercept': float(model.intercept_[0]),
        'threshold': 0.5
    }, f, ensure_ascii=False, indent=2)
with (RESULTS/'metrics.json').open('w', encoding='utf-8') as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)
joblib.dump(pipe, RESULTS/'churn_model.joblib')

out = df.copy()
out['risk_score'] = pipe.predict_proba(df[FEATURES])[:, 1].round(4)
out['pred_high_risk'] = (out['risk_score'] >= 0.5).astype(int)
out.to_csv(DATA/'customers_scored.csv', index=False, encoding='utf-8-sig')

labels = {
    'tenure_months': 'Thời gian gắn bó',
    'monthly_transactions': 'Giao dịch / tháng',
    'avg_balance_million_vnd': 'Số dư TB (triệu VND)',
    'app_login_days_30d': 'Ngày đăng nhập / 30 ngày',
    'complaints_90d': 'Khiếu nại / 90 ngày',
    'product_count': 'Số sản phẩm',
    'digital_usage_pct': 'Tỷ lệ sử dụng số (%)',
    'inactive_days': 'Ngày không hoạt động',
}
with (RESULTS/'coefficients.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['feature', 'feature_label', 'standardized_coefficient', 'direction'])
    for feat, c in sorted(zip(FEATURES, coef), key=lambda row: -abs(row[1])):
        w.writerow([feat, labels[feat], round(float(c), 4), 'Tăng nguy cơ' if c > 0 else 'Giảm nguy cơ'])

print(json.dumps(metrics, ensure_ascii=False, indent=2))
