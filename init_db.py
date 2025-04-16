from ZeroCalendar import db, app

def create_db():
    with app.app_context():
        db.create_all()
        print("Database initialized.")    


def create_user(name=None, session_cookie=None, created_at=None):

    raise Exception('USERS function is overkill, and not implemented.')

    with app.app_context():
        if created_at is not None:
            new_user = User(name=name, session_cookie=session_cookie, created_at=created_at)
        else:
            new_user = User(name=name, session_cookie=session_cookie)

        db.session.add(new_user)
        db.session.commit()

        print("] Created user - ", new_user)

def main():
    create_db()
    #create_user(name='Rick')
    #create_user(name='Test')




if __name__ == '__main__':
    main()