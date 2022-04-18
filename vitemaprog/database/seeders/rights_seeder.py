
from vitemaprog.database.seeders.seeder_interface import SeederInterface
from vitemaprog.exeptions.model_already_exists_exception import ModelAlreadyExistsException
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
            except ModelAlreadyExistsException:
                print(f"duplicate role entry : {right['label']}")
                continue
