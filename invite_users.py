#!/usr/bin/env python

from github import Github, enable_console_debug_logging, GithubException
from csv import DictReader
from os import getenv


class InviteUser:
    def __init__(self, token=None, debug=False):
        if debug:
            enable_console_debug_logging()
        if token is not None:
            self.g = Github(token, seconds_between_requests=0.05)
        else:
            self.g = Github(getenv("GITHUB_TOKEN", "ghp_1234567890abcdefgh"))

    def get_org(self, org_name="LCAS"):
        """ Get organization

        Args:
            org_name: Name of organization

        Returns:
            org: Organization object

        """
        return self.g.get_organization(org_name)
    
    def add_user_to_group(self, user_name, org_name="LCAS", team_name="Developers"):
        """ Add user to team

        Args:
            user_name: Name of user
            team_name: Name of team

        Returns:
            None

        """
        org = self.get_org(org_name)
        team = org.get_team_by_slug(team_name)
        user = self.g.get_user(user_name)
        team.add_membership(user)

    def invite_user_to_repo(self, user_name, org="LCAS", repo_name="Getting-Started", permission="push"):
        """ Invite user to repository

        Args:
            user_name: Name of user
            repo_name: Name of repository

        Returns:
            None

        """
        org = self.get_org(org)
        repo = org.get_repo(repo_name)
        user = self.g.get_user(user_name)
        repo.add_to_collaborators(user, permission=permission)
    
    def print_user(self, username):
        try:
            user = self.g.get_user(username)
        except Exception as e:
            print(f"User {username} not found")
            return
        print(user.login)
        print(user.get_organization_membership("LCAS").state)

    def is_member(self, user, organame="LCAS"):
        try:
            membership = user.get_organization_membership(organame).state
            return membership == "active"
        except GithubException as e:
            return False
    
    def add_user_to_repo(self, user_name, orga_name="LCAS", repo_names=["Getting-Started"], team_name="wagriciss"):
        user = self.g.get_user(user_name)
        org = self.get_org(orga_name)
        if self.is_member(user):
            team = org.get_team_by_slug(team_name)
            print("  adding %s member %s to team %s" % (orga_name, user_name, team_name))
            team.add_membership(user, role="member")
        else:
            print("user %s is not a member of org %s, so adding as collaborator" % (user_name, orga_name))
            for repo_name in repo_names:
                print("  checking to add %s as collaborator to repository %s" % (user_name, repo_name))
                repo = org.get_repo(repo_name)
                if repo.has_in_collaborators(user):
                    print("  %s is already a collaborator" % user_name)
                else:
                    invited = repo.get_pending_invitations()
                    for i in invited:
                        if i.invitee.login == user_name:
                            print("  %s has already been invited, removing invitiation" % i.invitee.login)
                            repo.remove_invitation(i.id)
                            break
                    print("  inviting %s to repository %s" % (user_name, repo_name))
                    repo.add_to_collaborators(user, permission="maintain")
                        
                



if __name__ == "__main__":

    invite_user = InviteUser()
    users = []
    repositories = [
        "WAgriCISS",
        "WAgriCISS_theme1",
        "WAgriCISS_theme2",
        "WAgriCISS_theme3",
        "WAgriCISS_theme4",
        "WAgriCISS_theme5",
        "WAgriCISS_theme6",
    ]
    group = "wagriciss"
    org = "LCAS"

    # debug
    #test_user = 'CabbSir'
    #invite_user.add_user_to_repo(test_user, org, repositories, group)

    

    with open("users.csv", "r") as csv_file:
        reader =DictReader(csv_file)
        for row in reader:
            if row["cleaned"] == "":
                continue
            try:
                invite_user.add_user_to_repo(row["cleaned"], org, repositories, group)
            except Exception as e:
                print('EXCEPTIION: %s when dealing with user %s, carry on.' % (e, row["cleaned"]))
                continue
