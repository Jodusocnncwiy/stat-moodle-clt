import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 設定網頁為寬螢幕佈局
st.set_page_config(layout="wide", page_title="中心極限定理互動視覺化")

st.title("📊 中心極限定理 (Central Limit Theorem) 互動探索")
st.markdown("管理系學生的統計直覺：當樣本數 $n$ 夠大時，不論母體的分配為何，**樣本平均數的抽樣分配**都會趨近於**常態分配**。請調整左側參數親自驗證！")

# 1. 建立左側側邊欄控制項
st.sidebar.header("🛠️ 實驗參數設定")
distribution = st.sidebar.selectbox(
    "1. 選擇母體分配類型",
    [
        "常態分配 (Normal)", 
        "均勻分配 (Uniform)", 
        "指數分配 (Exponential)", 
        "雙峰分配 (Bimodal)"
    ]
)

n = st.sidebar.slider("2. 每次抽樣的樣本數 (n)", min_value=2, max_value=100, value=5)
num_simulations = st.sidebar.slider("3. 重複抽樣次數 (模擬次數)", min_value=100, max_value=5000, value=1000, step=100)

# 2. 生成母體數據與抽樣邏輯
np.random.seed(42)

if distribution == "常態分配 (Normal)":
    pop_data = np.random.normal(loc=5.0, scale=1.5, size=10000)
    gen_sample = lambda size: np.random.normal(loc=5.0, scale=1.5, size=size)

elif distribution == "均勻分配 (Uniform)":
    pop_data = np.random.uniform(0, 10, 10000)
    gen_sample = lambda size: np.random.uniform(0, 10, size)

elif distribution == "指數分配 (Exponential)":
    pop_data = np.random.exponential(scale=2.0, size=10000)
    gen_sample = lambda size: np.random.exponential(scale=2.0, size=size)

else: # 雙峰分配
    pop1 = np.random.normal(2, 0.8, 5000)
    pop2 = np.random.normal(8, 0.8, 5000)
    pop_data = np.concatenate([pop1, pop2])
    def gen_sample(size):
        p = np.random.binomial(size, 0.5)
        return np.concatenate([np.random.normal(2, 0.8, p), np.random.normal(8, 0.8, size-p)])

# 計算多次模擬的抽樣平均數
sample_means = [np.mean(gen_sample(n)) for _ in range(num_simulations)]

# 3. 畫面佈局：左邊放母體，右邊放抽樣分配
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌐 母體分配 (Population Distribution)")
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(x=pop_data, nbinsx=50, marker_color='#34495e', opacity=0.75, histnorm='probability density'))
    fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    st.info(f"這是原始母體的樣貌。目前設定為：{distribution}")

with col2:
    st.subheader("🎯 樣本平均數的抽樣分配")
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=sample_means, nbinsx=50, marker_color='#2980b9', opacity=0.75, histnorm='probability density'))
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    
    # 動態引導文字（以台灣統計學教學標準：n >= 30 為大樣本門檻）
    if n < 30:
        if distribution == "常態分配 (Normal)":
            st.success(f"✨ 當前 n = {n}。注意！因為母體本身就是**常態分配**，根據統計理論，不論樣本數多小，抽樣分配都會完美呈現**鐘形常態分配**！")
        else:
            st.warning(f"⚠️ 當前 n = {n} (< 30，尚未達到統計學大樣本門檻)。注意看右圖，它依然保有一些母體分配的影子（例如不對稱或雙峰），尚未完全變成鐘形曲線。")
    else:
        st.success(f"✨ 當前 n = {n} (≥ 30，已達大樣本門檻！)。觀察右圖！即使原始母體極度不對稱或呈雙峰，抽樣分配此時都已經完美呈現對稱的**鐘形常態分配**！")
