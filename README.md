# data2bots_assessment_bitrus

This project contains backend code assessment for the Django developer role at Data2Bots role
## Getting Started

To run the project, first ensure you have cloned the repo and the database is setup correctly and follow the steps below. However I pushed this code to github alongside the file system django database sqlite3 with pre-populated data to ease testing.

 1. Ensure you are in the root directory with:

    `cd <path to root directory>`

 2. Create and activate a virtual  environment

 3. Install the requirements with:

    `pip install -r requirements.txt`
 4. Create an environment variable file in the root directory with:
 
    `touch .env`
5. Put in the following:
 
    `DEBUG=True`

    `SECRET_KEY=<Replace with your own secret>`
6.  Shell environment variable with the following command in the root directory where the file lives:

    `export $(xargs < .env)`

7. Start the server with:

    `python manage.py runserver`

8. Run unit test with:

    `python manage.py test`

9. To test the APIs, below is link to API Documentation:

    [Link to API Documentation](https://documenter.getpostman.com/view/14940225/2s7Z7YKaEU#9b84f64e-7fcd-49ca-9760-2d434a77647c)