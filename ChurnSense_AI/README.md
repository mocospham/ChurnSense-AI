# ChurnSense AI — Dự đoán nguy cơ khách hàng rời bỏ

**Portfolio demo | Python / scikit-learn / T-SQL / Dashboard HTML**  
**Người trình bày:** Phạm Trọng Đạt  
**Quan trọng:** Toàn bộ dữ liệu được mô phỏng, không phải dữ liệu ngân hàng thực.

## 1. Ý tưởng

Giả định một tổ chức tài chính muốn nhận biết **nhóm khách hàng có nguy cơ ngừng sử dụng dịch vụ trong 30 ngày tới** để ưu tiên chăm sóc. Dự án mô phỏng quy trình từ dữ liệu giao dịch/tương tác, huấn luyện thuật toán Logistic Regression đến dashboard trình diễn dự đoán.

Đầu ra là **xác suất dự đoán (risk score)**, không phải kết luận khách hàng chắc chắn rời bỏ.

## 2. Mở demo ngay — không cần cài đặt

Mở tệp **`ChurnSense_Demo.html`** bằng Chrome, Safari, Firefox hoặc Edge. Demo chạy **offline**, có thể:

- Xem tổng quan 1.200 khách hàng mô phỏng và phân phối xác suất;
- Thay đổi 8 biến của một khách hàng thử nghiệm để nhận điểm dự đoán mới;
- Lọc/tìm mã khách hàng, chọn hồ sơ để đưa lên mô hình;
- Xuất danh sách khách hàng giả lập theo bộ lọc thành CSV;
- Quan sát chiều ảnh hưởng của các hệ số Logistic Regression.

> Không mở `ChurnSense_Demo.html` trong ứng dụng xem văn bản thuần nếu muốn thử các thanh kéo: dùng trình duyệt web.

## 3. Cách xây dựng lại dự án

Có Python 3.10+:

```bash
python -m pip install -r requirements.txt
python generate_data.py
python train_model.py
python build_dashboard.py
```

**Để tái hiện kết quả**, giữ nguyên random seeds trong 2 script. 

### Quy trình

1. Tạo 1.200 hồ sơ **nhân tạo** với thời gian gắn bó, giao dịch/tháng, số dư bình quân, ngày đăng nhập ứng dụng, số lần khiếu nại, số sản phẩm, tỷ lệ sử dụng số và số ngày không hoạt động.
2. Gán nhãn `churn_next_30d` bằng xác suất mô phỏng (có thêm nhiễu), không dựa trên bất kỳ khách hàng thật nào.
3. Chia dữ liệu huấn luyện/kiểm thử **75% / 25%**, giữ tỷ lệ nhãn (`stratify`), random state = 42.
4. Huấn luyện pipeline **StandardScaler + LogisticRegression** trên tập training; scaler chỉ fit trong training pipeline để tránh rò rỉ dữ liệu.
5. Đo ROC-AUC, accuracy, precision và recall trên tập test chưa dùng để huấn luyện.
6. Xuất xác suất cho bộ dữ liệu mô phỏng và dựng dashboard tương tác (dùng đúng trọng số scaler/mô hình xuất ra).

## 4. Kết quả test (chỉ trên dữ liệu mô phỏng)

| Chỉ số | Giá trị |
|---|---:|
| Quy mô | 1.200 hồ sơ mô phỏng |
| Huấn luyện / test | 900 / 300 |
| ROC-AUC | 0.748 |
| Accuracy (threshold 0.50) | 74.7% |
| Precision (threshold 0.50) | 67.5% |
| Recall (threshold 0.50) | 30.0% |

**Lưu ý:** Recall chưa cao ở ngưỡng 0.50; đây là một giới hạn cần giải thích. Việc đổi ngưỡng có thể giúp phát hiện nhiều trường hợp hơn nhưng đánh đổi bằng nhiều cảnh báo sai. Vì dữ liệu là giả lập, các chỉ số này không thể được hiểu là kết quả đạt được trên dữ liệu thực.

## 5. T-SQL

`sql/analysis.sql` gồm 4 truy vấn cho SQL Server: thống kê tổng, phân tích theo số sản phẩm, phân nhóm theo thời gian không hoạt động và danh sách 15 mã có điểm rủi ro cao nhất.

Nếu muốn thử truy vấn, hãy nhập `data/customers_scored.csv` vào SQL Server với **SSMS > Tasks > Import Flat File** và đặt bảng `dbo.SyntheticChurnScored`. Trường `risk_score` là số thập phân (FLOAT/DECIMAL), `customer_id` là VARCHAR, các biến còn lại là số nguyên hoặc số thập phân tương ứng.

## 6. Cấu trúc thư mục

```text
ChurnSense_Demo.html           # Demo tương tác chạy offline
Du_an_ChurnSense_1_trang.pdf  # Tóm tắt portfolio
README.md                      # Hướng dẫn + phương pháp
requirements.txt

generate_data.py              # Tạo dữ liệu mô phỏng
train_model.py                # Huấn luyện / đo lường / xuất kết quả
build_dashboard.py            # Đóng gói mô hình và dữ liệu vào HTML

data/customers_synthetic.csv  # Bản dữ liệu chưa chấm điểm
data/customers_scored.csv     # Bản dữ liệu có điểm AI
sql/analysis.sql               # Truy vấn T-SQL
results/metrics.json          # Chỉ số test
results/model_parameters.json # Hệ số để chạy offline
results/churn_model.joblib     # Pipeline mô hình Python
results/coefficients.csv      # Hệ số các biến
```

## 7. Hạn chế và đạo đức sử dụng

- Đây là bài thực hành để **minh họa năng lực phân tích** và thử ý tưởng; không dùng dữ liệu thật, không có sự xác nhận bởi ngân hàng nào.
- Nhãn nhân tạo được sinh dựa trên công thức có chủ đích, nên không phản ánh hành vi thực tế, nguy cơ drift, sai lệch mẫu và fairness trong môi trường vận hành.
- Không dùng điểm nguy cơ để đưa ra quyết định bất lợi đối với khách hàng; đánh giá riêng quyền riêng tư, hiệu năng, tính giải thích, fairness và pháp lý khi làm dự án thật.
- Nếu dùng trong hồ sơ ứng tuyển, nên nói đây là **dự án thực hành có sử dụng AI hỗ trợ xây dựng**, và chỉ mô tả những bước bạn đã chạy, kiểm tra hoặc hiểu rõ.

## 8. Đoạn giới thiệu portfolio (có thể tùy chỉnh sau khi tự chạy thử)

> ChurnSense là dự án thực hành dự đoán nguy cơ khách hàng rời bỏ dịch vụ, sử dụng Python, scikit-learn, SQL Server và dashboard tương tác. Dự án thực hiện mô phỏng 1.200 hồ sơ, xử lý dữ liệu, huấn luyện Logistic Regression và đánh giá ROC-AUC trên tập test. Toàn bộ dữ liệu là giả lập; demo cho phép điều chỉnh chỉ số sử dụng dịch vụ để quan sát thay đổi của điểm dự đoán.
