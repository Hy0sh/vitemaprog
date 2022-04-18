
from vitemaprog.database.seeders.seeder_interface import SeederInterface
from vitemaprog.models.auth.role_model import RoleModel
from vitemaprog.models.auth.right_model import RightModel
from vitemaprog.requests import RoleCreate


class RolesSeeder(SeederInterface):
    @classmethod
    def run(cls) -> None:
        roles = [
            {"label": 'Administrateur', "is_admin": True, "slug": 'administrateur'},
            {"label": 'Utilisateur', "rights": ["create-update-delete-programmations"], "slug": 'utilisateur'},
        ]

        for role in roles:
            role_create = RoleCreate(**role)
            try:
                role_model = RoleModel.create(role_create)
                role_model.refresh()

                rights = RightModel.query().filter(RightModel.slug.in_(role.get("rights", []))).all()

                role_model.rights_bdd.extend(rights)
                role_model.save_relations()

            except Exception as e:
                message = e.args[0]
                if "psycopg2.errors.UniqueViolation" in message:
                    print(f"duplicate role entry : {role['label']}")
                    continue
                else:
                    raise e
