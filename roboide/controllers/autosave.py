
# Turbogears imports
from tg import expose
from sqlalchemy import or_
from roboide import model

# Standard library imports
import os
import string

# Import SR code
import user as srusers

class Autosave(object):

    @expose("json")
    @srusers.require(srusers.in_team())
    def savefile(self, team, path, content, rev):
        src_rev = int(rev)
        src_team = model.TeamNames.get(int(team))
        user = str(srusers.get_curuser())

        files = model.AutoSave.query.filter_by(
                    file_path = path,
                    team = src_team,
                    uname = user
                ).all()

        if len(files) > 0 :  #if it exists we're doing an update, else we need a new file
            save = files[0]
            save.set(file_path = path, revision = src_rev, team = src_team, uname = user, content = content)
        else:
            save = model.AutoSave(file_path = path, revision = src_rev, team = src_team, uname = user, content = content)

        return { 'date' : save.date, 'code' : save.content }

    @srusers.require(srusers.in_team())
    def getfilesrc(self, team, path, content = 0):
        user = str(srusers.get_curuser())
        src_team = model.TeamNames.get(int(team))

        #build a test for things that match the user and team
        test_set = model.AutoSave.query.filter_by(team = src_team, uname = user)

        if content == 1: #if we're after a specific file
            test_set = test_set.filter_by(file_path = path)
        else:
            test_set = test_set.filter(model.AutoSave.file_path.startswith(path))


        files = test_set.all()
        files_data = {}

        if len(files) > 0:   #if there's some files
            if content == 0:
                for f in files:
                    files_data[f.file_path] =  { 'date' : f.date, 'user' : f.uname, 'revision' : f.revision }
                return files_data
            else:
                return files[0].content
        else:
            if content == 1:
                return ""
            else:
                return {}

    @srusers.require(srusers.in_team())
    def move(self, team, src, dest):
        user = str(srusers.get_curuser())
        src_team = model.TeamNames.get(int(team))

        #build a test for things that match the user and team
        test_set = model.AutoSave.query.filter_by(team_id = src_team, uname = user)

        files = test_set.filter(model.AutoSave.file_path.startswith(src)).all()

        if len(files) > 0:   #if there's some files
            for f in files:
                new_path = string.replace(f.file_path, src, dest, 1)
                f.set(file_path = new_path)

        return ""

    @srusers.require(srusers.in_team())
    def delete(self, team, path):
        user = str(srusers.get_curuser())
        src_team = model.TeamNames.get(int(team))
        path_dir = str(path+"/")

        #build the tests: match team, user and ( path match OR path begins with given path plus a / )
        test_set = model.AutoSave.query.filter_by(team = src_team, uname = user)

        files = test_set.filter(or_(
                    model.AutoSave.file_path == path,   # exactly that file
                    model.AutoSave.file_path.startswith(path_dir)   # a file in that folder
                )).all()

        if len(files) > 0:   #if there's some files
            files[0].delete()
            return {}
        else:
            return { 'error' : 'no file to delete' }

