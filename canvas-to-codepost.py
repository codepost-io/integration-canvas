# =============================================================================
# codePost – Download from Canvas Utility
#
# Downloads submissions from Canvas instance in a file structure that
# codePost will recognize.
# =============================================================================

# Python stdlib imports
import requests
import json
import os
import shutil
import re
import argparse

# =============================================================================

parser = argparse.ArgumentParser(description='Canvas to codePost!')
parser.add_argument('course_id', help='Course ID')
parser.add_argument('assignment_id', help='Assignment ID')
args = parser.parse_args()

# =============================================================================

# Constants
CANVAS_API_KEY = "<YOUR CANVAS ADMIN API KEY HERE>"
COURSE_ID = str(args.course_id)
ASSIGNMENT_ID = str(args.assignment_id)

BASE_URL = 'https://canvas.instructure.com/api/v1'
HEADERS = {'Authorization': "Bearer " + CANVAS_API_KEY}
OUTPUT_DIRECTORY = 'codepost_upload'
ERROR_DIRECTORY = 'errors'

_cwd = os.getcwd()
_upload_dir = os.path.join(_cwd, OUTPUT_DIRECTORY)
_error_dir = os.path.join(_cwd, ERROR_DIRECTORY)
_tmp_dir = os.path.join(_cwd, 'tmp')

# =============================================================================
# Canvas Endpoints


def assignment_submissions_endpoint(course_id, assignment_id):
return
"{}/courses/{}/assignments/{}/submissions?include[]=group".format(BASE_URL,
                                                                  course_id, assignment_id)


def users_endpoint(user_id):
    return "{}/users/{}?include[]=email".format(BASE_URL, user_id)

# ======================================================================


def delete_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def download_file_from_attachment(attachment):
    url = attachment['url']
    return requests.get(url, allow_redirects=True)


def write_file(path, content):
    with open(path, 'wb') as f:
        f.write(content)


def get_email_from_canvas(user_id):
    response = requests.get(users_endpoint(user_id), headers=HEADERS)
    try:
        user = json.loads(response)
        return user['email']
    except:
        return None


def check_for_partners(submission):

    def find_partner_attachment(list, filter):
        for x in list:
            if filter(x):
                return x
        return None

    if not 'attachments' in submission:
        return []

    partner_attachment = find_partner_attachment(submission['attachments'], lambda x: x[
        'filename'] == 'partners' or x['filename'] == 'partners.txt')

    if (partner_attachment != None):
        file = download_file_from_attachment(partner_attachment)
        filepath = os.path.join(_tmp_dir, str(partner_attachment['id']))
        write_file(filepath, file.content)

        emails = [line.rstrip('\n') for line in open(filepath, 'r')]
        EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
        filtered_emails = [x for x in emails if re.match(EMAIL_REGEX, x)]

        return filtered_emails
    else:
        return []

# ======================================================================

url = assignment_submissions_endpoint(COURSE_ID, ASSIGNMENT_ID)

print('------> Requesting submissions from Canvas')
print("------> {}".format(url))
print("")

response = requests.get(url, headers=HEADERS)
print(response)
print("")

try:
    submissions = json.loads(response.content)
except:
    raise RuntimeError(
        "Something went wrong requesting the submissions. Please check your API KEY")

# Overwrite the directories if they exist already
delete_directory(_upload_dir)
delete_directory(_error_dir)
delete_directory(_tmp_dir)

os.makedirs(_upload_dir)
os.makedirs(_error_dir)
os.makedirs(_tmp_dir)

# Make sure no students are on multiple submissions
students_with_submissions = []
students_with_multiple_submissions = []

# First pass –> make sure no student has multiple submissions
for i, submission in enumerate(submissions):
    user_id = str(submission['user_id'])

    # You must have Admin Access in order to query emails from Canvas Users
    user_email = get_email_from_canvas(user_id)

    if 'attachments' in submission:
        partners = check_for_partners(submission)
        if user_email != None and user_email not in partners:
            partners += [user_email]

        for partner in partners:
            if partner in students_with_submissions:
                students_with_multiple_submissions += [partner]

        students_with_submissions += partners

# Second pass -> build the codePost file structure
for i, submission in enumerate(submissions):
    print("--------> {} | submission({}) | files({})".format(i,
                                                             submission['id'], len(submission['attachments']) if 'attachments' in submission else 0))
    user_id = str(submission['user_id'])

    # You must have Admin Access in order to query emails from Canvas Users
    user_email = get_email_from_canvas(user_id)

    error = None

    # Is the student's email in Canvas?
    if (user_email == None):
        error = "EMAILNOTFOUND"

    # This student has multiple submissions
    if (user_email in students_with_multiple_submissions):
        error = "MULTIPLESUBS"

    partners = check_for_partners(submission)

    if user_email != None and user_email not in partners:
        partners += [user_email]

    # codePost naming convention
    # /assignmentFolder/partner1@university.edu,partner2@university.edu
    folder_name = ",".join(partners)
    student_dir = os.path.join(_upload_dir, folder_name)
    os.makedirs(student_dir)

    if 'attachments' in submission:
        # Download each file
        for attachment in submission['attachments']:
            filename = attachment['filename']
            file = download_file_from_attachment(attachment)

            if error != None:
                file_path = os.path.join(
                    _error_dir, "{}_{}_{}".format(user_id, error, filename))
            else:
                file_path = os.path.join(student_dir, filename)

            write_file(file_path, file.content)

# destroy tmp
delete_directory(_tmp_dir)
