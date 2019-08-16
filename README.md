# Integrating with Canvas

## Importing Canvas submissions into codePost

We will use the Canvas API to download assignment submissions to our local machine in a file structure that codePost will recognize.

Running the `canvas-to-codepost` script will create a folder called `codepost_upload` which you can then drag-and-drop into codePost. Any problem files will go to an `errors` folder.

The process will only take a minute, start to finish.

> Need help? Email us at team@codepost.io

### 0. Getting your Canvas API Key

For this script, you will need to ask your Canvas Admin for the API Key.

Technical aside:

> Without the Admin API Key, the script won't be able to query the /users/:user_id endpoint which will map Canvas UserIDs to emails.

### 1. Get the COURSE_ID and the ASSIGNMENT_ID

Log into Canvas and navigate to the assignment page. In the URL you will see the COURSE_ID first and the Assignment_ID second. Copy these.

> Example: https://canvas.instructure.com/courses/1668XXX/assignments/12044XXX

### 2. Setting up the script

Clone this repository or copy the python script `canvas-to-codepost.py` to your local machine.

Replace `<YOUR CANVAS ADMIN API KEY HERE>` with your API KEY.

### 3. Run the script

Make sure that you have Python installed and run

`python3 canvas-to-codepost <COURSE_ID> <ASSIGNMENT_ID>`

You should now see a folder called `codepost_upload` with the student directories and submissions. Any problem files will be in the `errors` folder.

### 4. Upload to codePost

Navigate to [codepost.io](https://codepost.io), log in, and click `Assignments -> Actions -> Upload Submissions -> Multiple Submissions`. Drag `codepost_upload` and voila.

If you prefer to have more control over the upload process, check out our `upload-to-codepost` [command-line tool](https://github.com/codepost-io/codePost-tools) and our [Python SDK](https://github.com/codepost-io/codepost-python).

### Special Case A: Partners

Many assignments will have students submit in partners. Although Canvas has the notion of "Groups", it doesn't have a way for students to independently decide to partner on an assignment and submit together.

One solution to this will be to have students submit an extra file in their submission called `partners.txt`, where each in the submission's email is written on a new line.

As such:

```
partner1@university.edu
partner2@university.edu
partner3@university.edu
```

The `canvas-to-codepost` script will read this file from Canvas and do the work necessary to make sure the students are recorded as partners on codePost.
