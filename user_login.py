from flask_login import UserMixin
from flask import url_for, flash
import os


class UserLogin(UserMixin):
    def from_db(self, user_id, dbase):
        self.__user = dbase.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return self.__user['name'] if self.__user else "No name"

    def get_email(self):
        return self.__user['email'] if self.__user else "No email"

    def get_ava(self):
        path_img = None
        if not self.__user['avatar']:
            path_img = url_for('static',
                               filename=os.path.join('images_html',
                                                     'avatar', 'default.png'))
            self.__user['avatar'] = path_img
            return self.__user['avatar']

        return self.__user['avatar']

    def allowed_file_avatar(self, filename):
        extension_file = filename.rsplit(".", 1)[1]
        if extension_file in ("png", "PNG", "jpeg", "JPEG"):
            return True

        flash("Invalid file type. Type have to be 'png' or 'jpeg'.")

        return False
