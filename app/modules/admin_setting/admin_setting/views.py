from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint, json
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from modules.models.models.api import Affiliation_Id, Affiliation_Repository
from modules.login.login.views import index_login

blueprint = Blueprint(
    "admin_setting",
    __name__,
    url_prefix="/admin_setting",
    template_folder="templates",
    static_folder="static")

@blueprint.route("/", methods=['GET', 'POST'])
def index_affili():
    if not current_user.is_authenticated:
        return index_login()
    if request.method == "POST":
        affiliation_name = request.json.get("affiliation_name")
        repository_url = request.json.get("repository_url")
        access_token = request.json.get("access_token")
        if current_user.role == "管理者":
            affiliation_id_info = Affiliation_Id().get_affiliation_id_by_id(affiliation_name)
        else:
            affiliation_id_info = Affiliation_Id().get_affiliation_id_by_affiliation_name(affiliation_name)
        if affiliation_id_info:
            affiliation_repository_info = Affiliation_Repository().get_aff_repository_by_affiliation_id(affiliation_id_info.id)
            if affiliation_repository_info:
                try:
                    aff_repository = {"id":affiliation_repository_info.id, "affiliation_id":affiliation_id_info.id, "repository_url":repository_url,"access_token":access_token}
                    Affiliation_Repository().upt_aff_repository(aff_repository)
                    return jsonify(success=True),200
                except Exception as e:
                    return current_app.logger.error(
                'ERROR affliation settings: {}'.format(e)) 
            else:
                try:
                    aff_repository = {"affiliation_id":affiliation_id_info.id, "repository_url":repository_url,"access_token":access_token}
                    Affiliation_Repository().create_aff_repository(aff_repository)
                    return jsonify(success=True),200
                except Exception as e:
                    return current_app.logger.error(
                'ERROR affliation settings: {}'.format(e)) 
        else:
            return current_app.logger.error(
        'ERROR affliation settings: affiliation_id is not exist.') 
    else:
        role = current_user.role
        if role == "図書館員" or role == "管理者":
            repository_url = ""
            access_token = ""
            if role == "管理者":
                affiliation_name = "default"
                affiliation_id_info = Affiliation_Id().get_affiliation_id_by_affiliation_name(affiliation_name)
                affiliation_repository_info = Affiliation_Repository().get_aff_repository_by_affiliation_id(affiliation_id_info.id)
                if affiliation_repository_info:
                    repository_url = affiliation_repository_info.repository_url
                    access_token = affiliation_repository_info.access_token
            else:
                affiliation_id_info = Affiliation_Id().get_affiliation_id_by_id(current_user.affiliation_id)
                affiliation_name = affiliation_id_info.affiliation_name
                affiliation_repository_info = Affiliation_Repository().get_aff_repository_by_affiliation_id(affiliation_id_info.id)
                if affiliation_repository_info:
                    repository_url = affiliation_repository_info.repository_url
                    access_token = affiliation_repository_info.access_token
            affiliation_id_list = Affiliation_Id().get_affiliation_id_list()
            affiliation_repository_list = Affiliation_Repository().get_affiliation_repository_list()
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

@blueprint.route("/add", methods=['GET', 'POST'])
def add_affili():
    if not current_user.is_authenticated:
        return index_login()
    if request.method == "POST":
        affiliation_name = request.json.get("affiliation_name")
        affiliation_idp_url = request.json.get("affiliation_idp_url")
        affiliation_id_info = Affiliation_Id().get_affiliation_id_by_idp_url(affiliation_idp_url)
        try:
            if not affiliation_id_info:
                Affiliation_Id().create_affiliation_id(affiliation_idp_url, affiliation_name)
                return jsonify(success=True),200
        except Exception as e:
                return current_app.logger.error(
                'ERROR affliation settings: {}'.format(e))
    else:
        if current_user.role == "管理者":
            form = FlaskForm(request.form)
            return render_template("admin_setting/add_affili.html", form = form)
        else:
            form = FlaskForm(request.form)
            return render_template("admin_setting/permission_required.html", form = form)