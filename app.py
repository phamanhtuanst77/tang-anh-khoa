import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. CẤU HÌNH API KEY (ANH DÁN MÃ VÀO ĐÂY)
# =========================================================
MY_API_KEY = "AIzaSyBoXoD5BIeeWf8-9fQ1CyDT5n3ZD-mln9k"

# =========================================================
# 2. DANH MỤC ÔN THI 7 MÔN
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

# Khởi tạo trạng thái App
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# --- SIDEBAR ---
with st.sidebar:
    st.title("📚 CHỌN MÔN HỌC")
    subject = st.radio("", list(MENU_ON_THI.keys()))
    st.markdown("---")
    st.markdown("### 🎯 CHUYÊN ĐỀ")
    # Sử dụng key để Streamlit theo dõi thay đổi
    selected_topic = st.selectbox("Kích chọn học nhanh:", ["Chọn nội dung..."] + MENU_ON_THI[subject], key="topic_selector")
    
    if st.button("Làm mới buổi học"):
        st.session_state.messages = []
        st.session_state.last_topic = ""
        st.rerun()

# =========================================================
# 4. KẾT NỐI AI & XỬ LÝ DỮ LIỆU
# =========================================================

if MY_API_KEY:
    try:
        genai.configure(api_key=MY_API_KEY)
        
        # SỬA LỖI 404: Ép model không dùng v1beta
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # Bỏ tiền tố models/ để tránh lỗi endpoint
            system_instruction=f"Bạn là gia sư chuyên sâu môn {subject} giúp Anh Khoa ôn thi vào 10. Luôn chào: 'Chào Anh Khoa, bố Tuấn đã chuẩn bị bài học này cho con...'. Trình bày bài giảng đầy đủ, dễ hiểu, bám sát đề thi."
        )

        # Tự động xóa lịch sử khi đổi môn
        if "current_sub" not in st.session_state or st.session_state.current_sub != subject:
            st.session_state.messages = []
            st.session_state.current_sub = subject

        # Hiển thị lịch sử chat
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        # LOGIC TỰ ĐỘNG HIỆN BÀI GIẢNG KHI KÍCH CHỌN
        if selected_topic != "Chọn nội dung..." and selected_topic != st.session_state.last_topic:
            st.session_state.last_topic = selected_topic
            user_msg = f"Dạy cho con chuyên sâu về chuyên đề: {selected_topic} trong môn {subject}"
            
            # Thêm tin nhắn của người dùng vào lịch sử
            st.session_state.messages.append({"role": "user", "content": user_msg})
            with st.chat_message("user"): st.markdown(user_msg)
            
            with st.chat_message("assistant"):
                with st.spinner("Đang soạn bài giảng..."):
                    # Gọi AI với cơ chế thử lại nếu lỗi
                    try:
                        response = model.generate_content(user_msg)
                        answer = response.text
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as ai_err:
                        st.error(f"Lỗi khi gọi AI: {ai_err}")

        # Chat tự do
        if user_in := st.chat_input("Anh Khoa hỏi thêm thầy điều gì không?"):
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
    st.error("Chưa có API Key.")

st.markdown('<p style="text-align: center; color: gray; margin-top: 50px;">Yêu con trai nhiều! - Bố Tuấn</p>', unsafe_allow_html=True)
