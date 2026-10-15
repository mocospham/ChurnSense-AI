"""Create a single-page Vietnamese portfolio PDF."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

R=Path(__file__).resolve().parent
out=R/'Du_an_ChurnSense_1_trang.pdf'
m=json.loads((R/'results/metrics.json').read_text(encoding='utf-8'))
params=json.loads((R/'results/model_parameters.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=595.276,841.89
navy=HexColor('#14273A');teal=HexColor('#147F85');ink=HexColor('#213144');muted=HexColor('#637689');light=HexColor('#F3F6F8');line=HexColor('#DEE7EC');orange=HexColor('#B95643')
c=canvas.Canvas(str(out),pagesize=(W,H))

def text(x,y,s,size=10,font='DejaVu',color=ink):
    c.setFont(font,size);c.setFillColor(color);c.drawString(x,y,s)
def textlines(x,y,msg,maxw,size=9,leading=15,font='DejaVu',color=ink):
    for ln in simpleSplit(msg,font,size,maxw):
        text(x,y,ln,size,font,color);y-=leading
    return y

def block(x,y,w,h,fill=light,stroke=None,r=9):
    c.setFillColor(fill);c.setStrokeColor(stroke or fill);c.roundRect(x,y,w,h,r,stroke=bool(stroke),fill=1)

def section(y,label):
    text(40,y,label,11,'DejaVu-Bold',navy);c.setLineWidth(.7);c.setStrokeColor(line);c.line(40,y-8,555,y-8)

c.setFillColor(navy);c.rect(0,H-149,W,149,fill=1,stroke=0)
text(40,H-41,'ChurnSense',25,'DejaVu-Bold',HexColor('#FFFFFF'))
text(210,H-41,'AI',25,'DejaVu-Bold',HexColor('#44D7C1'))
text(40,H-66,'DỰ ÁN PORTFOLIO  •  PHÂN TÍCH DỮ LIỆU & MACHINE LEARNING',8,'DejaVu-Bold',HexColor('#95C9CD'))
text(40,H-97,'Dự đoán nguy cơ khách hàng ngừng sử dụng dịch vụ',12,'DejaVu',HexColor('#F6FBFD'))
text(40,H-120,'Phạm Trọng Đạt  |  Python • scikit-learn • SQL Server • HTML Dashboard',8.4,'DejaVu',HexColor('#D1E5E9'))

section(664,'01  BÀI TOÁN VÀ PHƯƠNG PHÁP')
y=642
y=textlines(40,y,'Xây dựng hệ thống minh họa giúp sàng lọc nhóm khách hàng có nguy cơ rời bỏ trong 30 ngày tới. Dữ liệu được tạo nhân tạo hoàn toàn để thực hành an toàn, không chứa dữ liệu khách hàng thật.',515,9,15)
y-=6
y=textlines(40,y,'Quy trình: mô phỏng dữ liệu → kiểm tra biến → chia train/test 75/25 → chuẩn hóa → huấn luyện Logistic Regression → đánh giá → dashboard thử tình huống.',515,9,15)

section(556,'02  KẾT QUẢ THỰC NGHIỆM (DỮ LIỆU MÔ PHỎNG)')
cards=[('1.200','Hồ sơ giả lập'),('0,748','ROC-AUC (test)'),('74,7%','Accuracy (test)'),('30,0%','Recall (test)')]
card_w=122;gap=9
for i,(v,label) in enumerate(cards):
    x=40+i*(card_w+gap)
    block(x,473,card_w,60,light,r=9)
    text(x+12,500,v,17,'DejaVu-Bold',teal if i<3 else orange)
    text(x+12,482,label,7.6,'DejaVu',muted)
text(42,459,'Tập test: 300 mẫu  •  Ngưỡng cảnh báo: 50%  •  Precision: 67,5%',8,'DejaVu',muted)

section(432,'03  MINH HỌA CÁC BIẾN ĐẦU VÀO')
inputs=[('inactive_days','Số ngày không hoạt động'),('complaints_90d','Số khiếu nại'),('app_login_days_30d','Ngày dùng ứng dụng'),('monthly_transactions','Số giao dịch/tháng')]
maxcoef=max(abs(x) for x in params['coefficients'])
for i,(key,label) in enumerate(inputs):
    idx=params['features'].index(key);coeff=params['coefficients'][idx]
    y=408-i*29
    text(42,y,label,8.2,'DejaVu',ink)
    block(225,y-2,205,9,HexColor('#E7EFF1'),r=4)
    fill=teal if coeff<0 else orange
    block(225,y-2,205*abs(coeff)/maxcoef,9,fill,r=4)
    text(443,y,f'{coeff:+.2f}',8,'DejaVu-Bold',fill)
text(42,278,'Hệ số chuẩn hóa: quan hệ của mô hình, không phải chứng cứ nhân quả.',8,'DejaVu',muted)

section(253,'04  SẢN PHẨM THỰC HÀNH & CÁCH DEMO')
y=230
for line_text in [
'• Dashboard HTML mở trực tiếp trên trình duyệt, không cần kết nối Internet.',
'• Thử 8 đầu vào bằng thanh trượt để xem xác suất dự đoán thay đổi.',
'• Tìm/lọc danh sách, xuất CSV và tham khảo 4 truy vấn T-SQL.',
'• Có mã nguồn Python, mô hình huấn luyện, bảng dữ liệu và README.']:
    text(44,y,line_text,8.6,'DejaVu',ink);y-=19

block(40,69,515,75,HexColor('#FFF8EA'),HexColor('#F7E3BC'),8)
text(53,123,'LƯU Ý KHI ỨNG TUYỂN',9,'DejaVu-Bold',HexColor('#7A5A25'))
y=textlines(53,105,'Đây là demo học tập tạo bằng công cụ AI hỗ trợ, sử dụng dữ liệu mô phỏng. Kết quả không thể suy rộng sang khách hàng thật hoặc ứng dụng để ra quyết định ngân hàng. Cần tự chạy, kiểm tra và hiểu dự án trước khi trình bày như kinh nghiệm cá nhân.',489,8.1,13,color=HexColor('#745B34'))
text(40,42,'Dữ liệu tổng hợp • Mã nguồn đầy đủ • Demo tương tác offline',8,'DejaVu',muted)
c.setStrokeColor(line);c.line(40,59,555,59)
c.showPage();c.save()
print(out,round(out.stat().st_size/1024,1),'KiB')
