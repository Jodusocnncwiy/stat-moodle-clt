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
    # 理論值：Mean=5.0, SD=1.5
    pop_data = np.random.normal(loc=5.0, scale=1.5, size=10000)
    gen_sample = lambda size: np.random.normal(loc=5.0, scale=1.5, size=size)

elif distribution == "均勻分配 (Uniform)":
    # 理論值：Mean=5.0, SD=2.89 (10/sqrt(12))
    pop_data = np.random.uniform(0, 10, 10000)
    gen_sample = lambda size: np.random.uniform(0, 10, size)

elif distribution == "指數分配 (Exponential)":
    # 理論值：Mean=2.0, SD=2.0
    pop_data = np.random.exponential(scale=2.0, size=10000)
    gen_sample = lambda size: np.random.exponential(scale=2.0, size=size)

else: # 雙峰分配
    pop1 = np.random.normal(2, 0.8, 5000)
    pop2 = np.random.normal(8, 0.8, 5000)
    pop_data = np.concatenate([pop1, pop2])
    def gen_sample(size):
        p = np.random.binomial(size, 0.5)
        return np.concatenate([np.random.normal(2, 0.8, p), np.random.normal(8, 0.8, size-p)])

# 計算母體的實際平均數與標準差
pop_mean = np.mean(pop_data)
pop_sd = np.std(pop_data)

# 計算多次模擬的抽樣平均數
sample_means = [np.mean(gen_sample(n)) for _ in range(num_simulations)]

# 計算抽樣分配的實際平均數與標準差
sm_mean = np.mean(sample_means)
sm_sd = np.std(sample_means)
# 理論上的標準誤 (Standard Error) = 母體標準差 / sqrt(n)
theoretical_se = pop_sd / np.sqrt(n)

# 3. 畫面佈局：左邊放母體，右邊放抽樣分配
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌐 母體分配 (Population Distribution)")
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(x=pop_data, nbinsx=50, marker_color='#34495e', opacity=0.75, histnorm='probability density'))
    fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=320, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    
    # 呈現母體的統計量描述
    st.markdown(f"""
    <div style="background-color: rgba(27, 54, 93, 0.05); padding: 15px; border-radius: 8px; border-left: 5px solid #1B365D;">
        <h4 style="color: #1B365D; margin-top: 0; margin-bottom: 8px;">📊 母體參數實際值</h4>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">母體平均數 (μ)：<b>{pop_mean:.3f}</b></p>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">母體標準差 (σ)：<b>{pop_sd:.3f}</b></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("🎯 樣本平均數的抽樣分配")
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=sample_means, nbinsx=50, marker_color='#2980b9', opacity=0.75, histnorm='probability density'))
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=320, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    
    # 呈現抽樣分配的實際值與理論值對比
    st.markdown(f"""
    <div style="background-color: rgba(27, 54, 93, 0.05); padding: 15px; border-radius: 8px; border-left: 5px solid #1B365D;">
        <h4 style="color: #1B365D; margin-top: 0; margin-bottom: 8px;">📈 抽樣分配統計量</h4>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">樣本平均數的平均數：<b>{sm_mean:.3f}</b> （理論上應接近 μ = {pop_mean:.3f}）</p>
        <p style="margin: 4px 0; font-size: 15px; color: #333333;">樣本平均數的標準差 (標準誤)：<b>{sm_sd:.3f}</b> （理論上應為 σ/√n = {theoretical_se:.3f}）</p>
    </div>
    """, unsafe_allow_html=True)

# 4. 動態引導文字與教學提示
st.markdown("---")
if n < 30:
    if distribution == "常態分配 (Normal)":
        st.success(f"✨ **教學觀念**：當前 n = {n}。注意看下方數據！因為母體本身就是**常態分配**，抽樣分配的平均數（**{sm_mean:.3f}**）與標準差（**{sm_sd:.3f}**）不僅完美符合理論，且分佈形狀依然保持完美的常態。")
    else:
        st.warning(f"⚠️ **教學觀念**：當前 n = {n} (< 30)。注意看右圖，因為樣本數不足，抽樣分配的形狀可能仍有些不對稱；但請觀察下方的數據，樣本平均數的平均數（**{sm_mean:.3f}**）已經非常接近母體平均數（**{pop_mean:.3f}**）了！")
else:
    st.success(f"✨ **教學觀念**：當前 n = {n} (≥ 30，已達大樣本門檻！)。此時無論母體原先多偏斜，抽樣分配均已收斂為常態分配。請比對下方數據，您會發現抽樣標準差（**{sm_sd:.3f}**）精準縮小到接近理論值 **{theoretical_se:.3f}**！")
