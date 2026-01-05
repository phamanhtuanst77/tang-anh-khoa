import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. CẤU HÌNH API KEY (Duy nhất 1 chỗ này)
# =========================================================
# Anh Tuấn dán mã API Key vào giữa hai dấu ngoặc kép dưới đây:
MY_API_KEY = "AIzaSyCTiPWA0c9UECJ8gTtps-g9N8eciGUaVyg"

# =========================================================
# 2. DANH MỤC ÔN THI CHI TIẾT 7 MÔN (Bám sát SGK & Đề thi)
# =========================================================
MENU_ON_THI = {
    "Môn Toán": [
        "Rút gọn biểu thức và bài toán liên quan",
        "Giải hệ phương trình bậc nhất 2 ẩn",
        "Phương trình bậc hai & Hệ thức Vi-ét",
        "Toán Chuyển động / Năng suất / Hình học",
        "Hàm số y = ax^2 và đường thẳng y = ax + b",
        "Tứ giác nội tiếp và Hình học đường tròn",
        "Hình trụ - Hình nón - Hình cầu",
        "Bài toán bất đẳng thức & Cực trị (Câu lấy điểm 10)"
    ],
    "Môn Ngữ Văn": [
        "Nghị luận xã hội (Tư tưởng đạo lý / Hiện tượng đời sống)",
        "Truyện: Làng - Lặng lẽ Sa Pa - Chiếc lược ngà",
        "Thơ: Đồng chí - Bài thơ về tiểu đội xe không kính",
        "Thơ: Đoàn thuyền đánh cá - Bếp lửa - Sang thu",
        "Thơ: Viếng lăng Bác - Nói với con",
        "Văn bản nhật dụng & Kỹ năng đọc hiểu",
        "Cách lập dàn ý và viết mở bài/kết bài ấn tượng",
        "Các thành phần biệt lập & Liên kết câu"
    ],
    "Môn Tiếng Anh": [
        "Hệ thống 12 Thì (Tenses) trọng tâm",
        "Câu bị động (Passive Voice) & Câu gián tiếp",
        "Câu điều kiện (Type 1, 2) & Câu ước (Wish)",
        "Mệnh đề quan hệ (Relative Clauses)",
        "Cấu trúc so sánh & Cụm động từ (Phrasal Verbs)",
        "Trọng âm & Phát âm (Phonetics)",
        "Kỹ năng làm bài Đọc hiểu & Điền từ",
        "Viết lại câu sao cho nghĩa không đổi"
    ],
    "Môn Vật Lý": [
        "Điện trở - Định luật Ôm - Đoạn mạch nối tiếp/song song",
        "Công suất điện - Điện năng tiêu thụ (Định luật Joule-Lenser)",
        "Hiện tượng cảm ứng điện từ - Máy biến thế",
        "Hiện tượng khúc xạ ánh sáng",
        "Thấu kính hội tụ & Thấu kính phân kỳ",
        "Sự tạo ảnh trong Mắt - Máy ảnh - Kính lúp",
        "Định luật bảo toàn và chuyển hóa năng lượng"
    ],
    "Môn Hóa Học": [
        "Oxide - Acid - Base - Muối (Tính chất & Phản ứng)",
        "Mối quan hệ giữa các hợp chất vô cơ",
        "Kim loại (Al, Fe) & Phi kim (Cl, C, Si)",
        "Bảng tuần hoàn các nguyên tố hóa học",
        "Hydrocarbon: Methane, Ethylene, Acetylene, Benzene",
        "Dẫn xuất Hydrocarbon: Rượu Ethyl, Axit Axetic",
        "Chất béo - Protein - Polyme",
        "Bài toán tính theo phương trình & nồng độ dung dịch"
    ],
    "Môn Lịch Sử": [
        "Lịch sử thế giới sau 1945 (Liên Xô, Mỹ, Nhật, Á-Phi-Mỹ Latinh)",
        "Các cuộc cách mạng khoa học - kỹ thuật",
        "Lịch sử VN 1919 - 1930 (Đảng ra đời)",
        "Cuộc vận động tiến tới CMT8 năm 1945",
        "Kháng chiến chống Pháp (1946 - 1954)",
        "Kháng chiến chống Mỹ (1954 - 1975)",
        "Lịch sử VN từ 1975 đến nay"
    ],
    "Môn Địa Lý": [
        "Địa lý dân cư & Các loại hình quần cư VN",
        "Các ngành kinh tế (Nông nghiệp, Công nghiệp, Dịch vụ)",
        "Vùng Trung du và miền núi Bắc Bộ",
        "Vùng Đồng bằng sông Hồng & Bắc Trung Bộ",
        "Vùng Duyên hải Nam Trung Bộ & Tây Nguyên",
        "Vùng Đông Nam Bộ & Đồng bằng sông Cửu Long",
        "Phát triển kinh tế biển & Đảo",
        "Kỹ năng vẽ và phân tích biểu đồ Địa lý"
    ]
}

# =========================================================
# 3. GIAO DIỆN APP (UI)
# =========================================================
st.set_page_config(page_title="Quà Tặng Anh Khoa", page_icon="🛡️", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #f4f7f6; }}
    .main-header {{ 
        background-color: #1a2a6c; padding: 30px; border-radius: 20px; 
        color: white; text-align: center; margin-bottom: 30px;
    }}
    </style>
    <div class="main-header">
        <h1>🌟 LỘ TRÌNH ÔN THI CHUYỂN CẤP TOÀN DIỆN</h1>
        <h2 style="color: #fdbb2d;">Bố Tuấn thiết kế riêng cho Anh Khoa</h2>
        <p>Con tr

