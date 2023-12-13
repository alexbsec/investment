import getpass

def authorize():
    attempts = 3
    for i in range(attempts):
        passwd = getpass.getpass("Enter password: ")
        
        if passwd == "mypasswd":
            print("Access granted")
            return True
        
        print("Invalid password. Try again")
        
    print("Access denied")

    return False

