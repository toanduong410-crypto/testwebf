import streamlit as st
import json
import os
from datetime import datetime

# 1. Cấu hình giao diện chuẩn giống Facebook
st.set_page_config(page_title="Facebook", page_icon="📘", layout="centered")

# Nhúng CSS tùy chỉnh để đổi giao diện thành màu xanh Facebook và bo góc các bài viết
st.markdown("""
    <style>
    .stApp { background-color: #000000; } 
    .fb-header { 
        background-color: #ffffff; 
        color: #000000; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        font-weight: bold; 
        margin-bottom: 20px; 
        border: 2px solid #ffffff;
    }
    .fb-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 0 4px 10px rgba(255,255,255,0.1); 
        margin-bottom: 15px; 
        color: #000000;
    }
    .fb-author { font-weight: bold; color: #000000; font-size: 16px; }
    .fb-time { color: #555555; font-size: 13px; }
    .fb-content { color: #000000; font-size: 15px; margin-top: 10px; margin-bottom: 10px; }
    h3, label, .stMarkdown p { color: #ffffff !important; }
    .fb-card h3, .fb-card label, .fb-card p, .fb-card span, .fb-card div { color: #000000 !important; }
    </style>
    
    <div class="fb-header"><h1>NAH</h1></div>
""", unsafe_allow_html=True)

# 2. Hàm xử lý dữ liệu (Đọc/Ghi file JSON)
def load_posts():
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            try: return json.load(f)
            except json.JSONDecodeError: return []
    return []

def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

# Khởi tạo hoặc lấy dữ liệu bài viết
if 'all_posts' not in st.session_state:
    st.session_state.all_posts = load_posts()

# 3. Khung đăng bài viết (Giống ô "Bạn đang nghĩ gì?" của FB)
with st.container():
    st.markdown('<div class="fb-card">', unsafe_allow_html=True) # Đã sửa ở đây
    st.subheader("Tạo bài viết mới")
    user = st.text_input("Tên tài khoản:", placeholder="Nhập tên của bạn...")
    text = st.text_area("Nội dung:", placeholder="Bạn đang nghĩ gì thế?")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        btn_submit = st.button("Đăng", use_container_width=True)
        
    if btn_submit:
        if user.strip() and text.strip():
            new_post = {
                "id": len(st.session_state.all_posts) + 1,
                "name": user,
                "content": text,
                "time": datetime.now().strftime("%d Tháng %m lúc %H:%M"),
                "likes": 0
            }
            st.session_state.all_posts.insert(0, new_post)
            save_posts(st.session_state.all_posts)
            st.rerun()
        else:
            st.error("Vui lòng điền tên và nội dung!")
    st.markdown('</div>', unsafe_allow_html=True) # Đã sửa ở đây

st.write("### Bảng tin")

# 4. Hiển thị danh sách bài viết theo phong cách các thẻ (Cards) của Facebook
for idx, post in enumerate(st.session_state.all_posts):
    # Tạo cấu trúc HTML cho từng bài viết
    post_html = f"""
    <div class="fb-card">
        <span class="fb-author">👤 {post['name']}</span><br>
        <span class="fb-time">🕒 {post['time']}</span>
        <div class="fb-content">{post['content']}</div>
    </div>
    """
    st.markdown(post_html, unsafe_allow_html=True) # Đã sửa ở đây
    
    # Nút bấm tương tác Thích (Like) đặt ngay dưới bài viết
    col_like, col_space = st.columns([1, 4])
    with col_like:
        if st.button(f"👍 Thích ({post['likes']})", key=f"like_{post['id']}_{idx}"):
            post['likes'] += 1
            save_posts(st.session_state.all_posts)
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True) # Đã sửa ở đây
