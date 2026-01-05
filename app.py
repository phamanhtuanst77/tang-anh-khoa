import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. CẤU HÌNH API KEY (DÁN MÃ CỦA ANH VÀO ĐÂY)
# =========================================================
MY_API_KEY = "AIzaSyBoXoD5BIeeWf8-9fQ1CyDT5n3ZD-mln9k"

# =========================================================
# 2. DANH MỤC ÔN THI 7 MÔN
# =========================================================
MENU_ON_THI = {
    "Môn Toán": ["Rút gọn biểu thức", "Hệ thức Vi-ét", "Toán Chuyển động/Năng suất", "Hàm số & Đồ thị", "Tứ giác nội tiếp", "Hình học không gian", "Bất đẳng thức"],
    "Môn Ngữ Văn": ["Nghị luận xã hội", "Truyện lớp 9", "Thơ lớp 9", "Cách lập dàn ý", "Kỹ năng đọc hiểu", "Thành phần biệt lập"],
    "Môn Tiếng Anh": ["12 Thì tiếng Anh", "Câu bị động/Gián tiếp", "Câu điều kiện", "Mệnh đề quan hệ", "Trọng âm/Phát âm", "Kỹ năng Reading"],
    "Môn Vật Lý": ["Định luật Ôm", "Công suất điện", "Thấu kính", "Khúc xạ ánh sáng", "Máy biến thế"],
    "Môn Hóa Học": ["Acid/Base/Muối", "Chuỗi phản ứng vô cơ", "Bảng tuần hoàn", "Hữu cơ lớp 9", "Nồng độ dung dịch"],
    "Môn Lịch Sử": ["Thế giới sau 1945", "CMT8 & Kháng chiến", "Lịch sử VN từ 1975"],
    "Môn Địa Lý": ["Địa lý dân cư/Kinh tế", "7 vùng kinh tế", "Biển đảo", "Kỹ năng biểu đồ"]
}

# =========================================================
# 3. GIAO DIỆN APP
# =========================================================
st.set_page_config(page_title="Học Cùng Anh Khoa", page_icon="🛡️", layout="wide")

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

if "messages" not in st.session_state: st.session_state.messages = []
if "last_topic" not in st.session_state: st.session_state.last_topic = ""

with st.sidebar:
    st.title("📚 CHỌN MÔN HỌC")
    subject = st.radio("", list(MENU_ON_THI.keys()))
    st.markdown("---")
    st.markdown("### 🎯 CHUYÊN ĐỀ")
    selected_topic = st.selectbox("Kích chọn học nhanh:", ["Chọn nội dung..."] + MENU_ON_THI[subject])
    if st.button("Làm mới buổi học"):
        st.session_state.messages = []
        st.session_state.last_topic = ""
        st.rerun()

# =========================================================
# 4. THUẬT TOÁN KẾT NỐI AI "THÔNG MINH" (SỬA LỖI 404)
# =========================================================

if MY_API_KEY:
    try:
        genai.configure(api_key=MY_API_KEY)

        # HÀM TỰ DÒ TÌM MODEL (QUAN TRỌNG NHẤT)
        if "working_model" not in st.session_state:
            with st.spinner("Đang kết nối với máy chủ giáo dục..."):
                try:
                    # Liệt kê các model mà Key này được phép dùng
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    # Ưu tiên lấy flash 1.5, nếu không có lấy bất kỳ cái nào có chữ 'gemini'
                    found = next((m for m in available_models if "gemini-1.5-flash" in m), None)
                    if not found:
                        found = next((m for m in available_models if "gemini" in m), available_models[0])
                    st.session_state.working_model = found
                except:
                    st.session_state.working_model = "gemini-1.5-flash" # Dự phòng cuối cùng

        # Khởi tạo AI với model vừa tìm được
        model = genai.GenerativeModel(
            model_name=st.session_state.working_model,
            system_instruction=f"Bạn là gia sư chuyên sâu môn {subject} cho Anh Khoa. Luôn chào: 'Chào Anh Khoa, bố Tuấn đã chuẩn bị bài học này cho con...'. Trình bày bài giảng dễ hiểu, bám sát đề thi."
        )

        # Tự động xóa lịch sử khi đổi môn
        if "current_sub" not in st.session_state or st.session_state.current_sub != subject:
            st.session_state.messages = []
            st.session_state.current_sub = subject

        # Hiển thị lịch sử
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        # TỰ ĐỘNG HIỆN BÀI GIẢNG KHI KÍCH CHỌN
        if selected_topic != "Chọn nội dung..." and selected_topic != st.session_state.last_topic:
            st.session_state.last_topic = selected_topic
            user_msg = f"Dạy cho con chuyên sâu về chuyên đề: {selected_topic} trong môn {subject}"
            st.session_state.messages.append({"role": "user", "content": user_msg})
            
            with st.chat_message("user"): st.markdown(user_msg)
            with st.chat_message("assistant"):
                with st.spinner("Đang soạn bài..."):
                    response = model.generate_content(user_msg)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

        # Chat tự do
        if user_in := st.chat_input("Anh Khoa muốn hỏi thêm điều gì không?"):
            st.session_state.messages.append({"role": "user", "content": user_in})
            with st.chat_message("user"): st.markdown(user_in)
            with st.chat_message("assistant"):
                resp = model.generate_content(user_in)
                st.markdown(resp.text)
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
                if "đúng" in resp.text.lower(): st.balloons()

    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
        st.info("Bố Tuấn thử nhấn nút 'Làm mới buổi học' hoặc xóa App trên Streamlit để Deploy lại nhé.")
else:
    st.error("Chưa có API Key.")

st.markdown('<p style="text-align: center; color: gray; margin-top: 50px;">Try your best</p>', unsafe_allow_html=True)
