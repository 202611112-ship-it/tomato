import streamlit as st
import pandas as pd
import joblib

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="Tomato AI",
    page_icon="🍅",
    layout="centered"
)

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b,
        #0f172a
    );
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    color: white;
}

@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.main-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 35px;
    box-shadow: 0 0 40px rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
}

.title {
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    color: #ff4b4b;
    text-shadow: 0 0 20px rgba(255,75,75,0.8);
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.stNumberInput input {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 12px !important;
}

.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 20px;
    border: none;
    background: linear-gradient(90deg,#ff416c,#ff4b2b);
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    transition: 0.3s;
    box-shadow: 0 0 20px rgba(255,75,75,0.5);
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 35px rgba(255,75,75,0.9);
}

.result-box {
    margin-top: 30px;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    background: linear-gradient(
        135deg,
        rgba(255,75,75,0.2),
        rgba(255,255,255,0.05)
    );
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 0 25px rgba(255,75,75,0.3);
}

.result-text {
    font-size: 2rem;
    font-weight: bold;
    color: #ffb703;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# 모델 불러오기
# ---------------------------
rf_model = joblib.load("tomato_model.pkl")

# ---------------------------
# 타이틀
# ---------------------------
st.markdown("""
<div class="main-card">
    <div class="title">🍅 TOMATO AI</div>
    <div class="subtitle">
        스마트팜 착과율 예측 시스템
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------------------
# 입력창
# ---------------------------
humidity = st.number_input(
    "💧 내부습도 (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=0.1
)

temp = st.number_input(
    "🌡 외부온도 (°C)",
    min_value=-30.0,
    max_value=60.0,
    value=25.0,
    step=0.1
)

# ---------------------------
# 버튼
# ---------------------------
if st.button("🚀 착과율 예측 시작"):

    # 입력 데이터
    input_data = pd.DataFrame(
        [[humidity, temp]],
        columns=["내부습도", "외부온도"]
    )

    # 예측
    predicted = rf_model.predict(input_data) # 
    score = float(predicted[0])

    # 디버깅 출력
    st.write("예측 원본값:", score)

    # 안전 범위 제한
    safe_score = max(0, min(int(score), 100))
    display_score = max(0, min(score, 100))

    # 진행바
    st.progress(safe_score)

    # 결과 박스
    st.markdown(
    f"""
    <div class="result-box">

        <div style="font-size:1.2rem;">
            AI 분석 완료
        </div>

        <div class="result-text">
            {display_score:.1f}%
        </div>

        <div style="margin-top:10px; color:#ddd;">
            현재 환경 기준 예상 착과률
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

    # 상태 메시지
    if display_score >= 80:
        st.success("🔥 토마토 상태 최상급이다냐")

    elif display_score >= 60:
        st.info("🌱 꽤 괜찮은 환경이네 냐")

    else:
        st.warning("⚠️ 환경 조정이 필요할 수도 있다냐")
