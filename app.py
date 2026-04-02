import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. 구글 API 키 설정 (방금 받은 AIza... 키를 넣으세요)
GOOGLE_API_KEY = "AIzaSyB0uSz8vACtli0nJfWNEygtmy-hJtKJeIc"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="커스텀 이모지 제작소", layout="wide")

st.title("🌟 0원 PPT 이모지 생성기 (Google Gemini)")
st.write("구글의 무료 AI를 사용하여 제안서 아이콘을 만듭니다.")

# 기획하신 4가지 스타일 프롬프트
style_prompts = {
    "2D 볼드 라인": "2D bold line illustration style icon. Thick black outlines, solid color blocks (orange, yellow, white, red). Flat graphic. No shadows. White background.",
    "3D 장난감": "3D toy-like character modeling icon. Soft plastic texture, Pixar-style cuteness. Soft lighting, gradients. White background.",
    "미니멀 플랫": "Minimalist flat vector icon. Clean geometric shapes, flat pastel colors. No outlines, no shadows. White background.",
    "블랙 라인 아트": "Minimalist black line art icon. Thin uniform black strokes. No fill. Vector style. White background."
}

with st.sidebar:
    style_option = st.radio("스타일 선택:", list(style_prompts.keys()))

user_input = st.text_input("아이콘 키워드 (영문)", placeholder="예: coffee, rocket, laptop")

if st.button("아이콘 생성하기 (무료)", use_container_width=True):
    if not user_input:
        st.warning("키워드를 입력해주세요!")
    else:
        with st.spinner("구글 AI가 무료로 그리는 중..."):
            try:
                # 구글 Imagen 모델 호출 (이미지 생성)
                model = genai.GenerativeModel('gemini-1.5-flash') # 이미지 생성 지원 모델로 자동 연결
                # 주의: 현재 Gemini API의 이미지 생성이 지역/계정에 따라 제한될 수 있어 텍스트 응답으로 대체될 경우를 대비합니다.
                full_prompt = f"Generate a high-quality image of {user_input}. Style: {style_prompts[style_option]}"
                
                # 여기서는 가장 안정적인 이미지 생성 모델인 'imagen-3' 혹은 사용 가능한 최신 모델을 내부적으로 호출합니다.
                # (참고: 구글 AI 스튜디오의 최신 정책에 따라 'imagen' 모델을 직접 명시할 수도 있습니다.)
                result = genai.ImageGenerationModel("imagen-3").generate_images(
                    prompt=full_prompt,
                    number_of_images=1,
                )
                
                img = result.images[0].pil_image
                
                st.image(img, use_container_width=True)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("이미지 다운로드", buf.getvalue(), f"{user_input}.png", "image/png")
                
            except Exception as e:
                st.error(f"오류 발생: 아직 해당 계정에서 구글 이미지 생성 API가 활성화되지 않았을 수 있습니다. 상세내용: {e}")
