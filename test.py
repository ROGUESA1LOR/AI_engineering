# import fastapi
# api_key="AIzaSyC1cZ7v0ckx9LEv0b7WmNwpQJlqkpfqr1c"
# model=""
# print(api_key)
y=300
x=int(input("Enter you password for transaction: ") )                                 #say this is my pasword
def authenticator(upcoming_func):     #decorator
    def password_checker():           #my objective is a simple transaction authenticater
        if x!=1234:                   #verifying
            return False
        elif x==1234:     
            print("Authorised ")
            upcoming_func()           #what now
        
    return password_checker
@authenticator
def transaction():
    global y
    z=int(input("Enter the amount to be withdrawn: "))
    y=y-z
    print(f"{z} withdrawn successfully your new balance is {y}")
transaction()