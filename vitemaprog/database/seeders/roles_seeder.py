
from vitemaprog.database.seeders.seeder_interface import SeederInterface
from vitemaprog.exeptions.model_already_exists_exception import ModelAlreadyExistsException
from vitemaprog.models.auth.role_model import RoleModel
from vitemaprog.models.auth.right_model import RightModel
from vitemaprog.requests import RoleCreate


class RolesSeeder(SeederInterface):
    @classmethod
    def run(cls) -> None:
        roles = [
            {"label": 'Administrateur', "is_admin": True, "slug": 'administrateur'},
            {"label": 'Utilisateur', "rights": ["create-update-delete-programmation"], "slug": 'utilisateur'},
        ]

        for role in roles:
            role_create = RoleCreate(**role)
            try:
                role_model = RoleModel.create(role_create)
                role_model.refresh()

                rights = RightModel.query().filter(RightModel.slug.in_(role.get("rights", []))).all()
                role_model.rights_bdd.extend(rights)
                role_model.save_relations()

            except ModelAlreadyExistsException:
                print(f"duplicate role entry : {role['label']}")
                continue
