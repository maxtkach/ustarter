from tables import *

class UserQuery():
    def GetUserById(self, id):
        return db.session.query(User)\
            .get(id)
    def GetUsers(self, id):
        return db.session.query(User)\
            .all()
    def GetUserByProjectId(self, projectId):
        return db.session.query(User)\
            .filter(User.projectsParticipated.projectId == projectId)\
            .first()
    def GetAuthorByProjectId(self, projectId):
        return self.GetUserById(db.session.query(Project)
            .filter(Project.id == projectId)
            .first()
            .authorId)
    def GetUsersWithProjects(self):
        return db.session.query(User)\
            .filter(User.projectsParticipated.role == "Author")\
            .all()
    def GetUsersInProjects(self):
        return db.session.query(User)\
            .filter(User.projectsParticipated)\
            .all()
    def GetUsersWithSponsoredProjects(self):
        return db.session.query(User)\
            .filter(User.projectsSponsored)\
            .order_by(sum(sp.money for sp in User.projectsSponsored))\
            .all()
    def GetTopUsersWithSponsoredProjects(self):
        return db.session.query(User)\
            .filter(User.projectsSponsored)\
            .order_by(sum(sp.money for sp in User.projectsSponsored))\
            .limit(5)\
            .all()
    def GetTopUsersWithProjects(self):
        return db.session.query(User)\
            .filter(User.projectsParticipated.role == "Author")\
            .order_by(len(User.projectsParticipated) * len(ProjectQuery()
            .GetProjectById(User.projectsParticipated.projectId).usersClicked.split(" ")))\
            .limit(5)\
            .all()


class ProjectQuery():
    def GetProjectById(self, id):
        return db.session.query(Project)\
            .get(id)
    def GetProjects(self):
        return db.session.query(Project)\
            .all()
    def GetProjectsByTeamMemberId(self, userId):
        team = UserQuery().GetUserById(userId).projectsParticipated
        projects = [self.GetProjectById(t.projectId) for t in team]
        return projects
    def GetTopProjects(self):
        return db.session.query(Project) \
            .order_by(len(Project.usersClicked.split(" "))) \
            .limit(5)\
            .all()
    def GetLatestProjects(self):
        return db.session.query(Project) \
            .order_by(Project.createdOn) \
            .limit(5)\
            .all()
    def GetProjectsBySponsorId(self, userId):
        sponsors = UserQuery().GetUserById(userId).projectsSponsored
        projects = [self.GetProjectById(s.projectId) for s in sponsors]
        return projects
    def GetProjectsByCategory(self, category):
        return db.session.query(Project) \
            .filter(Project.category == category) \
            .all()
