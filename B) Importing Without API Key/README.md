# Importing Canvas submissions into codePost manually

First, we’ll download assignment submissions from Canvas to our local machine.

Next, we’ll run `canvas_to_codepost_manual` script, which will create a folder called `codepost_upload` which you can drag-and-drop into codePost. Any errors will show up in the `errors` folder.

The process will only take a minute, start to finish.

> Need help? Email us at team@codepost.io

## 0. Downloading Submissions from Canvas

In your Canvas Instance, to `Course -> Assignments -> <This Assignment> -> Download Submissions`

## 1. Create a roster

Since the Canvas downloads are indexed by student names, we need to map {StudentName} to {Email} in order to upload to codePost.

Create a roster.csv with the following information:

```
first,last,email
turing,alan,turing@school.edu
liskov,barbara,liskov@school.edu
cooper,sheldon,cooper@school.edu
```

## 1. Setting up the script

Clone this repository or copy the python script `canvas_to_codepost_manual.py` to your local machine.

Move the downloaded submissions into the same directory as the script and name the folder `submissions`.

Move the roster.csv file you created into the same directory as the script. Make sure this file is called `roster.csv.`

## 3. Run the script

Make sure that you have Python3 installed and run

`python3 canvas_to_codepost_manual.py submissions roster.csv`

You should now see a folder called `codepost_upload`, whose subfolders correspond to students. Any problem files will show up in the `errors` folder.

> Optional flag '--simulate' will run the script without copying any files
> `python3 canvas_to_codepost_manual.py submissions roster.csv --simulate`

## 4. Upload to codePost

Navigate to [codepost.io](https://codepost.io), log in, and click `Assignments -> Actions -> Upload Submissions -> Multiple Submissions`. Drag `codepost_upload` into codePost and voila.

If you prefer to have more control over the upload process, check out our [Python SDK](https://github.com/codepost-io/codepost-python).

## Special Case A: Partners

Many assignments will have students submit together in groups of 2 or more. Although Canvas has the notion of "Groups", it doesn't have a way for students to independently decide to partner on an assignment and submit together.

If you want codePost to recognize group submissions, you can require your students to submit an extra file in their submission called `partners.txt` which contains the email address of each group member on a newline.

Like this:

```
partner1@school.edu
partner2@school.edu
partner3@school.edu
```

The `canvas_to_codepost_manual` script will read this file from Canvas and do the work necessary to make sure the students are recorded as partners on codePost.
