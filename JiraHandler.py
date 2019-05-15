# -*- coding: utf-8 -*-

from jira.client import JIRA
from jira.exceptions import JIRAError
import os
import re
import sys
import warnings

from pprint import pprint

# ignore all warnings
# so as to not confuse the user
warnings.filterwarnings("ignore")


def main():
    
    # This script shows how to use
    # the client in anonymous mode
    # against josecuervo.atlassian.net.
    
    # By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
    # (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
    # Override this with the options parameter.
    
    # production JIRA URL specs @ production
    jira_url = 'https://your-subdomain.atlassian.net'
    jira_port = ''
    jira_uid = 'jose'
    jira_pwd = '[redacted]'
    
#    options = {
#        'server': 'https://your-subdomain.atlassian.net'
#    }
    options = {
        'server': jira_url + jira_port
    }

    # specify the username, password    
#    basic_auth = ('jose', '[redacted]')
    basic_auth = (jira_uid, jira_pwd)

    # instantiate a JIRA object
    # using the specified options
    try:
        jira = JIRA(options=options,
                    basic_auth=basic_auth)
    except JIRAError as e:
        sys.stderr.write(str(e))
        sys.stderr.write("\n")
        return
    
    # Get all projects
    # visible to logged-in user.
    projects = jira.projects()
    
    # Sort available project keys, then return the second, third, and fourth keys.
    # keys = sorted([project.key for project in projects])[2:5]

    # Sort available project keys
    keys = sorted([project.key for project in projects])
    
    # list the project keys
    for key in keys:
        print(key)

    project = "JPT"
    issue_id = project + "-21"
    
    # Search for an issue
    print("Searching for issue '%s'" % issue_id)
    issue = None
    try:
        issues = jira.search_issues('id=' + issue_id)
        # get the issue of the one in question
        # along with all of its comments, if any
        if len(issues) > 0:
            issue = jira.issue(issues[0].key, expand='comments')
        else:
            sys.stderr.write("JIRA issue not found: %s" % issue_id)
            sys.stderr.write(os.linesep)
    except JIRAError as e:
        sys.stderr.write(str(e))
        sys.stderr.write("\n")
        
    # if issue in question was
    # NOT found within the project
    if issue is None:
        # Create an issue.
        print("Creating issue '%s'" % issue_id)
        try:
            # Set the new issue's values
            issue_dict = {
                'project': {'key': project},
                'summary': 'New Issue from JIRA Python',
                'description': 'JIRA-Python generated issue',
                'issuetype': {'name': 'Task'}
            }
            # actually create the issue
            issue = jira.create_issue(fields=issue_dict)
        except JIRAError as e:
            sys.stderr.write(str(e))
            sys.stderr.write("\n")
            return
            
    # Add a comment to the issue
    print("Commenting on issue '%s'" % issue_id)
    try:
        jira.add_comment(issue, 'This here is a comment!')
        # you have to do the following if you want the
        # comment just added to be present in the issue object
        # mind you, it's in JIRA's database, just NOT in this
        # program's issue object until you effectively "reload" it below
        issue = jira.issue(issue.key, expand='comments')
    except JIRAError as e:
        sys.stderr.write(str(e))
        sys.stderr.write("\n")

    # Print all comments for the issue in question
    for comment in issue.fields.comment.comments:
        print("Comment author: %s" % comment.author)
        
    # Find all comments made by "josecuervo.com" on this issue.
    all_comments = [comment for comment in issue.fields.comment.comments
                    if re.search(r'@your-git-name.com$', comment.author.emailAddress)]

    pprint(all_comments)
    
    # Change the issue's summary and description.
    issue.update(summary="I'm different!", description='Changed the summary to be different.')
    
    # You can update the entire labels field like this
    issue.update(labels=['AAA', 'BBB'])
    
    # Or modify the List of existing labels. The new label is unicode with no spaces
    issue.fields.labels.append(u'new_text')
    issue.update(fields={"labels": issue.fields.labels})
    
    # Linking a remote jira issue (needs applinks to be configured to work)
#    print ("Linking issues")
#    try:
#        issue = jira.issue('JP-20')
#        issue2 = jira.issue('JP-21')
#        jira.add_remote_link(issue, issue2)
#    except JIRAError as e:
#        sys.stderr.write(str(e))
#        sys.stderr.write("\n")
    
    # Send the issue away for good.
#    print ("Deleting issue '%s'" % issue_id)
#    try:
#        issue.delete()
#    except JIRAError as e:
#        sys.stderr.write(str(e))
#        sys.stderr.write("\n")

    return

# =========================================================================
# execute the "main" method
# -------------------------------------------------------------------------


if __name__ == "__main__":
    main()  # -*- coding: utf-8 -*-
