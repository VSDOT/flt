from flask import Blueprint, render_template, session,request, redirect, url_for, flash, send_from_directory
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker
from git import Repo
import os
from werkzeug.utils import secure_filename

GIT_TOKEN = os.getenv('GIT_TOKEN')
GIT_USERNAME = os.getenv('GIT_USERNAME')
REPO_CLONE_PATH = os.getenv('REPO_CLONE_PATH')
SRC_YAML_PATH = "terraform.yaml"
TF_CLONE_PATH = f"{REPO_CLONE_PATH}Azure-terraform"
REPO_FILE = "bash create_repo.sh"
SCRIPT_FILE = "bash azure_secrets.sh"

azure = Blueprint('azure', __name__)

DB_URL = os.getenv('DB_URL')
engine=create_engine(f"{DB_URL}")
db=scoped_session(sessionmaker(bind=engine))

selectuser = "SELECT email FROM account WHERE email=:email"
selectid = "SELECT user_id FROM account WHERE email=:email"
in_azure_credential = "SELECT azure_id FROM azure WHERE azure_id=:azureid"
get_azure_credential = "SELECT subscription_id,tenent_id,client_id,client_secret FROM azure WHERE azure_id=:azure_id"

####################### CREDENTIAL PAGE START ############################
@azure.route('/azure', methods=['GET', 'POST'])
def credential():
    if request.method=="POST":
        email = session.get('user_email')
        print("get email for azure credential", email)
        subscription_id = request.form['sub_id']
        tenant_id = request.form.get('ten_id')
        client_id = request.form['cli_id']
        client_secret = request.form.get('cli_sec')
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print("azure credential : ", emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create any resources","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            
            azure_id = db.execute(text(in_azure_credential), {"azureid":azure_user_id}).fetchone()
            
            if azure_id is None:
                put = "INSERT INTO azure(azure_id,subscription_id,tenent_id,client_id,client_secret) VALUES(:azure_id,:subscription_id,:tenent_id,:client_id,:client_secret)"
                db.execute(text(put),
                {"azure_id":azure_user_id, "subscription_id":subscription_id, "tenent_id":tenant_id, "client_id":client_id, "client_secret":client_secret})
                db.commit()
                flash("Your credentials added successfully", "success")
                return render_template("azure/azure_resources.html")
            else:
                flash("your credential alredy existed", "danger")
                return render_template("azure/azure_resources.html")
    return render_template('azure/azure_resources.html')

########################################################
###                   RESOURCE GROUP                ####
########################################################

@azure.route('/resource_group', methods=['GET', 'POST'])
def resource_group():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        r_name = request.form.get('resource_group_name')
        location = request.form.get('location')
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create resource_group","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = r_name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/RESOURCE_GROUP/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_name = {dq}{r_name}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}"]
                                    print(values)
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the RESOURCE GROUP FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

    return render_template('azure/azure_resources.html')

########################################################
###                        IFRAME                   ####
########################################################

@azure.route('/azure/resources')
def resources():
    return render_template('azure/Frame.html')

########################################################
###                      STORAGE BLOB               ####
########################################################
@azure.route('/azure/blob', methods=['GET', 'POST'])
def blob():
    if request.method=="POST":
        email = session.get('user_email')
        print("get email for azure credential", email)
        resource_group_id = request.form['rgi']
        account_tire = request.form['att']
        location = request.form['location']
        art = request.form['art']
        name = request.form['san']
        cat = request.form['anyone']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create blob resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/STORAGE_BLOB/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    values = [key_subscription, '\n', key_tenent, '\n', key_client, '\n', key_client_sec, '\n',
                                            resource_group_id, '\n', account_tire, '\n', location, '\n', art, '\n', name, '\n', cat]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the STORAGE BLOB FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/Storage_blob.html')

########################################################
###                   VIRTUAL MACHINE               ####
########################################################

@azure.route('/azure/vm', methods=['GET', 'POST'])
def vm():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        vnet_id = request.form['vnet_id']
        name = request.form['name']
        size = request.form['size']
        username = request.form['username']
        storage_type = request.form['storage_type']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create vm resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/VM/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq = '"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"virtual_network_id = {dq}{vnet_id}{dq}", '\n', 
                                              f"virtual_machine_name = {dq}{name}{dq}", '\n', 
                                              f"size = {dq}{size}{dq}", '\n', 
                                              f"admin_username = {dq}{username}{dq}", '\n', 
                                              f"storage_type = {dq}{storage_type}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the VIRTUAL MACHINE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/Virtual.html')

########################################################
###                   VIRTUAL NETWORK               ####
########################################################

@azure.route('/azure/vnet', methods=['GET', 'POST'])
def vnet():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        prefix = request.form['prefix']
        allowssh = request.form['allowssh']
        src_prefix = request.form['src_prefix']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create vnet resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Vnet/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"virtual_network_name = {dq}{name}{dq}", '\n', 
                                              f"address_prefixes = [{dq}{prefix}{dq}]", '\n', 
                                              f"allow_ssh_ip = {dq}{allowssh}{dq}", '\n', 
                                              f"source_address_prefix_value = {dq}{src_prefix}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the VNET FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/V_Net.html')

########################################################
###                 CONTAINER REGISTERY             ####
########################################################

@azure.route('/azure/containerregistery', methods=['GET', 'POST'])
def containerregistery():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        unit = request.form['unit']
        admin = request.form['admin']
        zone_redundancy = request.form['zone']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create containerregistery resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Container_Registry/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"container_name = {dq}{name}{dq}", '\n', 
                                              f"sku = {dq}{unit}{dq}", '\n', 
                                              f"admin_enabled = {admin}", '\n', 
                                              f"zone_redundancy_enabled = {zone_redundancy}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the CONTAINER REGISTERY FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/C_Registery.html')

########################################################
###                        AKS                      ####
########################################################

@azure.route('/azure/aks', methods=['GET', 'POST'])
def aks():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        vm_size = request.form['vm_size']
        disk_size = request.form['disk_size']
        max_count = request.form['count']
        vnet_id = request.form['vnet_id']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create aks resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/AZURE-AKS/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id  = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"kubernetes_cluster_name = {dq}{name}{dq}", '\n', 
                                              f"vm_size = {dq}{vm_size}{dq}", '\n', 
                                              f"disk_gb_size = {disk_size}", '\n', 
                                              f"max_count = {max_count}", '\n', 
                                              f"vnet_id = {dq}{vnet_id}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the AKS FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/AKS.html')

########################################################
###                 CONTAINER INSTANCE              ####
########################################################

@azure.route('/azure/containerinstance', methods=['GET', 'POST'])
def containerinstance():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        ip_type = request.form['ip_type']
        os_type = request.form['os_type']
        image_name = request.form['image_name']
        cpu_count = request.form['cpu_count']
        memory_size = request.form['memory_size']
        port = request.form['port']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create containerinstance resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Container_Instance/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"container_name = {dq}{name}{dq}", '\n', 
                                              f"ip_address_type = {dq}{ip_type}{dq}", '\n', 
                                              f"os_type = {dq}{os_type}{dq}", '\n', 
                                              f"image_name = {dq}{image_name}{dq}", '\n', 
                                              f"cpu_count = {dq}{cpu_count}{dq}", '\n', 
                                              f"memory_size = {dq}{memory_size}{dq}", '\n', 
                                              f"port = {port}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')

                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the CONTAINER INSTANCE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/C_Instance.html')

########################################################
###                     APP SERVICE                 ####
########################################################

@azure.route('/azure/appservice', methods=['GET', 'POST'])
def appservice():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        os_type = request.form['os_type']
        tire_type = request.form['tire_type']
        storage_type = request.form['storage_type']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create appservice resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/App_Service/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"app_service_plan_name = {dq}{name}{dq}", '\n', 
                                              f"os_type = {dq}{os_type}{dq}", '\n', 
                                              f"tier_type = {dq}{tire_type}{dq}", '\n', 
                                              f"storage_type = {dq}{storage_type}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')

                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the APP SERVICE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/App-ser.html')

########################################################
###                    DATA FACTORY                 ####
########################################################

@azure.route('/azure/datafactory', methods=['GET', 'POST'])
def datafactory():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        repository_url = request.form['repository_url']
        branch_name = request.form['branch_name']
        root_folder = request.form['root_folder']
        access_token = request.form['access_token']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create datafactory resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/Data_Factory/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"data_foctory_name = {dq}{name}{dq}", '\n', 
                                              f"repository_url = {dq}{repository_url}{dq}", '\n', 
                                              f"branch_name = {dq}{branch_name}{dq}", '\n', 
                                              f"root_floder_path = {dq}{root_folder}{dq}", '\n', 
                                              f"access_token_key = {dq}{access_token}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')

                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the DATA FACTORY FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/Data.html')

########################################################
###                      SQL SERVER                 ####
########################################################

@azure.route('/azure/SQLserver', methods=['GET', 'POST'])
def SQLserver():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        #repository_url = request.form['repository_url']
        admin_name = request.form['admin_name']
        admin_password = request.form['admin_password']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create SQLserver resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/SQL_SERVER/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"sql_server_name = {dq}{name}{dq}", '\n', 
                                              f"administrator_login_name = {dq}{admin_name}{dq}", '\n', 
                                              f"administrator_login_password = {dq}{admin_password}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')

                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the SQL SERVER FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                        
    return render_template('azure/Server.html')

########################################################
###                   ELASTIC POLL                  ####
########################################################

@azure.route('/azure/elasticpoll', methods=['GET', 'POST'])
def elasticpoll():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        sql_id = request.form['sql_id']
        storage_type = request.form['storage_type']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create elasticpoll resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/SQL_Elastic_Pool/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"elasticpool_name = {dq}{name}{dq}", '\n', 
                                              f"sql_server_id = {dq}{sql_id}{dq}", '\n', 
                                              f"storage_type = {dq}{storage_type}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')

                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the ELASTIC POLL FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                   
    return render_template('azure/Elastic.html')

########################################################
###                   FUNCTION APP                  ####
########################################################

@azure.route('/azure/functionapp', methods=['GET', 'POST'])
def functionapp():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        resource_group_id = request.form['rid']
        location = request.form['location']
        name = request.form['name']
        account_tire = request.form['account_tire']
        #account_replication = request.form['account_replication']
        language = request.form['language']
        version = request.form['version']
        type = request.form['type']
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create functionapp resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = name
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/FUNCTION_APP/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{resource_group_id}{dq}", '\n', 
                                              f"location = {dq}{location}{dq}", '\n', 
                                              f"function_app_name = {dq}{name}{dq}", '\n', 
                                              f"account_tier = {dq}{account_tire}{dq}", '\n', 
                                              f"language = {dq}{language}{dq}", '\n', 
                                              f"version = {dq}{version}{dq}", '\n', 
                                              f"account_replication_type = {dq}{type}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')

                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the FUNCTION APP FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")
        
                   
    return render_template('azure/Fun-app.html')

########################################################
###                   SQL DATABASE                  ####
########################################################

@azure.route('/azure/sqldb', methods=['GET', 'POST'])
def sqldb():
    if request.method=="POST":
        email = session.get('user_email')
        print(email)
        rg_id = request.form['rid']
        loc = request.form.get('location')
        dbname = request.form['dbname']
        server_id = request.form['serv_id']
        gb_size = request.form.get('size')
        att = request.form.get('att')
        # Checks whether the email entered by the user is present and if it is then executes the else part else executes the if condition
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        print(emaildata)
        if emaildata is None:
                flash("First you need to login and then you will create sqldb resource","danger")
                return redirect(url_for('login'))
        else:
            # Retrieves the user id from the database using the email entered by the user. If id is present the if condition will run otherwise the else part will run
            iddata = db.execute(text(selectid), {"email":email}).fetchone()
            azure_user_id = iddata[0]
            # Runs the if condition if the user id is not in aws_id , runs the else part if the user id is in aws_id
            azure_id = db.execute(text(get_azure_credential), {"azure_id":azure_user_id}).fetchone()
            if azure_id is None:
                flash("First you need to enter azure portal credentials", "danger")                
                return redirect(url_for('azure.credential'))
            else:
                key_subscription = azure_id[0]
                key_tenent = azure_id[1]
                key_client = azure_id[2]
                key_client_sec = azure_id[3]
                reponame = dbname
                
                # Use os.system to execute the shell script
                create_repo = os.system(f'{REPO_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame}')
                # Check the exit code to determine if the script executed successfully
                if create_repo == 0:
                    print(f"{reponame} Repository created successfully!")
                    
                    # Use os.system to execute the shell script
                    create_secret = os.system(f'{SCRIPT_FILE} {GIT_USERNAME} {GIT_TOKEN} {reponame} {key_subscription} {key_tenent} {key_client} {key_client_sec}')
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
                            tf_repo_url = f"https://{GIT_TOKEN}@github.com/cloudgarage-perambalur/Azure-terraform.git"
                            
                            Repo.clone_from(tf_repo_url, TF_CLONE_PATH)
                            # GITHUB CREATES A DIRECTORY FOR THE WORKFLOW
                            gh_workflow = os.system(f'cd {output_path} && mkdir -p ./.github/workflows')
                            # COPYING THE YAML FILE FOR THE GITHUB WORKFLOW
                            workflow_file = os.system(f'cp {SRC_YAML_PATH} {output_path}/.github/workflows/')
                            # TERRAFORM COPIES THE FILES FROM THE LOCAL DIRECTORY TO THE GIT CLONED DIRECTORY
                            tf_files = os.system(f'cp {TF_CLONE_PATH}/SQL_Database/*.tf {output_path}/')
                            if gh_workflow == 0 and workflow_file == 0 and tf_files == 0:
                                # Stores user-entered values inside the Terraform.tfvars file                        
                                file = f"{output_path}/terraform.tfvars"
                                with open(file, 'w') as f:
                                    dq='"'
                                    values = [f"subscription_id = {dq}{key_subscription}{dq}", '\n', 
                                              f"tenant_id = {dq}{key_tenent}{dq}", '\n', 
                                              f"client_id = {dq}{key_client}{dq}", '\n', 
                                              f"client_secret = {dq}{key_client_sec}{dq}", '\n', 
                                              f"resource_group_id = {dq}{rg_id}{dq}", '\n', 
                                              f"location = {dq}{loc}{dq}", '\n', 
                                              f"sql_database_name = {dq}{dbname}{dq}", '\n', 
                                              f"sql_server_id = {dq}{server_id}{dq}", '\n', 
                                              f"gb_size = {dq}{gb_size}{dq}", '\n', 
                                              f"account_tier_type = {dq}{att}{dq}"]
                                    f.writelines(values)
                                repo = Repo(output_path)
                                repo.git.add('.')
                                repo.index.commit("added demo")
                                origin = repo.remote(name='origin')
                                origin.push()
                                os.system(f'rm -rf {TF_CLONE_PATH}')
                                
                                return redirect(url_for('azure.success'))
                            else:
                                flash("We have three levels and your request were exit from the fourth level", "danger")
                                print("An error occurred while executing the SQL DATABASE FILES COPY step.")
                        else:
                            flash("We have three levels and your request were exit from the third level", "danger")
                            print(f"An error occurred while executing the REPOSITORY CLONE step. Exit code: {list_path}")
                    else:
                        flash("We have three levels and your request were exit from the second level", "danger")
                        print(f"An error occurred while executing the SECRET script. Exit code: {create_secret}")
                    
                else:
                    flash("We have three levels and your request were exit from the first level REPO NAME EXISTED", "danger")
                    print(f"An error occurred while executing the REPOSITORY script. Exit code: {create_repo}")

        
        
    return render_template('azure/SqlDataBase.html')

########################################################
###                   SUCCESS MESSAGE               ####
########################################################

@azure.route('/success')
def success():
    return 'success'