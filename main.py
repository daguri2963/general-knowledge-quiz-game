"""상식 퀴즈 게임 실행 파일."""

from game import QuizGame

def main() -> None:
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")
        game.save()


if __name__ == "__main__":
    main()
