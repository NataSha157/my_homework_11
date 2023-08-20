from collections import UserDict
from datetime import date, datetime,timedelta

# Додамо функціонал перевірки на правильність наведених значень для полів Phone, Birthday

class Field(): # буде батьківським для всіх полів, у ньому потім реалізуємо логіку, загальну для всіх полів
    def __init__(self, value):
        # self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            raise ValueError('You forgot to fill in this field')


class Phone(Field): # необов'язкове поле з телефоном та таких один запис (Record) може містити кілька
    def is_phone(self):
        # print('dirty phone =', self.value)
        delimiter = '+- .,/()[]'
        if len(self.value) > 0 and len(self.value) < 25:
            for i in self.value:
                if i in delimiter:
                    a = self.value.replace(i, '')
                    self.value = a
                elif not i.isdigit():
                    raise ValueError("A phone number is a set of numbers!")
        # print('clean phone = ', self.value)
        return self


class Name(Field): # обов'язкове поле з ім'ям
    pass

class Birthday(Field): # поле не обов'язкове, але може бути тільки одне
    def is_date_birthday(self):
        delimiter = ' ,./-'
        # print('self = ', self.value)
        if len(self.value) == 10:
            for s in self.value:
                if s in delimiter:
                    # print(s)
                    a = self.value.replace(s,'-')
                    # print('a = ', a)
                    self.value = a
                    #print('is_date self = ', self)
                    # print('is_date self.value = ', self.value)
                elif not s.isdigit():
                    raise ValueError("Pleas, enter the date of birth in the format: DD-MM-YYY.")
            return self



class Email(Field):
    pass


class Record(): #відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання
    # обов'язкового поля Name.
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            clean_phone = Phone.is_phone(phone)
            self.phones.append(clean_phone)  # якщо телефон прийде як обьект классу то додамо його в список
        # print('rec init phones = ', self.phones[0].value)
        self.birthday = None
        if birthday:
            self.birthday = Birthday.is_date_birthday(birthday)
            # print('rec self.birthday.value = ', self.birthday.value)
        # self.emails = emails


    def add_phone(self, phone: Phone):
        phone_number = Phone(phone)
        clean_number = Phone.is_phone(phone_number)
        if clean_number.value not in [ph.value for ph in self.phones]:
            self.phones.append(clean_number)
        return self


    def edit_phone(self, phone_old, phone_new: Phone):
        phone_number_old = Phone(phone_old)
        phone_number_new = Phone(phone_new)
        if phone_number_old.value in [ph.value for ph in self.phones]:
            # print(phone_number_old.value in [ph.value for ph in self.phones])
            # print('self.phones[0].value =', self.phones[0].value)
            self.phones[0].value = phone_number_new.value
        else:
            self.phones.append(phone_number_new)
            # print('self.phones[1].value =', self.phones[1].value)


    def del_phone(self, phone: Phone): # не розумію, як видалити об"єкт (пише, що його не існує)
        # phone_number = Phone(phone)
        # if phone_number.value in [ph.value for ph in self.phones]:
            # self.phones.remove(phone_number)
        pass


    def days_to_birthday(self):  # повертає кількість днів до наступного дня народження
        birthday_day = date.today()
        now_day = date.today()
        new_birthday_day = date.today()
        if self.birthday.value[2] == '-' and self.birthday.value[5]:
            birthday_day = datetime.strptime(self.birthday.value, '%d-%m-%Y').date()
        elif self.birthday.value[4] == '-' and self.birthday.value[7]:
            birthday_day = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
        # print('birthday_day = ', birthday_day, type(birthday_day))
        if now_day.month > birthday_day.month:
            new_birthday_day = birthday_day.replace(year=now_day.year + 1)

        elif now_day.month < birthday_day.month:
            new_birthday_day = birthday_day.replace(year=now_day.year)
        elif now_day.month == birthday_day.month:
            if now_day.day >= birthday_day.day:
                new_birthday_day = birthday_day.replace(year=now_day.year + 1)
            elif now_day.day < birthday_day.day:
                new_birthday_day = birthday_day.replace(year=now_day.year)
        # print('new birthday_day = ', new_birthday_day)
        delta_day = new_birthday_day - now_day
        return f'{delta_day.days} days until next birthday'
        pass


class AddressBook(UserDict): # наслідується від UserDict, та ми потім додамо логіку пошуку за записами до цього класу

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, N: int = 2):  # повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів
        for key,value in self.data.items():
            print(f"Abonent {key}, phone: {value.phones[0].value}, birthday: {value.birthday.value}. {Record.days_to_birthday(value)}")


if __name__ == "__main__":
    name = Name('Bill')
    phone = Phone('+ 12 34 56 7 8 9 0')
    birthday = Birthday('08-08/1999')
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)

    name1 = Name('Ann')
    phone1 = Phone('+ 38 (050) 585 - 58 - 58')
    phone11 = Phone('+ 38 067 670-16-16')
    birthday1 = Birthday('1944/02-20')
    rec1 = Record(name1, phone1, birthday1)
    ab1 = AddressBook()
    ab1.add_record(rec1)




    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    # assert ab['Bill'].phones[0].value == '1234567890'

    # print(isinstance(ab['Bill'].birthday, Birthday))
    # print("ab: ",ab['Bill'].birthday.value)
    #
    # print(rec.birthday.value, type(rec.birthday.value))
    # # print(Birthday.is_date_birthday(birthday))
    # print(rec.days_to_birthday())
    #
    # print(rec1.name.value)
    # print(rec1.phones[0].value)
    # print(rec1.birthday.value)
    # print(rec1.days_to_birthday())

    # print(Phone.is_phone(phone1))
    # print(rec1.phones[0].value)
    # print(rec1.phones[0].value)
    # print(rec.phones[0].value)

    print(AddressBook.iterator(ab))
    print(AddressBook.iterator(ab1))
