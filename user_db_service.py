import database


class User:
    id: int = None
    first_name: str
    last_name: str
    emails = []
    phones = []


class UserDBService:

    def execute(self, callback, *attr):
        connect, cursor = database.connect()

        res = callback((connect, cursor), *attr)

        connect.commit()
        connect.close()

        return res

    def create_tables(self):
        self.execute(self._create_tables)

    def add_user(self, user: User):
        return self.execute(self._add_user, user)

    def add_phones_for_user(self, phones, user_id):
        self.execute(self._add_phones_for_user, phones, user_id)

    def add_emails_for_user(self, emails, user_id):
        self.execute(self._add_emails_for_user, emails, user_id)

    def change_user_info(self, user: User):
        self.execute(self._change_user_info, user)

    def delete_phones_for_user(self, user_id):
        self.execute(self._delete_phones_for_user, user_id)

    def change_user_phones(self, phones, user_id):
        self.execute(self._change_user_phones, phones, user_id)

    def change_user_emails(self, emails, user_id):
        self.execute(self._change_user_emails, emails, user_id)

    def delete_user_by_id(self, user_id):
        self.execute(self._delete_user_by_id, user_id)

    def find_user(self, user: User):
        return self.execute(self._find_user, user)

    def Delete_emails_for_user(self, user_id):
        self.execute(self._delete_emails_for_user, user_id)

    def _create_tables(self, connect):
        (_, cursor) = connect

        cursor.execute(
            'create table if not exists Users (id SERIAL PRIMARY KEY, first_name varchar(25), last_name varchar(25));')
        cursor.execute(
            'create table if not exists Emails (email varchar(100), user_id SERIAL references Users(id), PRIMARY key (email, user_id));')
        cursor.execute(
            'create table if not exists Phones (phone varchar(20), user_id SERIAL references Users(id), PRIMARY key (phone, user_id));')

    def _add_user(self, connect, user: User):
        (_, cursor) = connect

        cursor.execute('insert into Users (first_name, last_name) values(%s, %s) returning id;', [
                       user.first_name, user.last_name])
        user_id = cursor.fetchone()[0]

        self._add_emails_for_user(connect, user.emails, user_id)
        self._add_phones_for_user(connect, user.phones, user_id)

        return user_id

    def _add_phones_for_user(self, connect, phones=[], user_id=None):
        (_, cursor) = connect

        if len(phones) > 0 and user_id is not None:
            params = list(map(lambda phone: [phone, user_id], phones))
            cursor.executemany(
                'insert into Phones (phone, user_id) values(%s, %s);', params)

    def _add_emails_for_user(self, connect, emails=[], user_id=None):
        (_, cursor) = connect

        if len(emails) > 0:
            params = list(map(lambda email: [email, user_id], emails))
            cursor.executemany(
                'insert into Emails (email, user_id) values(%s, %s);', params)

    def _change_user_info(self, connect, user: User):
        (_, cursor) = connect

        if user.id is not None:
            cursor.execute(
                "update Users set first_name = %s, last_name = %s where id = %s;",
                [user.first_name, user.last_name, user.id]
            )

            self._change_user_phones(connect, user.phones, user.id)
            self._change_user_emails(connect, user.emails, user.id)

    def _delete_phones_for_user(self, connect, user_id):
        (_, cursor) = connect

        cursor.execute('delete from Phones where user_id = %s;', [user_id])

    def _delete_emails_for_user(self, connect, user_id):
        (_, cursor) = connect

        cursor.execute('delete from Emails where user_id = %s;', [user_id])

    def _change_user_phones(self, connect, phones=[], user_id=None):
        (_, cursor) = connect

        if user_id is not None:
            self._delete_phones_for_user(connect, user_id)

            if len(phones) > 0:
                params = list(map(lambda phone: [phone, user_id], phones))
                cursor.executemany(
                    "update Phones set phone = %s where user_id = %s;", params)

    def _change_user_emails(self, connect, emails=[], user_id=None):
        (_, cursor) = connect

        if user_id is not None:
            self._delete_emails_for_user(connect, user_id)

            if len(emails) > 0:
                params = list(map(lambda email: [email, user_id], emails))
                cursor.executemany(
                    "update Emails set email = %s where user_id = %s;", params)

    def _delete_user_by_id(self, connect, user_id):
        (_, cursor) = connect

        if user_id is not None:
            cursor.execute('delete from Users where id = %s', [user_id])

    def _find_user(self, connect, user: User):
        (_, cursor) = connect

        where = []

        if user.id is not None:
            where.append(f'id = {user.id} ')

        if hasattr(user, 'first_name'):
            where.append(f'first_name = {user.first_name} ')

        if hasattr(user, 'last_name'):
            where.append(f'last_name = {user.last_name} ')

        if len(user.emails) > 0:
            arr = ', '.join(user.emails)
            where.append("email = any('{%s}'::text[])" % (arr))

        if len(user.phones) > 0:
            arr = ', '.join(user.phones)
            where.append("phone = any('{%s}'::text[])" % (arr))

        if len(where) > 0:
            cursor.execute("""
                select u.id, u.first_name, u.last_name, e.email, p.phone
                from Users u
                join Emails e on e.user_id = u.id
                join Phones p on p.user_id = u.id
                where %s;
            """ % ' and '.join(where))

            return cursor.fetchall()
