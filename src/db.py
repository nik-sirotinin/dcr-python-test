import sqlite3

conn = None


class DBO:
    DB_FILE = "../data/countries.db"

    def __init__(self):
        global conn

        if conn is None:
            conn = sqlite3.connect(self.DB_FILE)
        self.cursor = conn.cursor()

        self.data = None


class Region(DBO):
    def create(self, name):
        insert_query = "INSERT INTO region (name) VALUES (?)"
        self.cursor.execute(insert_query, (name,))
        conn.commit()

    def get_by_name(self, name):
        select_query = "SElECT id, name FROM region WHERE name=?"
        self.cursor.execute(select_query, (name,))
        region_data = self.cursor.fetchone()
        if not region_data:
            return False
        headers = [header[0] for header in self.cursor.description]
        self.data = {k: v for k, v in zip(headers, region_data)}
        return True

    def get_or_create_by_name(self, name):
        self.get_by_name(name)
        if not self.data:
            self.create(name)
        self.get_by_name(name)


class TopLevelDomain(DBO):
    def create(self, name):
        insert_query = "INSERT INTO topLevelDomain (name) VALUES (?)"
        self.cursor.execute(insert_query, (name,))
        conn.commit()

    def get_by_name(self, name):
        select_query = "SElECT id, name FROM topLevelDomain WHERE name=?"
        self.cursor.execute(select_query, (name,))
        tld_data = self.cursor.fetchone()
        if not tld_data:
            return False
        headers = [header[0] for header in self.cursor.description]
        self.data = {k: v for k, v in zip(headers, tld_data)}
        return True

    def get_or_create_by_name(self, name):
        self.get_by_name(name)
        if not self.data:
            self.create(name)
        self.get_by_name(name)


class CountryTopLevelDomain(DBO):
    def get_or_create(self, country_id, tld_id):
        select_query = "SELECT * FROM countryTopLevelDomain WHERE country_id = ? AND topLevelDomain_id = ?"
        self.cursor.execute(select_query, (country_id, tld_id))
        if self.cursor.fetchone() is None:
            insert_query = "INSERT INTO countryTopLevelDomain (country_id, topLevelDomain_id) VALUES (?, ?)"
            self.cursor.execute(insert_query, (country_id, tld_id))
            conn.commit()


class Country(DBO):
    def insert(self, name, alpha2Code, alpha3Code, population, region_id, capital):
        insert_query = (
            "INSERT INTO country (name, alpha2Code, alpha3Code, population, "
            "region_id, capital) VALUES (?, ?, ?, ?, ?, ?)"
        )
        self.cursor.execute(
            insert_query, (name, alpha2Code, alpha3Code, population, region_id, capital)
        )
        conn.commit()
        self.get_by_name(name)

    def update_capital(self, capital):
        update_query = "UPDATE country SET capital = ? WHERE id = ?"
        self.cursor.execute(update_query, (capital, self.data["id"]))
        conn.commit()

    def get_by_name(self, name):
        select_query = "SElECT * FROM country WHERE name=?"
        self.cursor.execute(select_query, (name,))
        region_data = self.cursor.fetchone()
        if not region_data:
            return False
        headers = [header[0] for header in self.cursor.description]
        self.data = {k: v for k, v in zip(headers, region_data)}
        return True

    @classmethod
    def list_all(cls):
        dbo = DBO()
        select_statement = """
            SELECT c.id, c.name AS country_name, c.alpha2Code, c.alpha3Code,
                    c.capital, c.population, r.name AS region_name
                FROM country c
                JOIN region r ON c.region_id = r.id;
            """
        dbo.cursor.execute((select_statement))
        headers = [header[0] for header in dbo.cursor.description]

        for row in dbo.cursor.fetchall():
            obj = cls()
            country_id = row[0]
            obj.data = {k: v for k, v in zip(headers, row)}
            dbo.cursor.execute(
                "SELECT tld.name "
                "FROM topLevelDomain tld "
                "INNER JOIN countryTopLevelDomain ctld ON tld.id = ctld.topLevelDomain_id "
                "WHERE ctld.country_id = ?",
                (country_id,),
            )
            tlds = dbo.cursor.fetchall()
            obj.data["topLevelDomain"] = tlds
            yield obj
