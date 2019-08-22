# =============================================================================
# codePost – Download from Canvas Utility
#
# Downloads submissions from Canvas and transform the file structure into
# a structure that codePost will recognize.
#
# Use this script if you don't have a Canvas Admin API Key
# =============================================================================

# Python stdlib imports
import os
import argparse
import csv
import shutil
import re

# =============================================================================

parser = argparse.ArgumentParser(description='Canvas to codePost!')
parser.add_argument(
    'submissions', help='The directory of submissions downloaded from Canvas')
parser.add_argument(
    'roster', help='The course roster of students that includes first name, last name, and email')
parser.add_argument('-s', '--simulate', action='store_true')
args = parser.parse_args()

# =============================================================================
# Constants

OUTPUT_DIRECTORY = 'codepost_upload'
ERROR_DIRECTORY = 'errors'

_cwd = os.getcwd()
_upload_dir = os.path.join(_cwd, OUTPUT_DIRECTORY)
_error_dir = os.path.join(_cwd, ERROR_DIRECTORY)

# =============================================================================
# Helpers


def normalize(string):
  return string.lower().strip()


def delete_directory(path):
  if os.path.exists(path):
    shutil.rmtree(path)


def validate_csv(row):
  for key in row.keys():
    if 'first' in normalize(key):
      first = key
    elif 'last' in normalize(key):
      last = key
    elif 'email' in normalize(key):
      email = key

  if first == None or last == None or email == None:
    if first == None:
      print("Missing header: first")
    if last == None:
      print("Missing header: last")
    if email == None:
      print("Missing header: email")

    raise RuntimeError(
        "Malformatted roster. Please fix the headers and try again.")

    return (first, last, email)
  else:
    return (first, last, email)


def name_to_email(roster):
  with open(roster, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    first, last, email = (None, None, None)
    name_to_email = {}
    for row in csv_reader:
      if line_count == 0:
        (first, last, email) = validate_csv(row)
        line_count += 1

      # Canvas convention: map {lastname}{firstname} to {codePost email}
      name_to_email["{}{}".format(
          normalize(row[last]), normalize(row[first]))] = normalize(row[email])
      line_count += 1
    return name_to_email


def check_for_partners(file_name):
  filepath = os.path.join(args.submissions, file_name)
  emails = [line.rstrip('\n') for line in open(filepath, 'r')]
  EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
  filtered_emails = [x for x in emails if re.match(EMAIL_REGEX, x)]

  return filtered_emails

# =============================================================================

if (args.simulate):
  print('\n~~~~~~~~~~~ START SIMULATION ~~~~~~~~~~~')

print('\nSetting up directories...')

# Overwrite the directories if they exist already
if not args.simulate:
  delete_directory(_upload_dir)
  delete_directory(_error_dir)

  os.makedirs(_upload_dir)
  os.makedirs(_error_dir)

print('\t/{}'.format(OUTPUT_DIRECTORY))
print('\t/{}'.format(ERROR_DIRECTORY))

print('\nReading and validating roster...')
name_to_email = name_to_email(args.roster)
print('\tVALID')

print('\nChecking submissions for partners...')

files = os.listdir(args.submissions)
folders = []
for file in files:
  file_name = file.split('_')[-1]
  if 'partners' in file_name:
    partners = check_for_partners(file)
    folders.append(partners)

print('\t{}'.format(folders))

print('\nCreating student folders...')
for student in name_to_email:
  found = False
  for folder in folders:
    if name_to_email[student] in folder:
      found = True
      break

  if not found:
    folders.append([name_to_email[student]])

for folder in folders:
  folder_name = ",".join(folder)
  if not args.simulate:
    os.makedirs(os.path.join(_upload_dir, folder_name))
  print('\t{}'.format(folder_name))


print('\nMapping and copying files...')
for file in files:
  student_name = file.split('_')[0]
  file_name = file.split('_')[-1]

  if normalize(student_name) in name_to_email:
    email = name_to_email[student_name]
    found = False

    for folder in folders:
      if email in folder:
        folder_name = ",".join(folder)
        found = True
        if not args.simulate:
          shutil.copyfile(os.path.join(args.submissions, file), os.path.join(
              os.path.join(_upload_dir, folder_name), file_name))
        print('\t{}'.format(os.path.join(
            os.path.join(_upload_dir, folder_name), file_name)))

    if not found:
      if not args.simulate:
        shutil.copyfile(os.path.join(args.submissions, file),
                        os.path.join(_error_dir, file))
      print('\tERROR: {}'.format(os.path.join(_error_dir, file)))
  else:
    if not args.simulate:
      shutil.copyfile(os.path.join(args.submissions, file),
                      os.path.join(_error_dir, file))
    print('\tERROR: {}'.format(os.path.join(_error_dir, file)))

if args.simulate:
  print('\n~~~~~~~~~~~ END SIMULATION ~~~~~~~~~~~\n')
