
from vitemaprog.database.seeders.seeder_interface import SeederInterface
from vitemaprog.models.auth.right_model import RightModel
from vitemaprog.requests import RightCreate


class RightSeeder(SeederInterface):
    @classmethod
    def run(cls) -> None:
        rights = [
            {
                "label": 'Create Update Delete User',
                "slug": 'create-update-delete-user',
                "description": 'Authorise la création, la modification et la suppression des utilisateurs'
            },
            {
                "label": 'Create Update Delete Programmations',
                "slug": 'create-update-delete-programmation',
                "description": 'Authorise la création, la modification et la suppression des programmations'
            },
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
                else:
                    raise e
