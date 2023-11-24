from flask import Blueprint, render_template, session, request, redirect, url_for, flash, send_from_directory
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker
from git import Repo
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'sh'}
GIT_TOKEN = os.getenv('GIT_TOKEN')
GIT_USERNAME = os.getenv('GIT_USERNAME')
REPO_CLONE_PATH = os.getenv('REPO_CLONE_PATH')
SRC_YAML_PATH = "terraform.yaml"
TF_CLONE_PATH = f"{REPO_CLONE_PATH}AWS-TERRAFORM"
REPO_FILE = "bash create_repo.sh"
SCRIPT_FILE = "bash aws_secrets.sh"

aws = Blueprint('aws', __name__)

DB_URL = os.getenv('DB_URL')
engine=create_engine(f"{DB_URL}")
db=scoped_session(sessionmaker(bind=engine))

selectuser = "SELECT email FROM account WHERE email=:email"
selectid = "SELECT user_id FROM account WHERE email=:email"
in_aws_credential = "SELECT aws_id FROM aws WHERE aws_id=:awsid"
get_aws_credential = "SELECT accesskey,secretkey FROM aws WHERE aws_id=:aws_id"

@aws.route('/aws', methods=['GET', 'POST'])
def credential():
    if request.method=="POST":
        email = session.get('user_email')
        print("get email for aws credential : ", email)
        accesskey = request.form['accesskey']
        secretkey = request.form.get('secretkey')
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print("aws credential : ", emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create any resources","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(in_aws_credential), {"awsid":aws_user_id}).fetchone()
            
            if aws_id is None:
                put = "INSERT INTO aws(aws_id,accesskey,secretkey) VALUES(:aws_id,:accesskey,:secretkey)"
                db.execute(text(put),
                {"aws_id":aws_user_id, "accesskey":accesskey, "secretkey":secretkey})
                db.commit()
                flash("Your credentials added successfully", "success")
                return render_template("aws/aws_resource.html")
            else:
                flash("your credential alredy existed", "danger")
                return render_template("aws/aws_resource.html")
    return render_template('aws/aws_resource.html')

@aws.route('/aws/resources')
def resources():
    return render_template('aws/aws-iframe.html')

@aws.route('/aws/vpc', methods=['GET', 'POST'])
def vpc():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form.get('region')
        name = request.form.get('name')
        vpc_cidr = request.form.get('vpc_cidr')
        subnet_cidr = request.form.get('subnet_cidr')
        route_cidr = request.form.get('route_cidr')
        ingress_cidr = request.form.get('ingress_cidr')
        ig_p1 = request.form.get('ig_p1')
        ig_p2 = request.form.get('ig_p2')
        ig_p3 = request.form.get('ig_p3')
        ig_p4 = request.form.get('ig_p4')
        ingress_port = f"{ig_p1}{ig_p2}{ig_p3}{ig_p4}"
        user_cidr = request.form.get('user_cidr')
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create vpc resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            
                           # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/VPC/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"Name = {dq}{name}{dq}", '\n', 
                                              f"vpc_cidr = {dq}{vpc_cidr}{dq}", '\n', 
                                              f"subnet_cidr = {dq}{subnet_cidr}{dq}", '\n', 
                                              f"routetable_cidr = {dq}{route_cidr}{dq}", '\n', 
                                              f"ingress_cidr = {dq}{ingress_cidr}{dq}", '\n', 
                                              f"ingress_ports = {dq}{ingress_port}{dq}", '\n', 
                                              f"user_for_cidr = {dq}{user_cidr}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
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

    return render_template('aws/vpc.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@aws.route('/aws/ec2', methods=['GET', 'POST'])
def ec2():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        print(region)
        name = request.form['name']
        print(name)
        instance_type = request.form['instance_type']
        print(instance_type)
        subnet_id = request.form['subnet_id']
        print(subnet_id)
        ami_id = request.form['ami_id']
        print(ami_id)
        size = request.form['size']
        print(size)
        key_name = request.form['key_name']
        print(key_name)
        file = request.files['file']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create ec2 resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/EC2/*.tf {output_path}/')
                            # It stores the user uploaded file inside the cloned repository directory
                            if file and allowed_file(file.filename):
                                filename = secure_filename(file.filename)
                                file.save(f'{output_path}/' + filename)  # Set your upload path here
                                
                                if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                    # Stores user-entered values inside the Terraform.tfvars file
                                    tf_file = f"{output_path}/terraform.tfvars"
                                    with open(tf_file, 'w') as f:
                                        dq='"'
                                        values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                                  f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                                  f"region = {dq}{region}{dq}", '\n', 
                                                  f" = {dq}{name}{dq}", '\n', 
                                                  f"instance_type = {dq}{instance_type}{dq}", '\n', 
                                                  f"subnet_id = {dq}{subnet_id}{dq}", '\n', 
                                                  f"ami_id = {dq}{ami_id}{dq}", '\n', 
                                                  f"volume_size = {dq}{size}{dq}", '\n', 
                                                  f"key_name = {dq}{key_name}{dq}", '\n', 
                                                  f"user_data = {dq}{filename}{dq}"]
                                        print(values)
                                        f.writelines(values)
                                    repo = Repo(output_path)
                                    repo.git.add('.')
                                    repo.index.commit("added demo")
                                    origin = repo.remote(name='origin')
                                    origin.push()
                                    os.system(f'rm -rf {TF_CLONE_PATH}/')

                                    return redirect(url_for('aws.success'))
                                else:
                                    flash("We have five levels and your request were exit from the fifth level", "danger")
                                    print("An error occurred while executing the FILE UPLOAD step.")
                            else:
                                flash("We have five levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the EC2 FILES COPY step.")
                        else:
                            flash("We have five levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have five levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have five levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
    return render_template('aws/Ec2.html')

@aws.route('/aws/s3', methods=['GET', 'POST'])
def s3():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        acl = request.form['acl']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create s3 resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/S3/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"bucket = {dq}{name}{dq}", '\n', 
                                              f"acl = {dq}{acl}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the S3 FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('aws/S3.html')

@aws.route('/aws/rds', methods=['GET', 'POST'])
def rds():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        db_user = request.form['db_user']
        db_password = request.form['db_password']
        db_name = request.form['db_name']
        instance_class = request.form['instance_class']
        vpc_id = request.form['vpc_id']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create rds resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/RDS/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f" = {dq}{name}{dq}", '\n', 
                                              f"username = {dq}{db_user}{dq}", '\n', 
                                              f"password = {dq}{db_password}{dq}", '\n', 
                                              f"db_name = {dq}{db_name}{dq}", '\n', 
                                              f"instance_class = {dq}{instance_class}{dq}", '\n', 
                                              f"vpc_id = {dq}{vpc_id}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the RDS FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('aws/RDS.html')

@aws.route('/aws/eks', methods=['GET', 'POST'])
def eks():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        sunet_id = request.form['subnet_id']
        sg_id = request.form['sg_id']
        node_group = request.form['node_group']
        instance_type = request.form['instance_type']
        capasity = request.form['capasity']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create eks resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/EKS/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"cluster_name = {dq}{name}{dq}", '\n', 
                                              f"subnet_ids = {dq}{sunet_id}{dq}", '\n', 
                                              f"security_group_ids = {dq}{sg_id}{dq}", '\n', 
                                              f"node_group_name = {dq}{node_group}{dq}", '\n', 
                                              f"instance_types = {dq}{instance_type}{dq}", '\n', 
                                              f"desired_capacity = {capasity}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the EKS FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('aws/EKS.html')

@aws.route('/aws/ecr', methods=['GET', 'POST'])
def ecr():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        mutability = request.form['mutability']
        scan = request.form['scan']
        encryption = request.form['encryption']        
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create ecr resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/ECR/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"name = {dq}{name}{dq}", '\n', 
                                              f"image_tag_mutability = {dq}{mutability}{dq}", '\n', 
                                              f"scan_on_push = {dq}{scan}{dq}", '\n', 
                                              f"encryption_type = {dq}{encryption}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the ECR FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('aws/ECR_form.html')

@aws.route('/aws/cloudwatch', methods=['GET', 'POST'])
def cloudwatch():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        operator = request.form['operator']
        namespace = request.form['namespace']
        eval_perod1 = request.form['eval_perod1']
        eval_perod2 = request.form['eval_perod2']
        eval_perod = f'{eval_perod1}{eval_perod2}'
        matric_name = request.form['matric_name']
        threadshold1 = request.form['threadshold1']
        threadshold2 = request.form['threadshold2']
        threadshold = f'{threadshold1}{threadshold2}'
        period1 = request.form['period1']
        period2 = request.form['period2']
        period = f'{period1}{period2}'
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create cloudwatch resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/CLOUD-WATCH/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"alarm_name = {dq}{name}{dq}", '\n', 
                                              f"comparison_operator = {dq}{operator}{dq}", '\n', 
                                              f"namespace = {dq}{namespace}{dq}", '\n', 
                                              f"evaluation_periods = {eval_perod}", '\n', 
                                              f"metric_name = {dq}{matric_name}{dq}", '\n', 
                                              f"threshold = {threadshold}", '\n', 
                                              f"period = {period}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the CLOUD WATCH FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('aws/Cloud-watch.html')

@aws.route('/aws/dynamodb', methods=['GET', 'POST'])
def dynamodb():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        billing = request.form['billing']
        read1 = request.form['read1']
        read2 = request.form['read2']
        read = f'{read1}{read2}'
        write1 = request.form['write1']
        write2 = request.form['write2']
        write = f'{write1}{write2}'
        stream = request.form['stream']
        view = request.form['view']
        enable = request.form['enable']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create dynamodb resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/DYNAMODB/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"name = {dq}{name}{dq}", '\n', 
                                              f"billing_mode = {dq}{billing}{dq}", '\n', 
                                              f"read_capacity = {read}", '\n', 
                                              f"write_capacity = {write}", '\n', 
                                              f"stream_enabled = {stream}", '\n', 
                                              f"stream_view_type = {dq}{view}{dq}", '\n', 
                                              f"enabled = {enable}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the DYNAMODB FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('aws/dynamodb.html')

@aws.route('/aws/ecs_service', methods=['GET', 'POST'])
def ecs_service():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        cluster_name = request.form['cluster_name']
        family = request.form['family']
        cpu1 = request.form['cpu1']
        cpu2 = request.form['cpu2']
        cpu3 = request.form['cpu3']
        cpu4 = request.form['cpu4']
        cpu = f'{cpu1}{cpu2}{cpu3}{cpu4}'
        memory1 = request.form['memory1']
        memory2 = request.form['memory2']
        memory3 = request.form['memory3']
        memory4 = request.form['memory4']
        memory = f'{memory1}{memory2}{memory3}{memory4}'
        essential = request.form['essential']
        con_name = request.form['container_name']
        port1 = request.form['port1']
        port2 = request.form['port2']
        port3 = request.form['port3']
        port4 = request.form['port4']
        port = f'{port1}{port2}{port3}{port4}'
        subnet = request.form['subnet']
        sg = request.form['sg']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create ecs_service resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/ECS-SERVICE/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f" = {dq}{name}{dq}", '\n', 
                                              f"cluster = {dq}{cluster_name}{dq}", '\n', 
                                              f"family = {dq}{family}{dq}", '\n', 
                                              f"cpu = {cpu}", '\n', 
                                              f"memory = {memory}", '\n', 
                                              f"essential = {essential}", '\n', 
                                              f"container_name = {dq}{con_name}{dq}", '\n', 
                                              f"container_port = {dq}{port}{dq}", '\n', 
                                              f"subnets = [{dq}{subnet}{dq}]", '\n', 
                                              f"security_groups = [{dq}{sg}{dq}]"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the ECS SERVICE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
    return render_template('aws/Ecs-service.html')

@aws.route('/aws/ecs_cluster', methods=['GET', 'POST'])
def ecs_cluster():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        instance_type = request.form['instance_type']
        prefix = request.form['prefix']
        image_id = request.form['image_id']
        memory1 = request.form['memory1']
        memory2 = request.form['memory2']
        memory3 = request.form['memory3']
        memory4 = request.form['memory4']
        memory = f'{memory1}{memory2}{memory3}{memory4}'
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create ecs_cluster resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/ECS-Cluster/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"ecs_cluster_name = {dq}{name}{dq}", '\n', 
                                              f"instance_type = {dq}{instance_type}{dq}", '\n', 
                                              f"name_prefix = {dq}{prefix}{dq}", '\n', 
                                              f"image_id = {dq}{image_id}{dq}", '\n', 
                                              f"memory = {memory}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the ECS CLUSTER FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
    return render_template('aws/Ecs-Cluster.html')

@aws.route('/aws/api', methods=['GET', 'POST'])
def api():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        integration_method = request.form['integration_method']
        uri = request.form['uri']
        type = request.form['type']
        http_method = request.form['http_method']
        status1 = request.form['status1']
        status2 = request.form['status2']
        status3 = request.form['status3']
        #status4 = request.form['status4']
        status = f'{status1}{status2}{status3}'
        storage = request.form['storage']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create api resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/API-GATEWAY/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"name = {dq}{name}{dq}", '\n', 
                                              f"integration_http_method = {dq}{integration_method}{dq}", '\n', 
                                              f"uri = {dq}{uri}{dq}", '\n', 
                                              f"type = {dq}{type}{dq}", '\n', 
                                              f"http_method = {dq}{http_method}{dq}", '\n', 
                                              f"status_code = {status}", '\n', 
                                              f"stage_name = {dq}{storage}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the API FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
    return render_template('aws/Api.html')

@aws.route('/aws/Lambda', methods=['GET', 'POST'])
def Lambda():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        time1 = request.form['time1']
        time2 = request.form['time2']
        time3 = request.form['time3']
        time4 = request.form['time4']
        time = f'{time1}{time2}{time3}{time4}'
        memory1 = request.form['memory1']
        memory2 = request.form['memory2']
        memory3 = request.form['memory3']
        memory4 = request.form['memory4']
        memory = f'{memory1}{memory2}{memory3}{memory4}'
        publish = request.form['publish']
        file_name = request.form['file_name']
        vpc_id = request.form['vpc_id']
        protocol = request.form['protocol']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create Lambda resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Lambda/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"function_name = {dq}{name}{dq}", '\n', 
                                              f"timeout = {time}", '\n', 
                                              f"memory_size = {memory}", '\n', 
                                              f"publish = {publish}", '\n', 
                                              f"filename = {dq}{file_name}{dq}", '\n', 
                                              f"vpc_id = {dq}{vpc_id}{dq}", '\n', 
                                              f" = {dq}{protocol}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the LAMBDA FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
    return render_template('aws/Lambda.html')

@aws.route('/aws/sns', methods=['GET', 'POST'])
def sns():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        region = request.form['region']
        name = request.form['name']
        topic = request.form['topic']
        endpoint = request.form['endpoint']
        fifo = request.form['fifo']
        content = request.form['content']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create sns resource","danger")
                return redirect(url_for('login'))
        else:
            # Gets user id from database using email entered by user.
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            aws_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            aws_id = db.execute(text(get_aws_credential), {"aws_id":aws_user_id}).fetchone()
            if aws_id is None:
                flash("First you need to enter aws portal credentials", "danger")                
                return redirect(url_for('aws.credential'))
            else:
                accesskey = aws_id[0]
                secretkey = aws_id[1]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {accesskey} {secretkey}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/AWS-TERRAFORM.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/SNS/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                        # Stores user-entered values inside the Terraform.tfvars file
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"access_key = {dq}{accesskey}{dq}", '\n', 
                                              f"secret_key = {dq}{secretkey}{dq}", '\n', 
                                              f"region = {dq}{region}{dq}", '\n', 
                                              f"name = {dq}{name}{dq}", '\n', 
                                              f"topic_arn = {dq}{topic}{dq}", '\n', 
                                              f"endpoint = {dq}{endpoint}{dq}", '\n', 
                                              f"fifo_topic = {fifo}", '\n', 
                                              f"content_based_deduplication = {content}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}/')

                                return redirect(url_for('aws.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the SNS FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
    return render_template('aws/sns.html')


@aws.route('/success')
def success():
    return 'success'