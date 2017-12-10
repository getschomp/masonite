import os
import sys
import shutil

def controller():
    if os.path.isfile('app/http/controllers/' + sys.argv[2] + '.py'):
        print '\033[95m' + sys.argv[2] + ' Controller Exists!' + '\033[0m'
    else:
        f = open('app/http/controllers/' + sys.argv[2] + '.py', 'w+')
        f.write("''' A Module Description '''\n")
        f.write('from app.http.providers.view import view\n\n')
        f.write('class ' + sys.argv[2] + '(object):\n')
        f.write("    ''' Class Docstring Description '''\n\n")
        f.write('    def __init__(self):\n')
        f.write('        pass\n')

        print '\033[92m' + sys.argv[2] + ' Created Successfully!' + '\033[0m'

def view():
    
    if os.path.isfile('resources/templates/' + sys.argv[2] + '.html'):
        print '\033[95m' + sys.argv[2] + ' View Exists!' + '\033[0m'
    else:
        f = open('resources/templates/' + sys.argv[2] + '.html', 'w+')
        print '\033[92m' + sys.argv[2] + ' View Created Successfully!' + '\033[0m'

def serve():
    from subprocess import call
    call(["gunicorn", "-w 1", "mine:app"])

def install():
    from subprocess import call
    call(["pip", "install", "-r", "requirements.txt"])

    # create the .env file if it does not exist

    if not os.path.isfile('.env'):
        shutil.copy('.env-example', '.env')

def model():
    if not os.path.isfile('app/' + sys.argv[2] + '.py'):
        f = open('app/' + sys.argv[2] + '.py', 'w+')

        f.write("''' A " + sys.argv[2] + " Database Module '''\n")
        f.write('from peewee import *\n')
        f.write('from config import database\n\n')
        f.write("db = database.engines['default']\n\n")
        f.write("class "+sys.argv[2]+"(Model):\n    ")
        f.write("# column = charField()\n\n")
        f.write("    class Meta:\n")
        f.write("        database = db\n\n")
        f.write("db.connect()\n")

        print '\033[92mModel Created Successfully!\033[0m'
    else:
        print '\033[95mModel Already Exists!\033[0m'

def migrate():
    import importlib
    
    from app.Migrations import Migrations
    
    module = importlib.import_module('databases.migrations')

    exists = False

    if not Migrations.table_exists():
        importlib.import_module('databases.migrations.automatic_migration_for_Migrations')
    for name in Migrations.select().where(Migrations.batch == 0):
        migration_name = name.migration[:-3]
        print migration_name
        importlib.import_module('databases.migrations.' + migration_name)
        print 'Migration Successful'
        exists = True

    if not exists:
        print 'No Migrations Exists'
    
def makemigration():
    from app.Migrations import Migrations
    f = open('databases/migrations/' + sys.argv[2] + '.py', 'w+')
    f.write("''' A Migration File '''\n")
    f.write('from playhouse.migrate import *\n')
    f.write('from config import database\n')
    f.write('from app.Migrations import Migrations\n')
    f.write('import os\n\n')
    f.write("engine = database.engines['default']\n")
    f.write("migrator = MySQLMigrator(engine)\n\n")
    f.write("class " + sys.argv[3] + "(Model):\n    ")
    f.write("pass\n\n")
    f.write("engine.create_table(" + sys.argv[3] + ", True)\n\n")
    f.write("migrate(\n    ")
    f.write("migrator.add_column('"+sys.argv[3]+"', 'column_name', CharField(default=255)),\n")
    f.write(')\n\n')
    f.write('query=Migrations.update(batch=1).where(\n')
    f.write('    Migrations.migration == os.path.basename(__file__))\n')
    f.write('query.execute()\n')
        
    Migrations.create(migration=sys.argv[2] + '.py')


    print '\033[92mMigration ' + sys.argv[2] + '.py Created Successfully!' + '\033[0m'

def startmigration():
    f = open('databases/migrations/automatic_migration_for_' + sys.argv[2] + '.py', 'w+')
    f.write("''' A Migration File '''\n")
    f.write('from playhouse.migrate import *\n')
    f.write('from app.' + sys.argv[2] + ' import ' + sys.argv[2] + '\n\n')
    f.write('from config import database\n\n')
    f.write("engine = database.engines['default']\n")
    f.write("migrator = MySQLMigrator(engine)\n\n")
    f.write("engine.drop_table(" + sys.argv[2] + ", True)\n")
    f.write("engine.create_table(" + sys.argv[2] + ", True)\n\n")

    print '\033[92mMigration ' + sys.argv[2] + '.py Created Successfully!' + '\033[0m'

def deploy():
    import subprocess
    from config import app
    output = subprocess.Popen(['heroku', 'git:remote', '-a', app.name.lower()], stdout=subprocess.PIPE).communicate()[0]
    if not output:
        create_app = raw_input(
            "App doesn't exist, would you like to craft one? [y/n]: ")  # Python 2
        if 'y' in create_app:
            subprocess.call(['heroku', 'create', app.name.lower()])
            subprocess.call(['python', 'craft', 'deploy'])
    else:
        subprocess.call(['git', 'push', 'heroku', 'master'])
