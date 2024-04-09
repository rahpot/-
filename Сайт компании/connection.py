db_name = input()


def connect(db_name):
    global_init(db_name)
    db_sess = create_session()
    db_sess.commit()
    id_members = []
    for deport in db_sess.query(Departments).filter(Departments.id == 1):
        for id_member in [int(i) for i in str(deport.members).split(', ')]:
            id_members.append(id_member)

    for user in db_sess.query(User).filter(User.id.in_(id_members)):
        h = 0
        for job in user.jobs:
            h += job.work_size
        if h > 25:
            print(f"""{user.surname} {user.name}""")


connect(db_name)
