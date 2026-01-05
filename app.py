import streamlit as st
import google.generativeai as genai
import time

# =========================================================
# 1. CẤU HÌNH API KEY (DÁN MÃ GEMINI CỦA ANH VÀO ĐÂY)
# =========================================================
# Anh dán mã API Key lấy từ aistudio.google.com vào đây:
MY_API_KEY = "AIzaSyBoXoD5BIeeWf8-9fQ1CyDT5n3ZD-mln9k"

# =========================================================
# 2. DANH MỤC ÔN THI 7 MÔN CHI TIẾT
# =========================================================
MENU_ON_THI = {
    "Môn Toán": ["Rút gọn biểu thức", "Hệ thức Vi-ét", "Toán Chuyển động/Năng suất", "Hàm số & Đồ thị", "Tứ giác nội tiếp", "Hình học không gian", "Bất đẳng thức (Điểm 10)"],
    "Môn Ngữ Văn": ["Nghị luận xã hội", "Truyện lớp 9 trọng tâm", "Thơ lớp 9 trọng tâm", "Cách làm văn Nghị luận văn học", "Kỹ năng đọc hiểu văn bản", "Các thành phần biệt lập"],
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
        <h1>🌟 LỘ TRÌNH ÔN THI CHUYỂN CẤP TOÀN DIỆN</h1>
        <h2 style="color: #fdbb2d;">Bố Tuấn thiết kế riêng cho Anh Khoa</h2>
        <p>Con trai hãy vững tin, bố luôn đồng hành cùng con!</p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("📚 CHỌN MÔN HỌC")
    subject = st.radio("", list(MENU_ON_THI.keys()))
    st.markdown("---")
    st.markdown("### 🎯 CHUYÊN ĐỀ")
    selected_topic = st.selectbox("Kích chọn học nhanh:", ["Chọn nội dung..."] + MENU_ON_THI[subject])
    if st.button("Làm mới buổi học"):
        st.session_state.messages = []
        st.rerun()

# =========================================================
# 4. KẾT NỐI AI (PHIÊN BẢN ỔN ĐỊNH CAO)
# =========================================================

if MY_API_KEY.startswith("AIza"):
    try:
        genai.configure(api_key=MY_API_KEY)
        
        # Kỹ thuật: Sử dụng trực tiếp model name không qua v1beta để tránh 404
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=f"Bạn là siêu gia sư ôn thi môn {subject} cho Anh Khoa. Luôn chào: 'Chào Anh Khoa, bố Tuấn đã chuẩn bị bài học này cho con...'. Trình bày dễ hiểu, bám sát SGK lớp 9."
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "current_sub" not in st.session_state or st.session_state.current_sub != subject:
            st.session_state.messages = []
            st.session_state.current_sub = subject

        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        # Xử lý khi chọn từ mục lục
        if selected_topic != "Chọn nội dung...":
            user_msg = f"Dạy cho con chuyên sâu về chuyên đề: {selected_topic}"
            if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_msg:
                st.session_state.messages.append({"role": "user", "content": user_msg})
                with st.spinner("Đang soạn bài giảng..."):
                    try:
                        response = model.generate_content(user_msg)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                        st.rerun()
                    except Exception as e:
                        if "429" in str(e):
                            st.warning("Hệ thống đang tải, Anh Khoa đợi thầy 10 giây nhé...")
                            time.sleep(10)
                            st.rerun()

        # Chat tự do
        if user_in := st.chat_input("Anh Khoa muốn hỏi thêm điều gì không?"):
            st.session_state.messages.append({"role": "user", "content": user_in})
            with st.chat_message("user"): st.markdown(user_in)
            with st.chat_message("assistant"):
                response = model.generate_content(user_in)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                if "đúng" in response.text.lower(): st.balloons()

    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
else:
    st.error("Bố Tuấn chưa dán API Key Gemini hợp lệ.")

st.markdown('<p style="text-align: center; color: gray; margin-top: 50px;">Try your best! - Mr Bin</p>', unsafe_allow_html=True)


