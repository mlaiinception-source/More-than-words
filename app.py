import streamlit as st
import random
import os

# 設定 Streamlit 頁面優化（適用於手機與網頁端）
st.set_page_config(
    page_title="深刻地認識一個人 - 互動抽卡遊戲 from Clark Chen",
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 自訂 CSS 提升介面美觀度與手機閱讀體驗 (質感升級版)
st.markdown("""
    <style>
    /* 引入 Google 字體：思源宋體 (適合展示深刻的文字) */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&display=swap');

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 卡牌主體設計：加入漸層、圓角與懸浮動畫 */
    .card-box {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 40px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border-top: 6px solid #4F46E5;
        margin-top: 20px;
        margin-bottom: 30px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* 滑鼠游標移過去時，卡牌會微微浮起的動畫 (手機版則不影響) */
    .card-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(79, 70, 229, 0.15);
    }
    
    /* 卡牌題目字體：使用優雅的宋體 */
    .card-title {
        font-family: 'Noto Serif TC', serif;
        color: #1E1B4B;
        font-size: 26px;
        font-weight: 700;
        line-height: 1.6;
        margin-top: 15px;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }
    
    /* 星級標籤：變成類似膠囊形狀的 Tag */
    .card-star {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4F46E5;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    
    /* 輔助說明的框框：改成更柔和的磨砂玻璃感 */
    .guide-box {
        background-color: rgba(248, 250, 252, 0.7);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-top: 10px;
    }
    .guide-title {
        font-weight: 800;
        color: #334155;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .guide-content {
        color: #64748B;
        font-size: 13px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 1. INGEST (資料接入層)
# ==========================================

def load_raw_questions():
    """
    從 questions.txt 讀取題庫，並根據標題自動賦予星級分類。
    """
    questions_dataset = []
    current_level = "破冰" # 預設星級

    # 檢查檔案是否存在
    if not os.path.exists("questions.txt"):
        return [{"id": 1, "text": "找不到 questions.txt 檔案，請確認是否已上傳至 GitHub。", "star_level": "系統提示"}]

    # 讀取文字檔並解析
    with open("questions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    q_id = 1
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 判斷是否為分類標題，若為標題則切換當前星級
        if "暖身破冰卡" in line:
            current_level = "破冰"
        elif "一星連結卡" in line:
            current_level = "一星"
        elif "二星連結卡" in line:
            current_level = "二星"
        elif "三星連結卡" in line:
            current_level = "三星"
        else:
            # 如果不是標題，就是題目內容，寫入資料集
            questions_dataset.append({
                "id": q_id,
                "text": line,
                "star_level": current_level
            })
            q_id += 1
            
    return questions_dataset


# ==========================================
# 2. TRANSFORM (資料轉換與邏輯層)
# ==========================================
def init_game_state(force_reset=False):
    raw_questions = load_raw_questions()
    
    if "pool" not in st.session_state or force_reset:
        st.session_state.pool = raw_questions.copy()
        st.session_state.drawn_history = []
        st.session_state.current_card = None
        st.session_state.selected_stars = ["破冰", "一星", "二星", "三星"]

def filter_and_draw_card():
    available_pool = [q for q in st.session_state.pool if q["star_level"] in st.session_state.selected_stars]
    
    if not available_pool:
        st.session_state.current_card = "EMPTY"
    else:
        chosen_card = random.choice(available_pool)
        st.session_state.pool.remove(chosen_card)
        st.session_state.drawn_history.append(chosen_card)
        st.session_state.current_card = chosen_card


# ==========================================
# 3. SERVE (展示與互動層)
# ==========================================
def run_app():
    init_game_state()
    
    with st.sidebar:
        st.title("🧩 遊戲前置與規則")
        
        st.subheader("💡 開場白引導")
        st.info(
            "「接下來我們要玩一個輕鬆但能深刻認識彼此的抽卡遊戲。 "
            "每一張卡片都是一個走入內心世界的邀請，沒有標準答案， "
            "只有最真實的分享。準備好了嗎？」"
        )
        
        st.subheader("📜 遊戲流程")
        st.markdown("""
        1. **輪流抽卡**：輪到的玩家點擊主畫面的按鈕抽卡。
        2. **真誠分享**：大聲唸出題目並回答，其餘玩家保持專注與傾聽。
        3. **深度互動**：回答完後，其他人可進行追問或給予讚美。
        """)
        
        st.subheader("⚙️ 題庫篩選")
        st.session_state.selected_stars = st.multiselect(
            "選擇允許抽取的卡牌星級：",
            options=["破冰", "一星", "二星", "三星"],
            default=st.session_state.selected_stars
        )
        
        st.markdown("---")
        if st.button("🔄 重新洗牌 / 重置遊戲", use_container_width=True):
            init_game_state(force_reset=True)
            st.rerun()

    st.title("🃏 深刻地認識一個人")
    st.caption("這是一場關於聆聽、共鳴與深層連結的靈魂對話遊戲。")
    
    # 計算進度
    total_initial = len(load_raw_questions())
    remaining_count = len([q for q in st.session_state.pool if q["star_level"] in st.session_state.selected_stars])
    drawn_count = len(st.session_state.drawn_history)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("符合條件的剩餘卡片", f"{remaining_count} 張")
    with col2:
        st.metric("本局已抽卡片", f"{drawn_count} 張")
        
    st.progress(drawn_count / total_initial if total_initial > 0 else 0)
    st.write("")

    if st.button("🔮 抽一張卡 (Draw a Card)", type="primary", use_container_width=True):
        filter_and_draw_card()

    if st.session_state.current_card:
        if st.session_state.current_card == "EMPTY":
            st.warning("⚠️ 當前選取的星級題庫已全數抽完，或您未勾選任何星級！請在側邊欄調整或點擊重新洗牌。")
        else:
            card = st.session_state.current_card
            
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-star">✦ {card['star_level']} ✦</div>
                    <div class="card-title">「 {card['text']} 」</div>
                </div>
            """, unsafe_allow_html=True)
            
            c_guide1, c_guide2 = st.columns(2)
            with c_guide1:
                st.markdown("""
                    <div class="guide-box">
                        <div class="guide-title">↩️ 回答輔助彈性</div>
                        <div class="guide-content">
                            • <b>換一張</b>：若太沉重可享一次PASS機會。<br>
                            • <b>請人代答</b>：指名現場一位朋友先幫忙打樣。
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with c_guide2:
                st.markdown("""
                    <div class="guide-box">
                        <div class="guide-title">💬 聆聽者互動建議</div>
                        <div class="guide-content">
                            • <b>溫暖讚美</b>：感謝對方的真誠與脆弱。<br>
                            • <b>好奇追問</b>：針對故事細節延伸靈魂對話。
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👆 請點擊上方「抽一張卡」按鈕開始遊戲！引導詞與規則已為您放在左側邊欄。")

if __name__ == "__main__":
    run_app()
