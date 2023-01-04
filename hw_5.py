import user_db_service

userDbService = user_db_service.UserDBService()

userDbService.create_tables()

user0 = user_db_service.User()
user0.last_name = 'andrei1'
user0.first_name = 'burak1'
user0.emails = ['test@test.ru', 'test2@test.ru']
user0.phones = ['7174334', '75823456']

userDbService.add_user(user0)


user1 = user_db_service.User()
user1.last_name = 'andrei2'
user1.first_name = 'burak2'
user1.emails = ['test2@test.ru']
user1.phones = ['7174223']

userDbService.add_user(user1)


user2 = user_db_service.User()
user2.last_name = 'andrei3'
user2.first_name = 'burak3'

userDbService.add_user(user2)


userDbService.add_phones_for_user(['+375296576523', '+377336574832'], 1)

user3 = user_db_service.User()
user3.id = 1
user3.last_name = 'Neburak'
user3.first_name = 'Neandrei'
user3.emails = []
user3.phones = []
userDbService.change_user_info(user3)

userDbService.delete_phones_for_user(1)

userDbService.delete_user_by_id(10)

user4 = user_db_service.User()
user4.emails = ['test2@test.ru']
user4.phones = ['7174223']

print(userDbService.find_user(user4))
