import os
import requests
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import re

load_dotenv()
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "gemma3")
mermaid_prompt = os.getenv('MERMAID_PROMPT')

# 환경 변수에서 Flask 서버 설정 값 읽기
host = os.getenv("FLASK_HOST", "0.0.0.0")  # 기본값은 "0.0.0.0"
port = int(os.getenv("FLASK_PORT", 5000))  # 기본값은 5000
debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"  # 기본값은 False

app = Flask(__name__)
CORS(app)  # CORS를 모든 경로에 대해 활성화

style_prompts = {
    "general": "다음 내용을 요약해 주세요.",
    "keywords": "다음 내용을 핵심 키워드 중심으로 요약해 주세요.",
    "pros_cons": "다음 내용을 장점과 단점으로 나눠서 정리해 주세요.",
    "table_summary": "다음 내용을 정리된 표 형태로 요약해 주세요.",
    "faq": "다음 내용을 FAQ 형식으로 재구성해 주세요.",
    "topic": "다음 내용을 주제별로 분류하여 요약해 주세요.",
    "brief_detail": "다음 내용을 요점 중심과 부연 설명으로 나눠서 정리해 주세요.",
    "bullet": "다음 내용을 핵심 항목별로 간결하게 정리해 주세요."
}
# LangChain 및 Ollama 설정
llm = ChatOllama(
    model=OLLAMA_MODEL_NAME,
    base_url=OLLAMA_API_URL
)

# 프롬프트 템플릿 정의
prompt_template = PromptTemplate(
    input_variables=["question"],
    template=mermaid_prompt
)

# 다이어그램 생성 체인 정의
diagram_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="mermaid_diagram")

def generate_mermaid_diagram(question):
    try:
        diagram_output = diagram_chain.invoke({"question": question})
        mermaid_code = diagram_output["mermaid_diagram"]
        print(mermaid_code)
        return {"success": True, "mermaid": mermaid_code}
    except Exception as e:
        return {"success": False, "error": str(e)}

# /webfonts 경로 추가
@app.route('/webfonts/<path:filename>')
def webfonts(filename):
    return send_from_directory('webfonts', filename)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        style = request.form["style"]
        lang = request.form["lang"]
        prompt = style_prompts.get(style, style_prompts["general"])
        if lang == "en":
            prompt = prompt.replace("다음 내용을", "Summarize the following content").replace("요약해 주세요", "")
        response = requests.post(
            f"{OLLAMA_API_URL}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": OLLAMA_MODEL_NAME,
                "messages": [
                    {"role": "system", "content": "당신은 요약 전문가입니다."},
                    {"role": "user", "content": f"{prompt}{text}"}
                ]
            }
        )
        summary = response.json()["choices"][0]["message"]["content"]
        return render_template("result.html", summary=summary, style=style)
    return render_template("result.html", summary=None)

@app.route("/diagram", methods=["GET", "POST"])
def diagram():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"success": False, "error": "'question' 값이 필요합니다."}), 400

    # Mermaid 코드 생성
    # print(question)
    mermaid_code = generate_mermaid_diagram(question)
    print(mermaid_code)
    if mermaid_code.get("success"):
        # Mermaid 코드를 ```mermaid로 바인딩하여 반환
        # "mermaid": f"```mermaid\n{mermaid_code['mermaid']}\n```"
        # "mermaid": f"{mermaid_code['mermaid']}"
        print(re.search(r'```(.*?)```', mermaid_code['mermaid'], re.DOTALL))
        match = re.search(r'```(.*?)```', mermaid_code['mermaid'], re.DOTALL)

        if match:
            # 추출된 결과를 문자열로 변환
            mermaid_code['mermaid'] = match.group(1)
            mermaid_code['mermaid'] = mermaid_code['mermaid'].replace('mermaid', '').replace('(', "'").replace(')', "'")

            print(mermaid_code['mermaid'])
        return jsonify({
            "success": True,
            "mermaid": mermaid_code['mermaid']
        })
    else:
        return jsonify({"success": False, "error": "❌ 다이어그램 생성에 실패했습니다."}), 500

# Flask 서버 실행
if __name__ == "__main__":
    app.run(
        host=host,
        port=port,
        debug=debug
    )
