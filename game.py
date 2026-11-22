"""메뉴와 게임 진행을 담당합니다."""

from quiz import Quiz
from storage import load_state, save_state


class QuizGame:
    def __init__(self) -> None:
        self.quizzes, self.best_score = load_state()

    def save(self) -> bool:
        return save_state(self.quizzes, self.best_score)

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
        if self.best_score is None or score > self.best_score["score"]:
            self.best_score = {"score": score, "correct": correct, "total": total}
            print("새로운 최고 점수입니다!")
            save_state(self.quizzes, self.best_score)

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
        if save_state(self.quizzes, self.best_score):
            print("퀴즈가 추가되고 저장되었습니다.")

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def show_score(self) -> None:
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return
        best = self.best_score
        print(f"최고 점수: {best['score']}점 ({best['total']}문제 중 {best['correct']}문제 정답)")

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
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.save()
                print("다음에 또 만나요!")
                return
