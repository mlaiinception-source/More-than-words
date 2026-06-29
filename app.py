import streamlit as st
import random
import json

# 設定 Streamlit 頁面優化（適用於手機與網頁端）
st.set_page_config(
    page_title="深刻地認識一個人 - 互動抽卡遊戲",
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 自訂 CSS 提升介面美觀度與手機閱讀體驗
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .card-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 6px solid #4F46E5;
        margin-bottom: 25px;
        text-align: center;
    }
    .card-title {
        color: #1E1B4B;
        font-size: 24px;
        font-weight: 700;
        line-height: 1.5;
        margin-bottom: 10px;
    }
    .card-star {
        color: #4F46E5;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .guide-box {
        background-color: #F8FAFC;
        padding: 15px 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-top: 15px;
    }
    .guide-title {
        font-weight: bold;
        color: #334155;
        font-size: 15px;
        margin-bottom: 5px;
    }
    .guide-content {
        color: #64748B;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 1. INGEST (資料接入層)
# ==========================================
def load_raw_questions():
    """
    接入遊戲原始題庫。
    設計上預留 'star_level' 欄位供未來擴充（包含：破冰、一星、二星、三星）。
    此處幫忙補齊 30 道精心設計的深層連結互動題目。
    """
    questions_dataset = [
        # 【破冰等級】
        {"id": 1, "text": "如果你可以擁有一種超能力，你最希望是什麼？", "star_level": "破冰"},
        {"id": 2, "text": "你最近聽過最喜歡的一首歌是什麼？它為什麼吸引你？", "star_level": "破冰"},
        {"id": 3, "text": "如果餘生只能吃一種食物，你會選擇什麼？", "star_level": "破冰"},
        {"id": 4, "text": "手機裡你最常用的三個 App 是什麼？", "star_level": "破冰"},
        {"id": 5, "text": "你最喜歡的一個旅行目的地是哪裡？發生過什麼有趣的事？", "star_level": "破冰"},
        {"id": 6, "text": "想像你開了一家店，你會想賣什麼產品或服務？", "star_level": "破冰"},
        {"id": 7, "text": "如果你可以穿越到過去或未來，你想去哪一個年份？", "star_level": "破冰"},
        
        # 【一星等級：個人故事與偏好】
        {"id": 8, "text": "你最深刻的一個童年回憶是什麼？", "star_level": "一星"},
        {"id": 9, "text": "在你的朋友眼中，你通常扮演什麼樣的角色？", "star_level": "一星"},
        {"id": 10, "text": "目前為止，你覺得自己做過最勇敢的決定是什麼？", "star_level": "一星"},
        {"id": 11, "text": "你最欣賞身邊哪一位朋友的特質？為什麼？", "star_level": "一星"},
        {"id": 12, "text": "如果中了頭獎，你第一件想做的事情是什麼？", "star_level": "一星"},
        {"id": 13, "text": "生活中，什麼事情最容易讓你感到放鬆或被治癒？", "star_level": "一星"},
        {"id": 14, "text": "你有沒有什麼不為人知的小癖好或怪癖？", "star_level": "一星"},
        
        # 【二星等級：價值觀與信念】
        {"id": 15, "text": "對你而言，一段理想的友誼或伴侶關係最核心的要素是什麼？", "star_level": "二星"},
        {"id": 16, "text": "什麼樣的事情會讓你真正感到生氣或踩到你的底線？", "star_level": "二星"},
        {"id": 17, "text": "如果可以改變自己過去的一個選擇，你會想改變什麼？", "star_level": "二星"},
        {"id": 18, "text": "當你心情低落時，你通常會如何陪伴自己或排解情緒？", "star_level": "二星"},
        {"id": 19, "text": "到目前為止，對你人生觀影響最深的一本書、電影或一句話是什麼？", "star_level": "二星"},
        {"id": 20, "text": "你覺得自己身上最顯著的優點和缺點分別是什麼？", "star_level": "二星"},
        {"id": 21, "text": "你相信命運是注定的，還是完全由自己掌控？", "star_level": "二星"},
        
        # 【三星等級：深層脆弱與靈魂對話】
        {"id": 22, "text": "你目前人生中最大的焦慮或恐懼是什麼？", "star_level": "三星"},
        {"id": 23, "text": "你曾經歷過最痛苦的一次挫折是什麼？你是怎麼走過來的？", "star_level": "三星"},
        {"id": 24, "text": "如果生命只剩下最後一個月，你最想和誰一起度過？做些什麼？", "star_level": "三星"},
        {"id": 25, "text": "你希望自己在十年後成為一個什麼樣的人？", "star_level": "三星"},
        {"id": 26, "text": "有沒有哪一個秘密或遺憾，是你一直放在心底很少對人提起的？", "star_level": "三星"},
        {"id": 27, "text": "當你離開這個世界時，你希望人們怎麼記得你？", "star_level": "三星"},
        {"id": 28, "text": "你覺得自己目前最缺乏的安全感來自於哪裡？", "star_level": "三星"},
        {"id": 29, "text": "如果可以用你現有的某個珍貴東西換取絕對的快樂，你願意嗎？", "star_level": "三星"},
        {"id": 30, "text": "在你心中，「愛」最真實的模樣應該長成什麼樣子？", "star_level": "三星"}
    ]
    return questions_dataset


# ==========================================
# 2. TRANSFORM (資料轉換與邏輯層)
# ==========================================
def init_game_state(force_reset=False):
    """
    利用 Streamlit 的 st.session_state 進行狀態管理。
    確保同一局內已抽過的題目不重複出現，直到題庫完全抽完。
    """
    # 載入原始資料
    raw_questions = load_raw_questions()
    
    # 建立或重置狀態
    if "pool" not in st.session_state or force_reset:
        st.session_state.pool = raw_questions.copy()
        st.session_state.drawn_history = []
        st.session_state.current_card = None
        st.session_state.selected_stars = ["破冰", "一星", "二星", "三星"] # 預設全選

def filter_and_draw_card():
    """
    動態篩選與隨機抽卡演算法邏輯。
    """
    # 根據 Serve 層的篩選條件過濾剩餘題庫
    available_pool = [q for q in st.session_state.pool if q["star_level"] in st.session_state.selected_stars]
    
    if not available_pool:
        st.session_state.current_card = "EMPTY"
    else:
        # 隨機抽取一張卡片
        chosen_card = random.choice(available_pool)
        # 更新狀態：從總題庫中移除，並加入已抽過歷史記錄
        st.session_state.pool.remove(chosen_card)
        st.session_state.drawn_history.append(chosen_card)
        st.session_state.current_card = chosen_card


# ==========================================
# 3. SERVE (展示與互動層)
# ==========================================
def run_app():
    # 初始化資料與邏輯狀態
    init_game_state()
    
    # --- 側邊欄 (Sidebar) 說明與設定 ---
    with st.sidebar:
        st.title("🧩 遊戲前置與規則")
        
        st.subheader("💡 開場白引導")
        st.info(
            "「接下來我們要玩一個輕鬆但能深刻認識彼此的抽卡遊戲。 "
            "每一張卡片都是一個走入內心世界的邀請，沒有標準答案， "
            "只有最真實的分享。準備好了嗎？」"
        )
        
        st.subheader("📜 遊戲流程")
        st.markdown(
            "1. **輪流抽卡**：輪到的玩家點擊主畫面的按鈕抽卡。
"
            "2. **真誠分享**：大聲唸出題目並回答，其餘玩家保持專注與傾聽。
"
            "3. **深度互動**：回答完後，其他人可進行追問或給予讚美。"
        )
        
        st.subheader("⚙️ 題庫篩選 (擴充功能)")
        # 動態連動核心數據狀態
        st.session_state.selected_stars = st.multiselect(
            "選擇允許抽取的卡牌星級：",
            options=["破冰", "一星", "二星", "三星"],
            default=st.session_state.selected_stars
        )
        
        st.markdown("---")
        # 重新洗牌按鈕
        if st.button("🔄 重新洗牌 / 重置遊戲", use_container_width=True):
            init_game_state(force_reset=True)
            st.rerun()

    # --- 主畫面 (Main Screen) 呈現 ---
    st.title("🃏 深刻地認識一個人")
    st.caption("這是一場關於聆聽、共鳴與深層連結的靈魂對話遊戲。")
    
    # 顯示當前進度與計數器
    total_initial = len(load_raw_questions())
    remaining_count = len([q for q in st.session_state.pool if q["star_level"] in st.session_state.selected_stars])
    drawn_count = len(st.session_state.drawn_history)
    
    # 頂部進度條與數據展示
    col1, col2 = st.columns(2)
    with col1:
        st.metric("符合條件的剩餘卡片", f"{remaining_count} 張")
    with col2:
        st.metric("本局已抽卡片", f"{drawn_count} 張")
        
    st.progress(drawn_count / total_initial if total_initial > 0 else 0)
    st.write("")

    # 核心抽卡觸發按鈕
    if st.button("🔮 抽一張卡 (Draw a Card)", type="primary", use_container_width=True):
        filter_and_draw_card()

    # 渲染抽出的卡牌內容
    if st.session_state.current_card:
        if st.session_state.current_card == "EMPTY":
            st.warning("⚠️ 當前選取的星級題庫已全數抽完，或您未勾選任何星級！請在側邊欄調整或點擊重新洗牌。")
        else:
            card = st.session_state.current_card
            
            # 使用自訂 CSS 樣式渲染卡牌大字體
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-star">✦ {card['star_level']} ✦</div>
                    <div class="card-title">「 {card['text']} 」</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 互動輔助提示區
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
        # 初始未抽卡狀態
        st.info("👆 請點擊上方「抽一張卡」按鈕開始遊戲！引導詞與規則已為您放在左側邊欄。")

if __name__ == "__main__":
    run_app()
