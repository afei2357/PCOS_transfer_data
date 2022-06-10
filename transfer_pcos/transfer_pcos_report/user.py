from app.models.models_user import *
from app import create_app

def main():
    Role.insert_roles()



if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()

