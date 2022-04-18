
from vitemaprog.database.seeders.seeder_interface import SeederInterface
from vitemaprog.models.auth.right_model import RightModel
from vitemaprog.requests import RightCreate


class RightSeeder(SeederInterface):
    @classmethod
    def run(cls) -> None:
        rights = [
            {"label": 'Test droit 1'},
            {"label": 'Test droit 2'},
            {"label": 'Test droit 3'},
            {"label": 'Test droit 4'},
        ]

        for right in rights:
            right_create = RightCreate(**right)
            try:
                RightModel.create(right_create)
            except Exception as e:
                message = e.args[0]
                if "psycopg2.errors.UniqueViolation" in message:
                    print(f"duplicate right entry : {right['label']}")
                continue
