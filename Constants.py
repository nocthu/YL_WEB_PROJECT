READ = 1
WRITE = 2
EXECUTE = 4

GUEST = 0
USER = READ
MODERATOR = READ | WRITE
ADMIN = READ | WRITE | EXECUTE


STATUS = 7
USERNAME = 1
FILE = 3
WATER = 6
DATE = 8
PERCENT = 9

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




