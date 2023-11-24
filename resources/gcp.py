from flask import Blueprint, render_template, session, request, redirect, url_for, flash, send_from_directory
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker
from git import Repo
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'sh', 'json'}
GIT_TOKEN = os.getenv('GIT_TOKEN')
GIT_USERNAME = os.getenv('GIT_USERNAME')
REPO_CLONE_PATH = os.getenv('REPO_CLONE_PATH')
SRC_YAML_PATH = "terraform.yaml"
TF_CLONE_PATH = f"{REPO_CLONE_PATH}GCP-Terraform"
REPO_FILE = "bash create_repo.sh"
SCRIPT_FILE = "bash gcp_secrets.sh"

gcp = Blueprint('gcp', __name__)


DB_URL = os.getenv('DB_URL')
engine=create_engine(f"{DB_URL}")
db=scoped_session(sessionmaker(bind=engine))

selectuser = "SELECT email FROM account WHERE email=:email"
selectid = "SELECT user_id FROM account WHERE email=:email"
in_gcp_credential = "SELECT gcp_id FROM gcp WHERE gcp_id=:gcpid"
get_gcp_credential = "SELECT project_id,credentials FROM gcp WHERE gcp_id=:gcp_id"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

########################################################
###                    CREDENTIALS                  ####
########################################################
@gcp.route('/gcp', methods=['GET', 'POST'])
def credential():
    if request.method=="POST":
        email = session.get('user_email')
        print("get email for gcp credential", email)
        project_id = request.form['project_id']
        file = request.files['credentials']
        print(file)
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print("gcp credential : ", emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create any resources","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(in_gcp_credential), {"gcpid":gcp_user_id}).fetchone()
            
            if gcp_id is None:
                if file and allowed_file(file.filename):    # Stores user-entered values inside the Terraform.tfvars file                        
                    filename = secure_filename(file.filename)
                    print(filename)
                    file.save(f'{REPO_CLONE_PATH}gcp_credential/' + filename)  # Set your upload path here
                
                put = "INSERT INTO gcp(gcp_id,project_id,credentials) VALUES(:gcp_id,:project_id,:credentials)"
                db.execute(text(put),
                {"gcp_id":gcp_user_id, "project_id":project_id, "credentials":filename})
                db.commit()
                flash("Your credentials added successfully", "success")
                return render_template("gcp/gcp_resources.html")
            else:
                flash("your credential alredy existed", "danger")
                return render_template("gcp/gcp_resources.html")
    return render_template('gcp/gcp_resources.html')

########################################################
###                         IFRAME                  ####
########################################################
@gcp.route('/gcp/resources')
def resources():
    return render_template('gcp/Google-frame.html')

########################################################
###                         VPC                     ####
########################################################
@gcp.route('/gcp/vpc', methods=['GET', 'POST'])
def vpc():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        route_mode = request.form['radio']
        subnet_name = request.form['subnet_name']
        cidr = request.form['cidr']
        range = request.form['range']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create vpc resources","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/VPC-NETWORK/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                
                                with open(file, 'w') as f:
                                    dq = '"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"vpc-name = {dq}{name}{dq}", '\n', 
                                              f"routing-mode = {dq}{route_mode}{dq}", '\n', 
                                              f"subnet-name = {dq}{subnet_name}{dq}", '\n', 
                                              f"subnet-cidr = {dq}{cidr}{dq}", '\n', 
                                              f"dest-range = {dq}{range}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the VPC FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/gcp_vpc.html')

########################################################
###                     CLOUD RUN                   ####
########################################################
@gcp.route('/gcp/cloudrun', methods=['GET', 'POST'])
def cloudrun():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        img_name = request.form['img_name']
        port1 = request.form['port1']
        port2 = request.form['port2']
        port3 = request.form['port3']
        port4 = request.form['port4']
        port5 = request.form['port5']
        port = f'{port1}{port2}{port3}{port4}{port5}'
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create cloudrun resources","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/CLOUD-RUN/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq = '"'
                                    values = [f"project = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"service-name = {dq}{name}{dq}", '\n', 
                                              f"image-name = {dq}{img_name}{dq}", '\n', 
                                              f"port = {dq}{port}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the CLOUD RUN FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/CloudRun.html')

########################################################
###                  COMPUTE ENGINE                 ####
########################################################

@gcp.route('/gcp/ComputeEngine', methods=['GET', 'POST'])
def ComputeEngine():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        machine_type = request.form['machine_type']
        disk_img = request.form['disk_img']
        size = request.form['size']
        file = request.files['file']
        svcemail = request.form['svcemail']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create ComputeEngine resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Compute-Engine/*.tf {output_path}/')
                            
                            if file and allowed_file(file.filename):    # Stores user-entered values inside the Terraform.tfvars file                        
                                filename = secure_filename(file.filename)
                                print(filename)
                                file.save(f'{output_path}/' + filename)  # Set your upload path here
                                
                                if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                        
                                    tf_file = f"{output_path}/terraform.tfvars"
                                    with open(tf_file, 'w') as f:
                                        dq='"'
                                        values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                                 f"credential = {dq}{credential}{dq}", '\n', 
                                                 f"region = {dq}{region}{dq}", '\n', 
                                                 f"zone = {dq}{zone}{dq}", '\n', 
                                                 f"instance-name = {dq}{name}{dq}", '\n', 
                                                 f"machine-type = {dq}{machine_type}{dq}", '\n', 
                                                 f"image-name = {dq}{disk_img}{dq}", '\n', 
                                                 f"size = {dq}{size}{dq}", '\n', 
                                                 f"startup-script = {dq}{filename}{dq}", '\n', 
                                                 f"email = {dq}{svcemail}{dq}"]
                                        print(values)
                                        f.writelines(values)
                                    repo = Repo(output_path)
                                    repo.git.add('.')
                                    repo.index.commit("added demo")
                                    origin = repo.remote(name='origin')
                                    origin.push()
                                    os.system(f'rm -rf {TF_CLONE_PATH}')
                                    
                                    return redirect(url_for('gcp.success'))
                                else:
                                    flash("We have five levels and your request were exit from the fifth level", "danger")
                                    print(f"An error occurred while executing the COMPUTE ENGINE FILE UPLOAD step.")
                            else:
                                flash("We have five levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the FILES COPY step.")
                        else:
                            flash("We have five levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have five levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have five levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
    return render_template('gcp/ComputeEngine.html')

########################################################
###                      CLOUD RUN                  ####
########################################################
@gcp.route('/gcp/CloudSql', methods=['GET', 'POST'])
def CloudSql():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        version = request.form['version']
        tire = request.form['tire']
        username = request.form['username']
        password = request.form['password']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create CloudSql resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Cloud-Sql/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"sql-database-instance-name = {dq}{name}{dq}", '\n', 
                                              f"database-version = {dq}{version}{dq}", '\n', 
                                              f"tier = {dq}{tire}{dq}", '\n', 
                                              f"sql-user-name = {dq}{username}{dq}", '\n', 
                                              f"sql-password = {dq}{password}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the CLOUD RUN FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/CloudSql.html')

########################################################
###                  CLOUD STORAGE                  ####
########################################################
@gcp.route('/gcp/CloudStorage', methods=['GET', 'POST'])
def CloudStorage():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        storage_class = request.form['storage_class']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create CloudStorage resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/ClOUD-STORAGE/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"bucket-name = {dq}{name}{dq}", '\n', 
                                              f"storage-class = {dq}{storage_class}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/Cloud-storage.html')

########################################################
###                         GKE                     ####
########################################################
@gcp.route('/gcp/gke', methods=['GET', 'POST'])
def gke():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        network = request.form['network']
        subnet = request.form['subnet']
        count1 = request.form['count1']
        count2 = request.form['count2']
        count = f'{count1}{count2}'
        node_pool = request.form['node_pool']
        machine_type = request.form['machine_type']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create gke resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/GKE-CLUSTER/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"cluster-name = {dq}{name}{dq}", '\n', 
                                              f"network = {dq}{network}{dq}", '\n', 
                                              f"subnetwork = {dq}{subnet}{dq}", '\n', 
                                              f"node-count = {count}", '\n', 
                                              f"node-pool-name = {dq}{node_pool}{dq}", '\n', 
                                              f"machine-type = {dq}{machine_type}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the GKE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/kuber.html')

########################################################
###                     APP ENGINE                  ####
########################################################
@gcp.route('/gcp/AppEngine', methods=['GET', 'POST'])
def AppEngine():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        runtime = request.form['runtime']
        shell = request.form['shell']
        source = request.form['source']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create AppEngine resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/APP-ENGINE/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"service = {dq}{name}{dq}", '\n', 
                                              f"runtime = {dq}{runtime}{dq}", '\n', 
                                              f"shell = {dq}{shell}{dq}", '\n', 
                                              f"zip-source-url = {dq}{source}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the APP ENGINE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/AppEngine.html')

########################################################
###                   CLOUD FUNCTION                ####
########################################################
@gcp.route('/gcp/CloudFunction', methods=['GET', 'POST'])
def CloudFunction():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        mbsize = request.form['mbsize']
        object = request.form['object']
        bucket_name = request.form['bucket_name']
        runtime = request.form['runtime']
        point = request.form['point']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create CloudFunction resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/GCP-Cloud-Function/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f" = {dq}{project_id}{dq}", '\n', 
                                              f" = {dq}{credential}{dq}", '\n', 
                                              f" = {dq}{region}{dq}", '\n', 
                                              f" = {dq}{zone}{dq}", '\n', 
                                              f" = {dq}{name}{dq}", '\n',
                                              f" = {mbsize}", '\n', 
                                              f" = {dq}{object}{dq}", '\n', 
                                              f" = {dq}{bucket_name}{dq}", '\n', 
                                              f" = {dq}{runtime}{dq}", '\n', 
                                              f" = {dq}{point}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the CLOUD FUNCTION FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/CloudFunction.html')

########################################################
###                       BIGQUERY                  ####
########################################################
@gcp.route('/gcp/BigQuery', methods=['GET', 'POST'])
def BigQuery():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        dataset = request.form['dataset']
        table_id = request.form['table_id']
        time = request.form['time']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create BigQuery resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/BigQuery/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"friendly-name = {dq}{name}{dq}", '\n', 
                                              f"dataset-id = {dq}{dataset}{dq}", '\n', 
                                              f"table-id = {dq}{table_id}{dq}", '\n', 
                                              f"time-partitioning-type = {dq}{time}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the BIGQUERY FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/big.html')

########################################################
###                  ARTIFACT REGISTRY              ####
########################################################
@gcp.route('/gcp/ArtifactRegistry', methods=['GET', 'POST'])
def ArtifactRegistry():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        format = request.form['format']
        mode = request.form['mode']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create ArtifactRegistry resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Artifact-Registry/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credentila = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"repository-id = {dq}{name}{dq}", '\n', 
                                              f"format = {dq}{format}{dq}", '\n', 
                                              f" = {dq}{mode}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the ARTIFACT REGISTRY FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('gcp/Artifact.html')

########################################################
###                   CLOUD SPANNER                 ####
########################################################
@gcp.route('/gcp/CloudSpanner', methods=['GET', 'POST'])
def CloudSpanner():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        db_name = request.form['db_name']
        config = request.form['config']
        db_dialect = request.form['db_dialect']
        node1 = request.form['node1']
        node2 = request.form['node2']
        node = f'{node1}{node2}'
        version = request.form['version']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create CloudSpanner resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Cloud-Spanner/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"spanner-name = {dq}{name}{dq}", '\n', 
                                              f"database-name = {dq}{db_name}{dq}", '\n', 
                                              f"config = {dq}{config}{dq}", '\n', 
                                              f"database-dialect = {dq}{db_dialect}{dq}", '\n', 
                                              f"num-nodes = {node}", '\n', 
                                              f" = {dq}{version}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the CLOUD SPANNER FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
    
    return render_template('gcp/spanner.html')

########################################################
###                      VM WARE                    ####
########################################################
@gcp.route('/gcp/vmware', methods=['GET', 'POST'])
def vmware():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        machine_type = request.form['machine_type']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create vmware resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/vmWare/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"vmware-instance-name = {dq}{name}{dq}", '\n', 
                                              f"machine-type = {dq}{machine_type}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the VM WARE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
    
    return render_template('gcp/vm-ware.html')

########################################################
###                  STORAGE TRANSFER               ####
########################################################
@gcp.route('/gcp/storagetransfer', methods=['GET', 'POST'])
def storagetransfer():
    if request.method=="POST":
        email = session.get('user_email')
        region = request.form['region']
        zone = request.form['zone']
        name = request.form['name']
        src_name = request.form['src_name']
        dest_name = request.form['dest_name']
        obj_delete1 = request.form['radio']
        obj_delete2 = request.form['radio']
        obj_delete = f'{obj_delete1}{obj_delete2}'
        sink_delete1 = request.form['sink']
        sink_delete2 = request.form['sink']
        sink_delete = f'{sink_delete1}{sink_delete2}'
        duration = request.form['duration']
        
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create storagetransfer resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            gcp_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            gcp_id = db.execute(text(get_gcp_credential), {"gcp_id":gcp_user_id}).fetchone()
            if gcp_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('gcp.credential'))
            else:
                project_id = gcp_id[0]
                credential = gcp_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {project_id} {credential}')
                    # Check the exit code to determine if the script executed successfully
                    if create_secret == 0:
                        print(f"{reponame} Secrets created successfully!")
                        repo_url = f'https://{GIT_TOKEN}@github.com/{GIT_USERNAME}/{reponame}.git'
                        # REPOSITORY CLONE PATH
                        output_path = f'{REPO_CLONE_PATH}{reponame}'                        
                        Repo.clone_from(repo_url, output_path)
                        #TO CHECK WHETHER THE CREATED REPOSITORY EXISTS OR NOT
                        list_path = os.system(f'ls {output_path}')
                        if list_path == 0:
                            print(f"{reponame} folder is there")
                            os.system(f'rm -rf {TF_CLONE_PATH}')
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/GCP-Terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # COPYING THE JSON FILE FOR THE USER CREDENTIAL IN GCP
                            credential_file = os.system(f'cp {REPO_CLONE_PATH}/gcp_credential/{credential} {output_path}/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Storage-Transfer/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and credential_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                filter_date = duration.split("-")
                                year = filter_date[0]
                                month = filter_date[1]
                                date = filter_date[2]
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"project-id = {dq}{project_id}{dq}", '\n', 
                                              f"credential = {dq}{credential}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"zone = {dq}{zone}{dq}", '\n', 
                                              f"source-bucket-name = {dq}{src_name}{dq}", '\n', 
                                              f"destination-bucket-name = {dq}{dest_name}{dq}", '\n', 
                                              f"source-object-delete = {obj_delete}", '\n', 
                                              f"sink-object-overwrite = {sink_delete}", '\n', 
                                              f"day = {year}", '\n', 
                                              f"month = {month}", '\n', 
                                              f"year = {date}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('gcp.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the STORAGE TRANSFER FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
    
    return render_template('gcp/storage.html')


########################################################
###                   SUCCESS MESSAGE               ####
########################################################
@gcp.route('/success')
def success():
    return 'success'
