# -*- coding: utf-8 -*-
# !/usr/bin/python
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import os
import json
import paramiko
from func import share
from urls import server_mods
from flask import Flask, render_template, request, Response
app = Flask(__name__)


def check_methods():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data)
        mod = server_mods.get(json_data['mod'])
        if mod:
            response_str = mod(data)
            return response_str


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    跳转起始界面
    :return:
    """
    return render_template('MT_agreement.html')


@app.route('/MT_agreement', methods=['GET', 'POST'])
def agreement():
    """
    跳转协议许可界面
    :return:
    """
    return render_template('MT_agreement.html')


@app.route('/MT_note', methods=['GET', 'POST'])
def note():
    """
    跳转用户需知界面
    :return:
    """
    return render_template('MT_note.html')


@app.route('/MT_check_env', methods=['GET', 'POST'])
def check_env():
    """
    跳转系统环境检查界面
    :return:
    """
    return render_template('MT_check_evn.html')


@app.route('/MT_check_os', methods=['GET', 'POST'])
def check_os():
    """
    检测系统版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_check_evn.html')


@app.route('/MT_check_storage', methods=['GET', 'POST'])
def check_storage():
    """
    检测/var/cache空间大小
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_check_evn.html')


@app.route('/MT_close_tool', methods=['GET', 'POST'])
def close_tool():
    """
    关闭迁移工具
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/MT_check_user', methods=['GET', 'POST'])
def check_user():
    """
    检测用户账户
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')
    
    return render_template('MT_check_root.html')


@app.route('/MT_repo', methods=['GET', 'POST'])
def repo():
    """
    跳转软件仓库界面
    :return:
    """
    return render_template('MT_repo.html')


@app.route('/MT_check_repo', methods=['GET', 'POST'])
def check_repo():
    """
    检测软件仓库
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/MT_kernel', methods=['GET', 'POST'])
def check_kernel():
    """
    跳转检测内核界面
    :return:
    """
    return render_template('MT_kernel.html') 


@app.route('/MT_check_os_kernel', methods=['GET', 'POST'])
def check_os_kernel():
    """
    检测系统内核版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_kernel.html')


@app.route('/MT_repo_kernel', methods=['GET', 'POST'])
def repo_kernel():
    """
    检测软件仓库内核版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_kernel.html')


@app.route('/Mt_environment', methods=['GET', 'POST'])
def environment():
    """
    跳转迁移前环境检测界面
    :return:
    """
    return render_template('MT_check_environment.html')


@app.route('/MT_check_environment', methods=['GET', 'POST'])
def check_environment():
    """
    迁移前系统环境检查
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')
    return render_template('MT_check_environment.html')


@app.route('/MT_check_progress', methods=['GET', 'POST'])
def check_progress():
    """
    环境检测进度检测
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_check_environment.html')


@app.route('/MT_export_migration_reports', methods=['GET', 'POST'])
def export_migration_reports():
    """
    导出迁移检测报告
    :return:
    """
    mod = check_methods()
    if mod:
        data = request.get_data()
        json_data = json.loads(data)
        user = json_data.get('info').split("|")[0]
        info = mod.split(',')
        ip = info[1].strip('"')
        port = 22

        with open("/usr/lib/migration-tools-server/.passwd.txt", "r") as f:
            password = f.read()

        remote_dir = local_dir = "/var/tmp/uos-migration"
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, port, user, password)
            sftp = client.open_sftp()

            remote_files = sftp.listdir(remote_dir)
            # 遍历远程文件列表
            for filename in remote_files:
                if filename.endswith('.tar.gz'):
                    remote_file_path = os.path.join(remote_dir, filename)
                    local_file_path = os.path.join(local_dir, filename)
                    sftp.get(remote_file_path, local_file_path)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # 关闭连接
            if client:
                client.close()
        return Response(mod, content_type='application/json')


@app.route('/MT_migration', methods=['GET', 'POST'])
def migration():
    """
    跳转迁移中界面
    :return:
    """
    return render_template('MT_migration.html')


@app.route('/MT_migration_progress', methods=['GET', 'POST'])
def migration_progress():
    """
    迁移进度
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_migration.html')


@app.route('/MT_system_migration', methods=['GET', 'POST'])
def system_migration():
    """
    迁移状态
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_migration.html')


@app.route('/MT_migration_results', methods=['GET', 'POST'])
def migration_results():
    """
    跳转迁移完成界面
    :return:
    """
    return render_template('MT_migration_results.html')


@app.route('/MT_system_migration_info', methods=['GET', 'POST'])
def system_migration_info():
    """
    迁移日志
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_migration.html')


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    uos_sysmig_conf = json.loads(share.get_sysmig_conf())
    ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
    port = int(json.loads(uos_sysmig_conf).get('serverport').strip()[1:-1])
    app.run(debug=True, host=ip, port=port)
