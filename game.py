"""메뉴와 게임 진행을 담당합니다."""

from default_quizzes import make_default_quizzes
from quiz import Quiz


class QuizGame:
    def __init__(self) -> None:
        self.quizzes: list[Quiz] = make_default_quizzes()
        self.best_score: dict | None = None

    @staticmethod
    def read_number(prompt: str, minimum: int, maximum: int) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                number = int(raw)
            except ValueError:
                print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")
                continue
            if minimum <= number <= maximum:
                return number
            print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")

    def play(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        correct = 0
        print(f"\n퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            answer = self.read_number("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
        total = len(self.quizzes)
        score = round(correct / total * 100)
        print(f"\n결과: {total}문제 중 {correct}문제 정답! ({score}점)")

    @staticmethod
    def read_text(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("내용을 입력하세요.")

    def add_quiz(self) -> None:
        print("\n새 퀴즈를 추가합니다.")
        question = self.read_text("문제: ")
        choices = [self.read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = self.read_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        print("퀴즈가 추가되었습니다.")

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def run(self) -> None:
        while True:
            print("\n=== 상식 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")
            choice = self.read_number("선택: ", 1, 5)
            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 5:
                print("다음에 또 만나요!")
                return
            else:
                print("기능을 준비 중입니다.")
