# Importing submissions into codePost using the Canvas API

We will use the Canvas API to download assignment submissions to our local machine in a file structure that codePost will recognize.

Running the `canvas_to_codepost_api` script will create a folder called `codepost_upload` which you can drag-and-drop into codePost to upload the submissions. Any errors will show up in the `errors` folder.

The process will only take a minute, start to finish.

> Need help? Email us at team@codepost.io

## 0. Getting your Canvas API Key

To get a Canvas API Key, either ask your school’s Canvas Admin or login to Canvas and go to `Account -> Settings -> New Access Token`

## 1. Get the COURSE_ID and the ASSIGNMENT_ID

Log into Canvas and navigate to the assignment page. In the URL you will see the COURSE_ID first and the Assignment_ID second. Copy these.

> Example: https://canvas.instructure.com/courses/1668XXX/assignments/12044XXX

## 2. Setting up the script

Clone this repository or copy the python script `canvas_to_codepost_api.py` to your local machine.

In the code of `canvas_to_codepost_api.py`, replace `<YOUR CANVAS API KEY HERE>` with your API KEY.

## 3. Run the script

Make sure that you have Python3 installed and run

`python3 canvas_to_codepost_api.py <COURSE_ID> <ASSIGNMENT_ID>`

After the script terminates, you should see a folder called `codepost_upload` containing the student directories and submissions. Any problem files will be in the `errors` folder.

## 4. Upload to codePost

Navigate to [codepost.io](https://codepost.io), log in, and click `Assignments -> Actions -> Upload Submissions -> Multiple Submissions`. Drag `codepost_upload` into codePost and voila.

If you prefer to have more control over the upload process, check out our [Python SDK](https://github.com/codepost-io/codepost-python).

## Special Case A: Partners

Many assignments will have students submit together in groups of 2 or more. Although Canvas has the notion of "Groups", it doesn't have a way for students to independently decide to partner on an assignment and submit together.

If you want codePost to recognize group submissions, you can require your students to submit an extra file in their submission called `partners.txt` which contains the email address of each group member on a newline.

Like this

```
partner1@school.edu
partner2@school.edu
partner3@school.edu
```

The `canvas_to_codepost_api` script can read this file from Canvas and do the work necessary to make sure the students are recorded as partners on codePost.
