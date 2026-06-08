# 🚀 나만의 자소서 도우미 (Resume Helper)

8주차 MCP 활용 서비스 개발 미니프로젝트 산출물입니다.
프롬프트 엔지니어링 기법과 에이전트 라우팅을 활용하여 자소서를 다각도로 분석하고 개선해 줍니다.

## 📂 주요 기능
- **CLI 대화형 인터페이스**: 터미널에서 명령어 기반으로 쉽게 동작
- **스타일 전환 (`/style`)**: Tech, Story, Impact 3가지 페르소나 전환 (PCT 구조 적용)
- **Agent 라우팅 (`/agent`)**: Triage 에이전트가 입력 문맥을 분석하여 적절한 전문가(Specialist)에게 전달
- **구조적 분석 (`/analyze`)**: Pydantic을 활용한 JSON 기반 문법/강점/약점 분석 기능
- **Guardrails 적용**: 프롬프트 인젝션 및 악의적 입력 사전 차단

## 💻 실행 방법

1. 의존성 설치 및 환경 준비 (uv 사용 권장)
   ```bash
   pip install python-dotenv pydantic