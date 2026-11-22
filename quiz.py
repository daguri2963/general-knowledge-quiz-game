"""개별 문제의 데이터와 정답 확인을 담당합니다."""

from dataclasses import dataclass


# dataclass가 문제 데이터용 __init__을 만들어 주므로 필드 정의에 집중할 수 있습니다.
@dataclass
class Quiz:
    """한 문제의 데이터와 표시·정답 판정을 묶어 형식을 일관되게 유지합니다."""

    # question은 사용자가 볼 문제 문장입니다.
    question: str
    # choices는 화면에 1~4번으로 보여 줄 네 개의 선택지입니다.
    choices: list[str]
    # answer는 선택지의 위치를 나타내는 1부터 시작하는 정답 번호입니다.
    answer: int

    def __post_init__(self) -> None:
        """잘못된 문제를 저장하거나 출제하지 않도록 생성 직후 검사합니다."""
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if not isinstance(self.choices, list) or len(self.choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if any(not isinstance(item, str) or not item.strip() for item in self.choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if type(self.answer) is not int or not 1 <= self.answer <= 4:
            raise ValueError("정답은 1~4 사이의 숫자여야 합니다.")

    def display(self, number: int) -> None:
        """풀이 순서인 number와 네 개의 선택지를 화면에 출력합니다."""
        print(f"\n[문제 {number}] {self.question}")
        # enumerate의 시작값을 1로 맞춰 사용자 입력 번호와 화면 번호를 일치시킵니다.
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, choice: int) -> bool:
        """입력한 번호가 정답인지 bool 값으로 돌려 점수 계산에 사용합니다."""
        return choice == self.answer

    def to_dict(self) -> dict:
        """Quiz 객체를 JSON에 쓸 수 있는 사전으로 변환합니다."""
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """저장된 사전으로 Quiz를 만들며 생성 시 데이터 검증도 다시 실행합니다."""
        return cls(data["question"], data["choices"], data["answer"])
