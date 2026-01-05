import streamlit as st
from openai import OpenAI

# =========================================================
# 1. CẤU HÌNH API KEY GROK (XAI)
# =========================================================
# Anh dán mã Grok (xai-...) vào giữa hai dấu ngoặc kép này:
GROK_API_KEY = "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"

# =========================================================
# 2. DANH MỤC ÔN THI 7 MÔN (DÀNH CHO ANH KHOA)
# =========================================================
MENU_ON_THI = {
    "Môn Toán": ["Rút gọn biểu thức", "Hệ thức Vi-ét", "Toán Chuyển động/Năng suất", "Hàm số & Đồ thị", "Tứ giác nội tiếp", "Hình học không gian", "Bất đẳng thức (Điểm 10)"],
    "Môn Ngữ Văn": ["Nghị luận xã hội", "Truyện lớp 9 trọng tâm", "Thơ lớp 9 trọng tâm", "Cách lập dàn ý văn học", "Kỹ năng đọc hiểu văn bản", "Các thành phần biệt lập"],
    "Môn Tiếng Anh": ["12 Thì tiếng Anh", "Câu bị động & Gián tiếp", "Câu điều kiện & Wish", "Mệnh đề quan hệ", "Trọng âm & Phát âm", "Kỹ năng Reading & Writing"],
    "Môn Vật Lý": ["Định luật Ôm & Điện trở", "Công suất & Điện năng", "Thấu kính hội tụ/phân kỳ", "Khúc xạ ánh sáng", "Máy biến thế & Truyền tải điện"],
    "Môn Hóa Học": ["Tính chất Acid/Base/Muối", "Chuỗi phản ứng vô cơ", "Bảng tuần hoàn", "Hydrocarbon (Methane, Etilen...)", "Rượu & Axit hữu cơ", "Tính toán nồng độ dung dịch"],
    "Môn Lịch Sử": ["Lịch sử thế giới sau 1945", "Cách mạng 8 & Kháng chiến Pháp/Mỹ", "Lịch sử VN từ 1975", "Sơ đồ mốc thời gian quan trọng"],
    "Môn Địa Lý": ["Địa lý dân cư & Kinh tế VN", "7 vùng kinh tế trọng điểm", "Địa lý biển đảo", "Kỹ năng vẽ/đọc biểu đồ"]
}

# =========================================================
# 3. GIAO DIỆN APP
# =========================================================
st.set_page_config(page_title="Quà Tặng Anh Khoa", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-header { 
        background-color: #1a2a6c; padding: 30px; border-radius: 20px; 
        color: white; text-align: center; margin-bottom: 30px;
    }
    </style>
    <div class="main-header">
        <h1>🚀 HỆ THỐNG ÔN THI VÀO 10 TOÀN DIỆN</h1>
        <h2 style="color: #fdbb2d;">Bố Tuấn thiết kế riêng cho Anh Khoa</h2>
        <p>Con trai hãy vững tin, bố luôn đồng hành cùng con!</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar chọn môn
with st.sidebar:
    st.title("📚 CHỌN MÔN HỌC")
    subject = st.radio("", list(MENU_ON_THI.keys()))
    st.markdown("---")
    st.markdown("### 🎯 CHUYÊN ĐỀ")
    selected_topic = st.selectbox("Kích chọn học ngay:", ["Chọn nội dung..."] + MENU_ON_THI[subject])
    if st.button("Làm mới buổi học"):
        st.session_state.messages = []
        st.rerun()

# =========================================================
# 4. KẾT NỐI GROK AI
# =========================================================

if GROK_API_KEY.startswith("xai-"):
    client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Reset khi đổi môn
    if "current_sub" not in st.session_state or st.session_state.current_sub != subject:
        st.session_state.messages = []
        st.session_state.current_sub = subject

    # Hiển thị lịch sử
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    # Xử lý chọn từ mục lục
    if selected_topic != "Chọn nội dung...":
        prompt = f"Chào em, thầy là Grok. Bố Tuấn nhờ thầy dạy cho Anh Khoa chuyên sâu về {subject}, chuyên đề: {selected_topic}. Hãy giảng bài dễ hiểu, bám sát SGK và đề thi vào 10."
        if not st.session_state.messages or st.session_state.messages[-1]["content"] != prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Grok đang soạn bài giảng cho Anh Khoa..."):
                response = client.chat.completions.create(
                    model="grok-beta", # Hoặc "grok-2" tùy gói của anh
                    messages=[{"role": "system", "content": f"Bạn là gia sư ôn thi vào 10 cho Anh Khoa môn {subject}. Luôn bắt đầu bằng: 'Chào Anh Khoa, bố Tuấn đã chuẩn bị bài học này cho con...'"},
                              {"role": "user", "content": prompt}]
                )
                answer = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

    # Chat tự do
    if user_in := st.chat_input("Anh Khoa hỏi Grok thêm điều gì không?"):
        st.session_state.messages.append({"role": "user", "content": user_in})
        with st.chat_message("user"): st.markdown(user_in)
        with st.chat_message("assistant"):
            with st.spinner("Grok đang suy nghĩ..."):
                response = client.chat.completions.create(
                    model="grok-beta",
                    messages=[{"role": "system", "content": f"Bạn là gia sư ôn thi vào 10 cho Anh Khoa môn {subject}."},
                              *st.session_state.messages]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                if "đúng" in answer.lower(): st.balloons()
else:
    st.error("Bố Tuấn ơi, anh chưa dán mã API Key của Grok (xai-...) vào dòng số 10 rồi!")

st.markdown('<p style="text-align: center; color: gray; margin-top: 50px;">Yêu con trai nhiều! - Bố Tuấn</p>', unsafe_allow_html=True)
