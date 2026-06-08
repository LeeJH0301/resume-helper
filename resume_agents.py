import json
from pydantic import BaseModel, Field
from openai import OpenAI


class AnalysisResult(BaseModel):
    grammar_errors: list[str] = Field(description="발견된 맞춤법 및 문법 오류 리스트")
    strengths: list[str] = Field(description="자소서 초안의 강점")
    weaknesses: list[str] = Field(description="자소서 초안의 약점 및 보완점")
    overall_score: int = Field(description="100점 만점 기준의 총점")

class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

class TriageAgent(Agent):
    def __init__(self):
        instructions = """
        당신은 자소서 입력값을 분석하여 가장 적합한 전문가(Specialist)에게 전달하는 라우터입니다.
        - 사용자가 '기술, 코드, 알고리즘, 트러블슈팅'을 강조하면 'TechSpecialist'로 라우팅하세요.
        - 사용자가 '협업, 갈등, 팀워크, 성장'을 강조하면 'StorySpecialist'로 라우팅하세요.
        - 그 외의 경우 또는 판단이 어려울 경우 'GeneralSpecialist'로 라우팅하세요.
        응답은 반드시 라우팅할 에이전트 이름만 출력하세요. (예: TechSpecialist)
        """
        super().__init__("TriageAgent", instructions)

class TechSpecialistAgent(Agent):
    def __init__(self):
        instructions = "기술적 뎁스와 아키텍처, 트러블슈팅 관점에서 자소서를 날카롭게 분석하는 기술 전문가입니다."
        super().__init__("TechSpecialistAgent", instructions)

class StorySpecialistAgent(Agent):
    def __init__(self):
        instructions = "협업 경험과 소프트 스킬, 인성 측면을 부각시키는 스토리텔링 전문가입니다."
        super().__init__("StorySpecialistAgent", instructions)

class Runner:
    def __init__(self):
        self.triage = TriageAgent()
        self.specialists = {
            "TechSpecialist": TechSpecialistAgent(),
            "StorySpecialist": StorySpecialistAgent(),
            "GeneralSpecialist": Agent("GeneralSpecialist", "일반적인 자소서 교정을 담당합니다.")
        }
    
    def run(self, user_input: str) -> str:
        """Triage -> Specialist 라우팅 실행 구조"""
        print(f"\n[Agent System] 🔍 TriageAgent가 분석 중...")
        
        if "기술" in user_input or "개발" in user_input or "DB" in user_input or "UI" in user_input:
            routed_to = "TechSpecialist"
        elif "팀" in user_input or "협업" in user_input or "소통" in user_input:
            routed_to = "StorySpecialist"
        else:
            routed_to = "GeneralSpecialist"
            
        print(f"[Agent System] 🔀 라우팅 결정: {routed_to}")
        specialist = self.specialists.get(routed_to, self.specialists["GeneralSpecialist"])
        
        return f"[{specialist.name}의 피드백] '{user_input[:20]}...' 내용을 바탕으로 {specialist.instructions[:20]}.. 관점에서 분석을 완료했습니다."