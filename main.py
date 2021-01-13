from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

association_table = Table(
    'association_table', Base.metadata,
    Column('assignee', Integer, ForeignKey('users.id')),
    Column('assigned', Integer, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    address = Column(String)
    phone = relationship("Phone", backref='owner')
    emails = relationship('Email', backref='owner')
    partners = relationship('User', secondary=association_table,
                            primaryjoin=association_table.c.assignee == id,
                            secondaryjoin=association_table.c.assigned == id)

    def __repr__(self):
        return f'\n\n<User(name={self.first_name} {self.last_name}, address={self.address}>,\nemails={self.emails},' \
               f'\nphone_numbers:{self.phone},\npartners {self.partners}> '


class Phone(Base):
    __tablename__ = "phone"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'\n\t<number={self.number}, user_id={self.owner_id}>'


class Email(Base):
    __tablename__ = "email"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'\n\t<email={self.email}, user_id={self.owner_id}>'


def create_sample():
    engine = create_engine("sqlite:///users.db", echo=False)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    user1 = User(first_name='John', last_name='Cena', address='Essex 10-500 Elizabeth st. 5')
    session.add(user1)

    mail1 = Email(email='somemail@kiskes.com', owner=user1)
    session.add(mail1)

    phone1 = Phone(number=601284888, owner=user1)
    session.add(phone1)

    user2 = User(first_name='Under', last_name='Taker', address='Mississippi 35-150 Nulla St.Mankato 96522')
    session.add(user2)

    mail21 = Email(email='teddymail@kiskes.com', owner=user2)
    session.add(mail21)

    mail22 = Email(email='teddypriv@kiskes.com', owner=user2)
    session.add(mail22)

    phone21 = Phone(number=600800200, owner=user2)
    session.add(phone21)

    phone22 = Phone(number=12312313, owner=user2)
    session.add(phone22)

    user3 = User(first_name='Hulk', last_name='Hogan', address='Rhode Island 20-400 Nunc. Avenue Erie 24975')
    user3.partners.append(user1)
    session.add(user3)

    user4 = User(first_name='Rey', last_name='Mysterio', address='Rhode Island 20-420 Beach North Dakota 58563')
    user4.partners.append(user2)

    mail31 = Email(email='hellokitty@kiskes.com', owner=user4)
    session.add(mail31)

    phone31 = Phone(number=726800137, owner=user4)
    session.add(phone31)

    phone32 = Phone(number=637298473, owner=user4)
    session.add(phone32)

    # all_users = session.query(User).all()
    # print(str(all_users))

    session.close()


def add_user():
    engine = create_engine("sqlite:///users.db", echo=False)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    firstname = input('First name: ')
    lastname = input('Last name: ')
    someaddress = input('Address: ')
    mailamount = int(input('How many email addresses? '))
    mails = []
    for x in range(mailamount):
        mails.append(input(f'Email address nr {x + 1}: '))

    phoneamount = int(input('How many phone numbers? '))
    num = []
    for x in range(phoneamount):
        num.append(int(input(f'Phone number nr {x + 1}: ')))

    # TODO: while partner amount smaller than amount of users
    partneramount = int(input("How many partners? "))
    partner = []
    for _ in range(partneramount):
        partner.append(input('Partner\'s last name: '))

    new_user = User(first_name=firstname, last_name=lastname, address=someaddress)
    session.add(new_user)
    for x in mails:
        new_email = Email(email=x, owner=new_user)
        session.add(new_email)

    for x in num:
        new_num = Phone(number=x, owner=new_user)
        session.add(new_num)

    for x in partner:
        partnerquery = session.query(User).filter(User.last_name == x)
        somepartner = session.query(User).get(partnerquery[0].id)
        new_user.partners.append(somepartner)

    print(f'Added user: {new_user}')
    session.commit()
    session.close()


def find_user():
    engine = create_engine("sqlite:///users.db", echo=False)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    search_text = 'Search by:\n1) First name\n2) Last name\n3) Address\n4) ID\n'
    choice = int(input(search_text))
    if choice == 1:
        search = input('Enter first name: ')
        queryresult = session.query(User).filter(User.first_name == search)
        for result in queryresult:
            print(session.query(User).get(result.id))

    if choice == 2:
        search = input('Enter last name: ')
        queryresult = session.query(User).filter(User.last_name == search)
        for result in queryresult:
            print(session.query(User).get(result.id))

    if choice == 3:
        search = input('Enter address: ')
        queryresult = session.query(User).filter(User.address.like(search + '%'))
        for result in queryresult:
            print(session.query(User).get(result.id))

    if choice == 4:
        search = input('Enter id: ')
        print(session.query(User).get(search))

    session.close()


def print_all_users():
    engine = create_engine("sqlite:///users.db", echo=False)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    all_users = session.query(User).all()
    print(str(all_users))

    session.close()


if __name__ == '__main__':
    create_sample()
    pick = 'x'
    operation_select = '\n1) Add User\n2) Find User\n3) Print all users\n4) Exit\n'
    while pick != '4':
        pick = input(operation_select)
        if pick == '1':
            add_user()
        if pick == '2':
            find_user()
        if pick == '3':
            print_all_users()
