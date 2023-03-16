from tables import User, Project, Team, Sponsor

class User_Query():
    def get_user_by_id(self, id, session):
        return session.query(User)\
            .filter_by(User.id == id)\
            .first_or_404()
    def get_user_by_project_id(self, project_id, session):
        return session.query(User)\
            .filter_by(User.projects_participated.project_id == project_id)\
            .first_or_404()
    def get_author_by_project_id(self, project_id, session):
        return self.get_user_by_id(session.query(Project)
            .filter_by(Project.id == project_id)
            .first_or_404()
            .author_id, session)
    def get_users_with_projects(self, session):
        return session.query(User)\
            .filter_by(User.projects_participated.role == "Author")\
            .all()
    def get_users_in_projects(self, session):
        return session.query(User)\
            .filter_by(User.projects_participated)\
            .all()
    def get_users_with_sponsored_projects(self, session):
        return session.query(User)\
            .filter_by(User.projects_sponsored)\
            .order_by(sum(sp.money for sp in User.projects_sponsored))\
            .all()


class Project_Query():
    def get_project_by_id(self, id, session):
        return session.query(Project)\
            .filter_by(Project.id == id)\
            .first_or_404()
    def get_project_by_user_id(self, user_id, session):
        return session.query(Project)\
            .filter_by(Project.team.user_id == user_id)\
            .first_or_404()
