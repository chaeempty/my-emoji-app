import streamlit as st
from openai import OpenAI
from rembg import remove
from PIL import Image
import io
import requests

# 1. API 키 설정 (보안을 위해 실제 서비스 시에는 st.secrets를 사용하세요)
client = OpenAI(api_key="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")

st.set_page_config(page_title="PPT Emoji Maker", layout="wide")

st.title("🎨 PPT 전용 커스텀 이모지 생성기")
st.write("광고 제안서의 톤앤매너에 딱 맞는 아이콘을 생성하고 배경 없이 다운로드하세요.")

# --- 사이드바: 스타일 설정 ---
with st.sidebar:
    st.header("⚙️ 스타일 설정")
    
    style_option = st.radio(
        "원하는 이모지 스타일을 선택하세요:",
        [
            "2D 볼드 라인 (Bold & Flat)",
            "3D 장난감 (Soft & Cute)",
            "미니멀 플랫 (Simple Vector)",
            "블랙 라인 아트 (Minimal Line)"
        ]
    )

    # 스타일별 프롬프트 정의
    style_prompts = {
        "2D 볼드 라인 (Bold & Flat)": "2D bold line illustration style icon. Thick black outlines, filled with solid color blocks (orange, yellow, white, red). formalized and flat graphic shape. No shadows, no gradients, no texture. Clean white background.",
        "3D 장난감 (Soft & Cute)": "3D toy-like character modeling style icon. Soft and voluminous forms, clay or soft plastic finish. Warm and friendly color palette. Pixar-style cuteness. Soft lighting, subtle gradients. Clean white background.",
        "미니멀 플랫 (Simple Vector)": "Very simple and minimalist flat vector icon. Clean geometric shapes, flat color blocks (bright primary and pastel tones) without lines. Minimal detail. No gradients, no shadows, no texture, no 3D effects. Clean white background.",
        "블랙 라인 아트 (Minimal Line)": "Very simple and minimalist black line art icon. Thin and uniform black lines. No color fill, no gradients, no shadows. Vector style clean outlines. Flat design. Clean white background."
    }

# --- 메인 영역: 입력 및 생성 ---
col1, col2 = st.columns([1, 1])

with col1:
    user_input = st.text_input("어떤 아이콘을 만들까요?", placeholder="예: 텀블러, 로켓, 강아지, 전구 등")
    generate_btn = st.button("아이콘 생성하기", use_container_width=True)

if generate_btn:
    if not user_input:
        st.warning("만들고 싶은 아이콘 키워드를 입력해 주세요.")
    else:
        with st.spinner("AI가 아이콘을 그리는 중입니다... (약 10~20초 소요)"):
            try:
                # DALL-E 3 호출
                full_prompt = f"{user_input}. {style_prompts[style_option]}"
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=full_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                # 이미지 URL 가져오기
                image_url = response.data[0].url
                raw_image = Image.open(requests.get(image_url, stream=True).raw)

                with col2:
                    st.subheader("✅ 완성된 아이콘")
                    
                    # 배경 제거 처리
                    with st.spinner("배경을 투명하게 만드는 중..."):
                        transparent_image = remove(raw_image)
                    
                    # 결과 표시
                    st.image(transparent_image, use_container_width=True)

                    # 다운로드 버튼
                    buf = io.BytesIO()
                    transparent_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="배경 없는 PNG 다운로드",
                        data=byte_im,
                        file_name=f"{user_input}_icon.png",
                        mime="image/png",
                        use_container_width=True
                    )
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# --- 안내 문구 ---
st.divider()
st.info("💡 Tip: 영어로 입력하면 더 정확한 결과가 나올 수 있습니다. (예: Coffee cup 대신 'Coffee cup with steam')")
