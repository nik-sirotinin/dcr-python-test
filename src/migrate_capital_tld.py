from typing import List
from db import DBO


class Migration(DBO):

    def create_table(self, table_name: str, fields: List[str]):
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table_name}(
            {",".join(fields)}
            )"""
        )

    def run(self):
        self.cursor.execute("PRAGMA table_info('country')")
        column_names = [col[1] for col in self.cursor.fetchall()]
        if "capital" not in column_names:
            print("adding col for capital")
            alter_query = f"ALTER TABLE country ADD COLUMN capital TEXT"
            self.cursor.execute(alter_query)
        # Top-level domain table
        print("creating TLD table")
        self.create_table(
            "topLevelDomain", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL"]
        )
        print(f"conn: {conn}")
        # Junction table
        print("Creating junction table")
        self.create_table(
            "countryTopLevelDomain",
            [
                "country_id INTEGER",
                "topLevelDomain_id INTEGER",
                "PRIMARY KEY(country_id, topLevelDomain_id)",
                "FOREIGN KEY(country_id) REFERENCES country(id)",
                "FOREIGN KEY(topLevelDomain_id) REFERENCES topLevelDomain(id)",
            ],
        )


if __name__ == "__main__":
    Migration().run()
