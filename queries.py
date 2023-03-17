from tables import User, Project, Team, Sponsor

class UserQuery():
    def GetUserById(self, id, session):
        return session.query(User)\
            .get(id)
    def GetUserByProjectId(self, projectId, session):
        return session.query(User)\
            .filter_by(User.projectsParticipated.projectId == projectId)\
            .first_or_404()
    def GetAuthorByProjectId(self, projectId, session):
        return self.GetUserById(session.query(Project)
            .filter_by(Project.id == projectId)
            .first_or_404()
            .authorId, session)
    def GetUsersWithProjects(self, session):
        return session.query(User)\
            .filter_by(User.projectsParticipated.role == "Author")\
            .all()
    def GetUsersInProjects(self, session):
        return session.query(User)\
            .filter_by(User.projectsParticipated)\
            .all()
    def GetUsersWithSponsoredProjects(self, session):
        return session.query(User)\
            .filter_by(User.projectsSponsored)\
            .order_by(sum(sp.money for sp in User.projectsSponsored))\
            .all()
    def GetTopUsersWithSponsoredProjects(self, session):
        return session.query(User)\
            .filter_by(User.projectsSponsored)\
            .order_by(sum(sp.money for sp in User.projectsSponsored))\
            .limit(5)\
            .all()
    def GetTopUsersWithProjects(self, session):
        return session.query(User)\
            .filter_by(User.projectsParticipated.role == "Author")\
            .order_by(len(User.projectsParticipated) * len(ProjectQuery()
            .GetProjectById(User.projectsParticipated.projectId, session).usersClicked.split(" ")))\
            .limit(5)\
            .all()


class ProjectQuery():
    def GetProjectById(self, id, session):
        return session.query(Project)\
            .get(id)
    def GetProjectsByTeamMemberId(self, userId, session):
        return session.query(Project)\
            .filter_by(Project.team.userId == userId)\
            .all()
    def GetTopProjects(self, session):
        return session.query(Project) \
            .order_by(len(Project.usersClicked.split(" "))) \
            .limit(5)\
            .all()
    def GetLatestProjects(self, session):
        return session.query(Project) \
            .order_by(Project.createdOn) \
            .limit(5)\
            .all()
    def GetProjectsBySponsorId(self, userId, session):
        return session.query(Project) \
            .filter_by(Project.sponsors.userId == userId) \
            .all()

