import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm, expon

# 設定網頁為寬螢幕佈局
st.set_page_config(layout="wide", page_title="中心極限定理互動視覺化")

# 🟢 【精準調整：只縮減右側主畫面頂部留白，左側 Jodus 學習品牌位置保持完美不變】
st.markdown(
    """
    <style>
        /* 縮減右側主內容區的最頂端留白，不影響左側側邊欄 */
        [data-testid="stMain"] .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0rem !important;
        }
        /* 讓主畫面的大標題更貼近頂端 */
        [data-testid="stMain"] h1 {
            margin-top: -10px !important;
            margin-bottom: 10px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 1. 建立左側側邊欄（「🎓 Jodus學習」位置完美保留在最左上角）
st.sidebar.markdown(
    """
    <div style="padding-bottom: 10px; border-bottom: 2px solid #1B365D; margin-bottom: 20px;">
        <h1 style="color: #1B365D; font-size: 28px; margin: 0; font-weight: bold;">🎓 Jodus學習</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

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

# 2. 標題與主畫面說明
st.title("📊 中心極限定理 (Central Limit Theorem) 互動探索")
st.markdown("當樣本數 $n$ 夠大時，不論母體的分配為何，**樣本平均數的抽樣分配**都會趨近於**常態分配**。請調整左側參數親自驗證！")

# 3. 定義各分配的理論值與生成模擬抽樣
np.random.seed(42)

# 用於繪製平滑母體理論圖的 X 軸範圍
x_eval = np.linspace(-5, 15, 1000)

if distribution == "常態分配 (Normal)":
    theoretical_pop_mean = 5.0
    theoretical_pop_sd = 2.0
    y_eval = norm.pdf(x_eval, loc=5.0, scale=2.0)
    gen_sample = lambda size: np.random.normal(loc=5.0, scale=2.0, size=size)

elif distribution == "均勻分配 (Uniform)":
    theoretical_pop_mean = 5.0
    theoretical_pop_sd = 10.0 / np.sqrt(12)
    x_eval = np.array([-1.0, 0.0, 0.0, 10.0, 10.0, 11.0])
    y_eval = np.array([0.0, 0.0, 0.1, 0.1, 0.0, 0.0])
    gen_sample = lambda size: np.random.uniform(0, 10, size)

elif distribution == "指數分配 (Exponential)":
    theoretical_pop_mean = 2.0
    theoretical_pop_sd = 2.0
    x_eval = np.linspace(-1.0, 12.0, 1000)
    y_eval = np.where(x_eval >= 0, expon.pdf(x_eval, scale=2.0), 0.0)
    gen_sample = lambda size: np.random.exponential(scale=2.0, size=size)

else: # 雙峰分配
    theoretical_pop_mean = 5.0
    theoretical_pop_sd = np.sqrt(9.64)
    y_eval = 0.5 * norm.pdf(x_eval, loc=2.0, scale=0.8) + 0.5 * norm.pdf(x_eval, loc=8.0, scale=0.8)
    def gen_sample(size):
        p = np.random.binomial(size, 0.5)
        return np.concatenate([np.random.normal(2, 0.8, p), np.random.normal(8, 0.8, size-p)])

# 4. 模擬抽樣分配（重複進行 num_simulations 次）
sample_means = [np.mean(gen_sample(n)) for _ in range(num_simulations)]

# 計算模擬抽樣分配的統計量
simulated_sm_mean = np.mean(sample_means)
simulated_sm_sd = np.std(sample_means)

# 理論上的標準誤 (Standard Error) = 理論母體標準差 / sqrt(n)
theoretical_se = theoretical_pop_sd / np.sqrt(n)

# 5. 畫面佈局：左邊放母體，右邊放抽樣分配
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌐 母體分配 (Population Distribution)")
    fig1 = go.Figure()
    
    # 完美繪製母體理論機率密度函數 (PDF)
    fig1.add_trace(go.Scatter(
        x=x_eval, y=y_eval, 
        mode='lines', 
        line=dict(color='#34495e', width=3),
        fill='tozeroy',
        fillcolor='rgba(52, 73, 94, 0.25)',
        name='理論母體 PDF'
    ))
    
    fig1.update_layout(
        margin=dict(l=20, r=20, t=10, b=10), 
        height=300, 
        showlegend=False,
        xaxis_title="值 (Value)",
        yaxis_title="機率密度 (Density)"
    )
    # 動態鎖定 x 軸顯示區間
    if distribution == "均勻分配 (Uniform)":
        fig1.update_xaxes(range=[-1, 11])
    elif distribution == "指數分配 (Exponential)":
        fig1.update_xaxes(range=[-1, 10])
    else:
        fig1.update_xaxes(range=[-2, 12])
        
    st.plotly_chart(fig1, use_container_width=True)
    
    # 呈現純淨的理論母體參數
    st.markdown(f"""
    <div style="background-color: rgba(27, 54, 93, 0.05); padding: 15px; border-radius: 8px; border-left: 5px solid #1B365D;">
        <h4 style="color: #1B365D; margin-top: 0; margin-bottom: 8px;">📊 理論母體參數值</h4>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">母體理論平均數 (&mu;)：<b style="font-size: 18px; color: #1B365D;">{theoretical_pop_mean:.3f}</b></p>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">母體理論標準差 (&sigma;)：<b>{theoretical_pop_sd:.3f}</b></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("🎯 樣本平均數的抽樣分配")
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=sample_means, nbinsx=50, marker_color='#2980b9', opacity=0.75, histnorm='probability density'))
    fig2.update_layout(
        margin=dict(l=20, r=20, t=10, b=10), 
        height=300, 
        showlegend=False,
        xaxis_title="樣本平均數 (Sample Mean)",
        yaxis_title="機率密度 (Density)"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # 呈現模擬抽樣的統計量
    st.markdown(f"""
    <div style="background-color: rgba(27, 54, 93, 0.05); padding: 15px; border-radius: 8px; border-left: 5px solid #1B365D;">
        <h4 style="color: #1B365D; margin-top: 0; margin-bottom: 8px;">📈 抽樣分配模擬統計量</h4>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">樣本平均數的平均數 (x̄)：<b>{simulated_sm_mean:.3f}</b> （理論值 &mu;<sub>X̄</sub> 應接近：{theoretical_pop_mean:.3f}）</p>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">樣本平均數的模擬標準差：<b>{simulated_sm_sd:.3f}</b> （理論值 &sigma;<sub>X̄</sub> 應為 &sigma;/&radic;n = {theoretical_se:.3f}）</p>
    </div>
    """, unsafe_allow_html=True)

# 6. 動態引導文字與教學提示
st.markdown("---")
if n < 30:
    if distribution == "常態分配 (Normal)":
        st.success(f"✨ **教學觀念**：當前 n = {n}。注意看下方數據！因為母體本身就是**常態分配**，抽樣分配的平均數（**{simulated_sm_mean:.3f}**）與標準差（**{simulated_sm_sd:.3f}**）不僅完美符合理論，且分佈形狀依然保持完美的常態。")
    else:
        st.warning(f"⚠️ **教學觀念**：當前 n = {n} (< 30)。注意看右圖，因為樣本數不足，抽樣分配的形狀可能仍有些不對稱；但請觀察下方的數據，樣本平均數的平均數（**{simulated_sm_mean:.3f}**）已經非常接近母體理論平均數 **{int(theoretical_pop_mean)}** 了！")
else:
    st.success(f"✨ **教學觀念**：當前 n = {n} (≥ 30，已達大樣本門檻！)。此時無論母體原先多偏斜，抽樣分配均已收斂為常態分配。請比對下方數據，您會發現抽樣標準差（**{simulated_sm_sd:.3f}**）精準縮小到接近理論值 **{theoretical_se:.3f}**！")
