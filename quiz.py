"""개별 문제의 데이터와 정답 확인을 담당합니다."""

from dataclasses import dataclass


@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: int

    def __post_init__(self) -> None:
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if not isinstance(self.choices, list) or len(self.choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if any(not isinstance(item, str) or not item.strip() for item in self.choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if type(self.answer) is not int or not 1 <= self.answer <= 4:
            raise ValueError("정답은 1~4 사이의 숫자여야 합니다.")

    def display(self, number: int) -> None:
        print(f"\n[문제 {number}] {self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, choice: int) -> bool:
        return choice == self.answer

    def to_dict(self) -> dict:
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        return cls(data["question"], data["choices"], data["answer"])
