# encoding: utf-8

# to provide different access rights
READ = 1
WRITE = 2
EXECUTE = 4

GUEST = 0
USER = READ
MODERATOR = READ | WRITE
ADMIN = READ | WRITE | EXECUTE

# for class DataBaseUser
USERNAME = 2
WATER = 6
STATUS = 7
DATE = 8
PERCENT = 9
USER_FILE = 10
DAYS_HERE = 11
POSTS = 12

# for class DataBaseAdvices
FILE = 3

if __name__ == '__main__':
    # print(USER & READ, USER & WRITE, USER & EXECUTE)
    # print(MODERATOR & READ, MODERATOR & WRITE, MODERATOR & EXECUTE)
    # print(ADMIN & READ, ADMIN & WRITE, ADMIN & EXECUTE)
    # if MODERATOR & WRITE:
    #     print(1)
    # if USER & WRITE:
    #     print(2)
    print(ADMIN)
    print(MODERATOR)




