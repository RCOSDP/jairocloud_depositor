from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint, json
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager
from depositor_models.affiliation_repository import Affiliation_Repository, Affiliation_Repository_manager
from depositor_login.views import index_login

blueprint = Blueprint(
    "admin_setting",
    __name__,
    url_prefix="/admin_setting",
    template_folder="templates",
    static_folder="static")

@blueprint.route("/", methods=['GET', 'POST'])
def index_affili():
    if not current_user.is_authenticated:
        return redirect(url_for('login.index_login'))
    if request.method == "POST":
        try:
            affiliation_name = request.json.get("affiliation_name")
            repository_url = request.json.get("repository_url")
            access_token = request.json.get("access_token")
            if all([affiliation_name,repository_url,access_token]):
                if current_user.role == "管理者":
                    affiliation_id_info = Affiliation_Id_manager.get_affiliation_id_by_id(affiliation_name)
                else:
                    affiliation_id_info = Affiliation_Id_manager.get_affiliation_id_by_affiliation_name(affiliation_name)
                affiliation_repository_info = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(affiliation_id_info.id)
                if affiliation_repository_info:
                        aff_repository = {"id":affiliation_repository_info.id,
                                        "affiliation_id":affiliation_id_info.id,
                                        "repository_url":repository_url,
                                        "access_token":access_token}
                        Affiliation_Repository_manager.upt_aff_repository(aff_repository)
                        return jsonify(success=True),200
                else:
                        aff_repository = Affiliation_Repository(affiliation_id=affiliation_id_info.id, repository_url=repository_url, access_token=access_token)
                        Affiliation_Repository_manager.create_aff_repository(aff_repository)
                        return jsonify(success=True),200
            else:
                current_app.logger.error(
                        'ERROR affliation settings: settings is not exist.')
                return jsonify(success=False),400
        except Exception as e:
                current_app.logger.error(
                    'ERROR affliation settings: {}'.format(e))
                return jsonify(success=False),400
    else:
        role = current_user.role
        try:
            if role == "図書館員" or role == "管理者":
                repository_url = ""
                access_token = ""
                if role == "管理者":
                    affiliation_name = "default"
                    affiliation_id_info = Affiliation_Id_manager.get_affiliation_id_by_affiliation_name(affiliation_name)
                    affiliation_repository_info = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(affiliation_id_info.id)
                else:
                    affiliation_id_info = Affiliation_Id_manager.get_affiliation_id_by_id(current_user.affiliation_id)
                    affiliation_name = affiliation_id_info.affiliation_name
                    affiliation_repository_info = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(affiliation_id_info.id)
                repository_url = affiliation_repository_info.repository_url
                access_token = affiliation_repository_info.access_token
                affiliation_id_list = Affiliation_Id_manager.get_affiliation_id_list()
                affiliation_repository_list = Affiliation_Repository_manager.get_affiliation_repository_list()
                aff_repository_dict = {}
                for affiliation_repository in affiliation_repository_list:
                    aff_repository_dict[affiliation_repository.affiliation_id] = {"repository_url":affiliation_repository.repository_url, "access_token":affiliation_repository.access_token}
                form = FlaskForm(request.form)
                return render_template("admin_setting/affi_index.html",
                                    form = form,
                                    affiliation_id_list = affiliation_id_list,
                                    aff_repository_dict = json.dumps(aff_repository_dict),
                                    affiliation_name = affiliation_name,
                                    repository_url = repository_url,
                                    access_token = access_token)
            else:
                form = FlaskForm(request.form)
                return render_template("admin_setting/permission_required.html", form = form)
        except Exception as e:
            current_app.logger.error(
               'ERROR affliation settings: {}'.format(e)) 
            return jsonify(success=False),400

@blueprint.route("/add", methods=['GET', 'POST'])
def add_affili():
    if not current_user.is_authenticated:
        return redirect(url_for('login.index_login'))
    if request.method == "POST":
        affiliation_name = request.json.get("affiliation_name")
        affiliation_idp_url = request.json.get("affiliation_idp_url")
        is_affiattion_name = Affiliation_Id_manager.get_affiliation_id_by_affiliation_name(affiliation_name)
        is_affiation_idp_url = Affiliation_Id_manager.get_affiliation_id_by_idp_url(affiliation_idp_url)
        try:
            if not any([is_affiattion_name, is_affiation_idp_url]):
                aff_id = Affiliation_Id(affiliation_idp_url=affiliation_idp_url, affiliation_name=affiliation_name)
                Affiliation_Id_manager.create_affiliation_id(aff_id)
                return jsonify(success=True),200
            else:
                return jsonify(success=False),400
        except Exception as e:
            current_app.logger.error(
                'ERROR affliation settings: {}'.format(e))
            return jsonify(success=False),400
    else:
        if current_user.role == "管理者":
            form = FlaskForm(request.form)
            return render_template("admin_setting/add_affili.html", form = form)
        else:
            form = FlaskForm(request.form)
            return render_template("admin_setting/permission_required.html", form = form)