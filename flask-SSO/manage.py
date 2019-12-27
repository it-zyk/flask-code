
from api import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cas import CAS

# 创建flask的应用对象
app = create_app("develop")
CAS(app)

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    app.run(debug=True)
