import os
from dotenv import load_dotenv
from styles import PROMPT_STYLES
from resume_agents import Runner, AnalysisResult

load_dotenv()

def check_guardrails(user_input: str) -> bool:
    """[기본 기능: Guardrails 연결] 악의적 프롬프트 사전 차단"""
    forbidden_words = ["명령 무시", "해킹", "시스템 프롬프트", "forget everything"]
    for word in forbidden_words:
        if word.lower() in user_input.lower():
            return False
    return True

def mock_llm_response(messages: list) -> str:
    """API 키 없이도 동작을 확인하기 위한 Mock 함수 (실제 API 연동 시 교체)"""
    return f"LLM 응답 처리 완료 (현재 스타일: {messages[0]['role']} 설정됨)"

def mock_analyze(user_input: str) -> str:
    """[PE 기법: Structured Output] Pydantic 모델을 JSON으로 반환하는 시뮬레이션"""
    mock_data = AnalysisResult(
        grammar_errors=["'바램입니다' -> '바람입니다'"],
        strengths=["구체적인 기술 스택 명시"],
        weaknesses=["문제 해결 과정의 구체성 부족"],
        overall_score=85
    )
    return mock_data.model_dump_json(indent=2)

def main():
    print("="*50)
    print("🚀 나만의 자소서 도우미 (Resume Helper) 🚀")
    print("="*50)
    print("명령어: /style [이름], /analyze, /agent, /help, /quit")
    print("기본 자소서를 입력하지 않고 바로 명령어를 테스트해보세요.")
    
    current_style = "tech"
    # 테스트를 위한 개인화된 이력서 기본 샘플
    default_resume_context = """
    프로젝트명: 7Hours (반려견 산책 앱)
    사용 기술: Android, Kotlin, Jetpack Compose, Django, PostgreSQL
    내용: UI/UX 설계 및 서버 연동을 구현했습니다. 특히 일반적인 BottomSheet 대신 
    하단에서 위로 당겨서 여는(Pull-up) 커스텀 Action Bar 인터페이스를 직접 구현하여 사용자 편의성을 높였습니다.
    """
    
    agent_runner = Runner()

    while True:
        try: 
            user_input = input("\n[You] (자소서 내용 또는 명령어) > ").strip()
            
            if not user_input:
                continue
                
            if user_input == "/quit":
                print("자소서 도우미를 종료합니다. 좋은 결과 있으시길 바랍니다!")
                break
                
            elif user_input == "/help":
                print("\n[도움말]")
                print("/style tech|story|impact : 평가 스타일 변경")
                print("/analyze : 현재 입력된 샘플 자소서 구조적 결함 탐지 (JSON 출력)")
                print("/agent : Agent 라우팅 테스트")
                continue
                
            elif user_input.startswith("/style"):
                parts = user_input.split()
                if len(parts) > 1 and parts[1] in PROMPT_STYLES:
                    current_style = parts[1]
                    print(f"\n✅ 스타일이 '{current_style}'(으)로 변경되었습니다.")
                    print(f"설명: {PROMPT_STYLES[current_style]['description']}")
                else:
                    print(f"사용 가능한 스타일: {list(PROMPT_STYLES.keys())}")
                continue
                
            elif user_input == "/analyze":
                print("\n[구조적 분석 결과 (Structured Output)]")
                print(mock_analyze(default_resume_context))
                continue
                
            elif user_input == "/agent":
                print("\n[Agent System 테스트]")
                result = agent_runner.run(default_resume_context)
                print(result)
                continue

            if not check_guardrails(user_input):
                print("🚨 [Guardrail 경고] 부적절한 지시나 보안 위협이 감지되어 요청이 거부되었습니다.")
                continue
            
            messages = [
                {"role": PROMPT_STYLES[current_style]["role"], "content": PROMPT_STYLES[current_style]["content"]},
                {"role": "user", "content": user_input}
            ]
            
            print(f"\n[AI Helper ({current_style} 모드)]")
            print(mock_llm_response(messages))
            print("(입력하신 내용을 바탕으로 리뷰가 생성되었습니다.)")

        except KeyboardInterrupt:
            print("\n프로그램을 강제 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()