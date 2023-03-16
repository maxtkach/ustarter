from tables import User, Project, Team, Sponsor

class UserQuery():
    def GetUserById(self, id, session):
        return session.query(User)\
            .filter_by(User.id == id)\
            .first_or_404()
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


class ProjectQuery():
    def GetProjectById(self, id, session):
        return session.query(Project)\
            .filter_by(Project.id == id)\
            .first_or_404()
    def GetProjectByUserId(self, userId, session):
        return session.query(Project)\
            .filter_by(Project.team.userId == userId)\
            .first_or_404()
