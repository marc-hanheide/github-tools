#!/usr/bin/env python

from github import Github, enable_console_debug_logging
import json
from os import getenv

token = getenv("GITHUB_TOKEN", "ghp_1234567890abcdefgh")

g = Github(token)
enable_console_debug_logging()

def get_org(org_name="org_name"):
    """ Get organization

    Args:
        org_name: Name of organization

    Returns:
        org: Organization object

    """
    return g.get_organization(org_name)

class InviteUser:
    def __init__(self):
        self.org = None

    def add_user_to_group(self, user_name, org="LCAS", team_name="Developers"):
        """ Add user to team

        Args:
            user_name: Name of user
            team_name: Name of team

        Returns:
            None

        """
        if self.org is None:
            self.org = get_org(org)
        team = self.org.get_team_by_slug(team_name)
        user = g.get_user(user_name)
        team.add_membership(user)

    def invite_user_to_repo(self, user_name, org="LCAS", repo_name="Getting-Started"):
        """ Invite user to repository

        Args:
            user_name: Name of user
            repo_name: Name of repository

        Returns:
            None

        """
        if self.org is None:
            self.org = get_org(org)
        repo = self.org.get_repo(repo_name)
        user = g.get_user(user_name)
        repo.add_to_collaborators(user, permission="push")


if __name__ == "__main__":
    invite_user = InviteUser()
    #invite_user.invite_user_to_repo("marc-hanheide", "LCAS", "WAgriCISS")
    invite_user.add_user_to_group("strands-jenkins", "LCAS", "wagriciss")