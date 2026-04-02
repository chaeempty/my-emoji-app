import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import requests

# 1. API 키 설정 (본인의 sk-로 시작하는 키를 넣으세요)
client = OpenAI(api_key="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") 

st.set_page_config(page_title="PPT Emoji Maker", layout="wide")

# 사이트 제목 및 설명
st.title("🎨 PPT 커스텀 이모지 생성기")
st.write("광고 제안서 톤앤매너에 맞는 아이콘을 생성하세요. (배경 제거 제외 버전)")

# 스타일 설정 (기획하신 4가지 스타일)
style_prompts = {
    "2D 볼드 라인": "2D bold line illustration style icon. Thick black outlines, filled with solid color blocks (orange, yellow, white, red). flat graphic shape. No shadows, no gradients. Clean white background.",
    "3D 장난감": "3D toy-like character modeling style icon. Soft plastic texture, Pixar-style cuteness. Soft lighting, subtle gradients. Clean white background.",
    "미니멀 플랫": "Minimalist flat vector icon. Clean geometric shapes, flat color blocks. No gradients, no shadows. Clean white background.",
    "블랙 라인 아트": "Minimalist black line art icon. Thin uniform black lines. No color fill, no shadows. Clean white background."
}

# UI 구성
with st.sidebar:
    st.header("⚙️ 스타일 선택")
    style_option = st.radio("원하는 스타일을 고르세요:", list(style_prompts.keys()))

user_input = st.text_input("어떤 아이콘을 만들까요? (영문 입력 추천)", placeholder="예: rocket, laptop, coffee cup")

if st.button("아이콘 생성하기", use_container_width=True):
    if not user_input:
        st.warning("키워드를 입력해주세요!")
    else:
        with st.spinner("AI가 이모지를 그리는 중입니다... (약 15초 소요)"):
            try:
                # 이미지 생성 요청
                full_prompt = f"{user_input}. {style_prompts[style_option]}"
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=full_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                # 이미지 URL에서 이미지 불러오기
                image_url = response.data[0].url
                image_data = requests.get(image_url).content
                img = Image.open(io.BytesIO(image_data))
                
                # 결과 표시
                st.image(img, caption=f"생성된 아이콘: {user_input}", use_container_width=True)
                
                # 다운로드 버튼
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button(
                    label="이미지 다운로드 (PNG)",
                    data=buf.getvalue(),
                    file_name=f"{user_input}_icon.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

st.divider()
st.caption("Tip: 배경 제거가 필요하면 생성된 이미지를 다운로드 후 [remove.bg] 사이트를 이용해 보세요!")
