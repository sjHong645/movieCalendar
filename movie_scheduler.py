import os
import json
from datetime import datetime

class ScheduleManager:
    def __init__(self):
        self.current_user = None
        self.movies_to_watch = []
        self.crawled_showtimes = []
        self.my_schedule = {}
        self.travel_times = {}

    def select_user(self):
        print("\n=== 사용자 선택 ===")
        
        # 기존 사용자 파일들 검색
        existing_users = []
        for filename in os.listdir('.'):
            if filename.endswith('_schedule.json'):
                username = filename.replace('_schedule.json', '')
                existing_users.append(username)
        
        if existing_users:
            print("기존 사용자:")
            for i, user in enumerate(existing_users, 1):
                print(f"{i}. {user}")
            print(f"{len(existing_users) + 1}. 새 사용자 생성")
            
            try:
                choice = int(input("선택하세요: "))
                if 1 <= choice <= len(existing_users):
                    self.current_user = existing_users[choice - 1]
                    print(f"사용자 '{self.current_user}'로 로그인했습니다.")
                    self.load_user_data()
                elif choice == len(existing_users) + 1:
                    self.create_new_user()
                else:
                    print("올바른 번호를 입력해주세요.")
                    return False
            except ValueError:
                print("숫자를 입력해주세요.")
                return False
        else:
            print("등록된 사용자가 없습니다. 새 사용자를 생성합니다.")
            self.create_new_user()
        
        return True
    
    def create_new_user(self):
        username = input("사용자 이름을 입력하세요: ").strip()
        if not username:
            print("올바른 사용자 이름을 입력해주세요.")
            return False
        
        # 파일명에 사용할 수 없는 문자 체크
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in username for char in invalid_chars):
            print("파일명에 사용할 수 없는 문자가 포함되어 있습니다.")
            return False
        
        self.current_user = username
        print(f"새 사용자 '{username}'가 생성되었습니다.")
        return True

    def load_user_data(self):
        if not self.current_user:
            return
        
        schedule_file = f"{self.current_user}_schedule.json"
        travel_file = f"{self.current_user}_travel_times.json"
        
        # 시간표 데이터 로드
        try:
            if os.path.exists(schedule_file):
                with open(schedule_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.movies_to_watch = data.get('movies_to_watch', [])
                    self.my_schedule = data.get('my_schedule', {})
                print(f"시간표 데이터를 불러왔습니다.")
            else:
                # 파일이 없으면 초기값으로 설정
                self.movies_to_watch = []
                self.my_schedule = {}
        except Exception as e:
            print(f"시간표 데이터 로드 중 오류 발생: {e}")
            self.movies_to_watch = []
            self.my_schedule = {}
        
        # 이동 시간 데이터 로드
        try:
            if os.path.exists(travel_file):
                with open(travel_file, 'r', encoding='utf-8') as f:
                    self.travel_times = json.load(f)
                print(f"이동 시간 데이터를 불러왔습니다.")
            else:
                self.travel_times = {}
        except Exception as e:
            print(f"이동 시간 데이터 로드 중 오류 발생: {e}")
            self.travel_times = {}

    def save_user_data(self):
        if not self.current_user:
            return
        
        schedule_file = f"{self.current_user}_schedule.json"
        travel_file = f"{self.current_user}_travel_times.json"
        
        # 시간표 데이터 저장
        try:
            schedule_data = {
                'movies_to_watch': self.movies_to_watch,
                'my_schedule': self.my_schedule
            }
            with open(schedule_file, 'w', encoding='utf-8') as f:
                json.dump(schedule_data, f, ensure_ascii=False, indent=2)
            print(f"시간표 데이터가 저장되었습니다. ({schedule_file})")
        except Exception as e:
            print(f"시간표 데이터 저장 중 오류 발생: {e}")
        
        # 이동 시간 데이터 저장
        try:
            with open(travel_file, 'w', encoding='utf-8') as f:
                json.dump(self.travel_times, f, ensure_ascii=False, indent=2)
            if self.travel_times:  # 이동 시간 데이터가 있을 때만 메시지 출력
                print(f"이동 시간 데이터가 저장되었습니다. ({travel_file})")
        except Exception as e:
            print(f"이동 시간 데이터 저장 중 오류 발생: {e}")

    def get_travel_time(self, start_loc, end_loc):
        pass

    def add_movie_to_watch(self):
        print("\n=== 보고 싶은 영화 추가 ===")
        movie_title = input("영화 제목을 입력하세요: ").strip()
        if movie_title and movie_title not in self.movies_to_watch:
            self.movies_to_watch.append(movie_title)
            print(f"'{movie_title}'이(가) 목록에 추가되었습니다.")
        elif movie_title in self.movies_to_watch:
            print("이미 목록에 있는 영화입니다.")
        else:
            print("올바른 영화 제목을 입력해주세요.")

    def view_movies_to_watch(self):
        print("\n=== 보고 싶은 영화 목록 ===")
        if not self.movies_to_watch:
            print("목록이 비어있습니다.")
        else:
            for i, movie in enumerate(self.movies_to_watch, 1):
                print(f"{i}. {movie}")

    def add_to_my_schedule(self):
        print("\n=== 내 시간표에 영화 추가 ===")
        if not self.movies_to_watch:
            print("먼저 보고 싶은 영화를 추가해주세요.")
            return

        print("보고 싶은 영화 목록:")
        for i, movie in enumerate(self.movies_to_watch, 1):
            print(f"{i}. {movie}")

        try:
            choice = int(input("선택할 영화 번호를 입력하세요: "))
            if 1 <= choice <= len(self.movies_to_watch):
                movie_title = self.movies_to_watch[choice - 1]
            else:
                print("올바른 번호를 입력해주세요.")
                return
        except ValueError:
            print("숫자를 입력해주세요.")
            return

        theater = input("영화관을 입력하세요 (예: CGV 용산): ").strip()
        location = input("위치를 입력하세요 (예: 용산): ").strip()
        day = input("요일을 입력하세요 (예: 월요일): ").strip()
        start_time = input("시작 시간을 입력하세요 (예: 14:30): ").strip()
        
        try:
            runtime = int(input("상영 시간(분)을 입력하세요 (예: 134): "))
        except ValueError:
            print("올바른 숫자를 입력해주세요.")
            return

        movie_info = {
            'title': movie_title,
            'theater': theater,
            'location': location,
            'start_time': start_time,
            'runtime': runtime
        }

        if day not in self.my_schedule:
            self.my_schedule[day] = []

        self.my_schedule[day].append(movie_info)
        print(f"'{movie_title}'이(가) {day} 시간표에 추가되었습니다.")

    def crawl_showtimes(self):
        pass

    def display_schedule(self):
        print("\n=== 나의 주간 영화 시간표 ===")
        if not self.my_schedule:
            print("시간표가 비어있습니다.")
            return

        days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        
        for day in days:
            if day in self.my_schedule and self.my_schedule[day]:
                print(f"\n[{day}]")
                for movie in self.my_schedule[day]:
                    end_hour = int(movie['start_time'].split(':')[0])
                    end_minute = int(movie['start_time'].split(':')[1]) + movie['runtime']
                    if end_minute >= 60:
                        end_hour += end_minute // 60
                        end_minute = end_minute % 60
                    end_time = f"{end_hour:02d}:{end_minute:02d}"
                    
                    print(f"  * {movie['title']}")
                    print(f"    장소: {movie['theater']} ({movie['location']})")
                    print(f"    시간: {movie['start_time']} ~ {end_time} ({movie['runtime']}분)")

    def run(self):
        print("개인 맞춤형 영화 시간표 자동 생성기 v0.2")
        print("=" * 50)
        
        # 사용자 선택
        if not self.select_user():
            print("사용자 선택에 실패했습니다.")
            return
        
        while True:
            print("\n[메뉴]")
            print("1. 보고 싶은 영화 추가")
            print("2. 보고 싶은 영화 목록 보기")
            print("3. 내 시간표에 영화 추가")
            print("4. 주간 시간표 보기")
            print("5. 데이터 저장")
            print("6. 프로그램 종료")
            
            choice = input("\n선택하세요 (1-6): ").strip()
            
            if choice == '1':
                self.add_movie_to_watch()
            elif choice == '2':
                self.view_movies_to_watch()
            elif choice == '3':
                self.add_to_my_schedule()
            elif choice == '4':
                self.display_schedule()
            elif choice == '5':
                self.save_user_data()
            elif choice == '6':
                print("데이터를 저장하고 프로그램을 종료합니다.")
                self.save_user_data()
                break
            else:
                print("올바른 번호를 선택해주세요.")

if __name__ == "__main__":
    manager = ScheduleManager()
    manager.run()