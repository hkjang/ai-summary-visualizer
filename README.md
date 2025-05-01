# Mermaid Diagram Generator + Summary Tool (Flask + LangChain + Ollama)

이 프로젝트는 **Flask** 기반의 웹 애플리케이션으로, 사용자가 입력한 내용을 요약하거나 Mermaid 다이어그램 코드로 변환하는 기능을 제공합니다.  
**LangChain**과 **Ollama** API를 사용하여 자연어 처리를 수행합니다.

---

## 🛠️ 주요 기능

| 기능 | 설명 |
|------|------|
| 요약 생성 | 입력 텍스트에 대해 다양한 스타일로 요약 제공 |
| 다이어그램 생성 | 입력된 설명을 기반으로 Mermaid 다이어그램 생성 |
| 다국어 지원 | 한국어/영어 요약 가능 |
| LangChain 연동 | LLMChain 기반 프롬프트 처리 |
| Ollama 연동 | 로컬 또는 서버 기반 Ollama 모델 API 활용 |

---

## 📁 프로젝트 구조

| 파일/디렉토리 | 설명 |
|---------------|------|
| `Dockerfile` | Python 3.12-slim 기반의 도커 설정 |
| `requirements.txt` | 필요한 Python 패키지 목록 |
| `app.py` | Flask 웹서버 및 LangChain 연동 메인 로직 |
| `templates/result.html` | 결과 렌더링을 위한 HTML 템플릿 |
| `.env` | 환경 변수 설정 파일 (`OLLAMA_API_URL`, `OLLAMA_MODEL_NAME` 등) |

---

## 🧪 실행 방법

### 1. 환경 변수 설정

`.env` 파일을 생성하고 다음 항목을 채워주세요:

```
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3
MERMAID_PROMPT=당신은 전문가입니다. 다음 설명을 Mermaid 다이어그램 형식으로 변환하세요:
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
```

### 2. Docker로 실행

```bash
docker build -t mermaid-summary-app .
docker run -p 5000:5000 --env-file .env mermaid-summary-app
```

### 3. 로컬 실행 (Python 직접 실행)

```bash
pip install -r requirements.txt
python app.py
```

---

## 🧠 사용 예시

### 요약 요청 (POST `/`)

```bash
text=국내 총생산이 증가함에 따라...
style=keywords
lang=ko
```

### Mermaid 생성 요청 (POST `/diagram`)

```json
{
  "question": "AI 시스템의 구성 요소를 설명해줘"
}
```

---

## 🧱 Mermaid 다이어그램 정제 방식

- 백틱(```)으로 감싸진 코드 블럭에서 `mermaid` 키워드를 추출
- `()`는 사용하지 않고 `'`으로 대체 처리
- LangChain에서 프롬프트 템플릿 처리 후 결과값을 정규표현식으로 추출

---

## 📦 Dockerfile 요약

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EXPOSE 5000
```

---

## 📜 의존성 목록 (`requirements.txt`)

```txt
flask
flask-cors
python-dotenv
requests
langchain
langchain-community
langchain-core
langchain-ollama
```

---

## ✅ 참고

- Ollama: https://ollama.com
- Mermaid: https://mermaid.js.org
- LangChain: https://www.langchain.com