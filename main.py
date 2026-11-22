"""터미널에서 실행하는 상식 퀴즈 게임."""


def main() -> None:
    while True:
        print("\n=== 상식 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        choice = input("선택: ").strip()
        if choice == "5":
            print("다음에 또 만나요!")
            return
        if choice in {"1", "2", "3", "4"}:
            print("기능을 준비 중입니다.")
        else:
            print("1~5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()
