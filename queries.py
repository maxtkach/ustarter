from tables import *
from sqlalchemy import desc

class UserQuery():
    def GetUserById(self, id):
        return db.session.query(User)\
            .get(id)
    def GetUserByEmail(self, email):
        return db.session.query(User) \
            .filter(User.email == email)\
            .first()
    def GetUsers(self):
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
            .filter(User.projectsParticipated.role == "Автор")\
            .all()
    def GetUsersInProjects(self):
        return db.session.query(User)\
            .filter(User.projectsParticipated)\
            .all()
    def GetUsersWithSponsoredProjects(self):
        return db.session.query(User)\
            .filter(User.projectsSponsored)\
            .order_by(desc(sum(sp.money for sp in User.projectsSponsored)))\
            .all()
    def GetTopUsersWithSponsoredProjects(self):
        return db.session.query(User)\
            .filter(User.projectsSponsored)\
            .order_by(desc(sum(sp.money for sp in User.projectsSponsored)))\
            .limit(4)\
            .all()
    def GetTopUsersWithProjects(self):
        return db.session.query(User)\
            .filter(User.projectsParticipated.role == "Author")\
            .order_by(desc(len(User.projectsParticipated) * len(ProjectQuery()
            .GetProjectById(User.projectsParticipated.projectId).usersClicked.split(" "))))\
            .limit(4)\
            .all()


class ProjectQuery():
    def GetProjectById(self, id):
        return db.session.query(Project)\
            .get(id)
    def GetUserProjects(self, userId):
        return db.session.query(Project)\
               .filter(Project.authorId == userId)\
               .all()
    def GetProjectByCaption(self, caption):
        return db.session.query(Project) \
            .filter(caption == Project.caption)\
            .first()
    def GetProjects(self):
        return db.session.query(Project)\
            .all()
    def GetProjectsByTeamMemberId(self, userId):
        team = UserQuery().GetUserById(userId).projectsParticipated
        projects = [self.GetProjectById(t.projectId) for t in team]
        return projects
    def GetTopProjects(self):
        return db.session.query(Project)\
            .filter(Project.usersClicked != None)\
            .order_by(desc(Project.usersClicked)) \
            .limit(4)\
            .all()
    def GetLatestProjects(self):
        return db.session.query(Project) \
            .order_by(desc(Project.createdOn)) \
            .limit(4)\
            .all()
    def GetProjectsBySponsorId(self, userId):
        sponsors = UserQuery().GetUserById(userId).projectsSponsored
        projects = [self.GetProjectById(s.projectId) for s in sponsors]
        return projects
    def GetProjectsByCategory(self, category):
        return db.session.query(Project) \
            .filter(Project.category == category) \
            .all()

class TeamQuery():
    def GetTeamByProjectId(self, projectId):
        return db.session.query(ProjectTeam).filter(ProjectTeam.projectId == projectId).all()
    def GetTeamByUserId(self, userId):
        return db.session.query(ProjectTeam).filter(ProjectTeam.userId == userId).all()

class SponsorQuery():
    def GetSponsorsByProjectId(self, projectId):
        return db.session.query(UserSponsor).filter(UserSponsor.projectId == projectId).all()
    def GetSponsorsByUserId(self, userId):
        return db.session.query(UserSponsor).filter(UserSponsor.userId == userId).all()
