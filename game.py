"""메뉴와 게임 진행을 담당합니다."""

from quiz import Quiz
from storage import load_state, save_state


class QuizGame:
    """퀴즈 목록과 최고 점수를 보관하고 메뉴별 동작을 연결합니다."""

    def __init__(self) -> None:
        """첫 실행에는 기본 문제를, 재실행에는 저장된 상태를 불러옵니다."""
        # quizzes와 best_score를 한 번에 읽어 화면과 저장 파일의 상태를 맞춥니다.
        self.quizzes, self.best_score = load_state()

    def save(self) -> bool:
        """현재 문제와 최고 점수를 저장하고 성공 여부를 돌려줍니다."""
        return save_state(self.quizzes, self.best_score)

    @staticmethod
    def read_number(prompt: str, minimum: int, maximum: int) -> int:
        """메뉴와 정답 입력에 공통으로 쓰는 범위 검증 숫자 입력입니다."""
        while True:
            # raw의 앞뒤 공백을 없애 ' 2 '도 2로 처리합니다.
            raw = input(prompt).strip()
            if not raw:
                print(f"입력이 비어 있습니다. {minimum}~{maximum} 사이의 숫자를 입력하세요.")
                continue
            try:
                # number로 변환한 뒤에만 범위를 검사해 문자 입력으로 게임이 종료되지 않게 합니다.
                number = int(raw)
            except ValueError:
                print(f"숫자가 아닙니다. {minimum}~{maximum} 사이의 숫자를 입력하세요.")
                continue
            if minimum <= number <= maximum:
                return number
            print(f"범위를 벗어났습니다. {minimum}~{maximum} 사이의 숫자를 입력하세요.")

    def play(self) -> None:
        """모든 문제를 풀게 하고 정답 수·백분율·최고 점수를 계산합니다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        # correct는 이번 게임에서 맞힌 문제 수를 누적합니다.
        correct = 0
        print(f"\n퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        # number는 화면 번호, quiz는 현재 문제, answer는 사용자가 고른 번호입니다.
        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            answer = self.read_number("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
        # total을 따로 보관해 정답 수와 함께 결과 및 최고 기록에 남깁니다.
        total = len(self.quizzes)
        # score는 문제 수가 달라도 기록을 비교할 수 있게 100점 만점으로 환산합니다.
        score = round(correct / total * 100)
        print(f"\n결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score["score"]:
            # 최고 기록에는 점수뿐 아니라 당시의 문제 수와 정답 수도 보관합니다.
            self.best_score = {"score": score, "correct": correct, "total": total}
            print("새로운 최고 점수입니다!")
            save_state(self.quizzes, self.best_score)

    @staticmethod
    def read_text(prompt: str) -> str:
        """문제와 선택지에 빈 문자열이 들어가지 않도록 다시 입력받습니다."""
        while True:
            # value를 비워 두면 Quiz 생성 시 오류가 나므로 여기서 다시 받습니다.
            value = input(prompt).strip()
            if value:
                return value
            print("내용을 입력하세요.")

    def add_quiz(self) -> None:
        """문제·선택지·정답을 받아 Quiz를 만들고 즉시 저장합니다."""
        print("\n새 퀴즈를 추가합니다.")
        # question과 choices를 나눠 받아 Quiz의 세 속성과 같은 형태로 구성합니다.
        question = self.read_text("문제: ")
        choices = [self.read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = self.read_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if save_state(self.quizzes, self.best_score):
            print("퀴즈가 추가되고 저장되었습니다.")

    def list_quizzes(self) -> None:
        """저장된 문제의 번호와 문장을 보여 주며 빈 목록도 안내합니다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def show_score(self) -> None:
        """아직 기록이 없는 경우와 최고 기록이 있는 경우를 구분해 보여 줍니다."""
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return
        # best는 딕셔너리의 점수·정답 수·문제 수를 읽기 쉽게 출력하기 위한 지역 변수입니다.
        best = self.best_score
        print(f"최고 점수: {best['score']}점 ({best['total']}문제 중 {best['correct']}문제 정답)")

    def run(self) -> None:
        """종료를 고를 때까지 메뉴를 반복하고 선택한 기능을 호출합니다."""
        while True:
            print("\n=== 상식 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")
            # choice는 메뉴 번호이며 공통 입력 함수가 1~5 범위를 보장합니다.
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
