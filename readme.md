### Installation
1. Download the git repo in the folder you want it
2. Navigate to spielegenerator/ copy .example.env to .env and edit the new .env file
3. Navigate into the main folder and run:
* "python3 manage.py migrate"
* "python3 manage.py makemigrations home"
* "python3 manage.py migrate"
* "python3 manage.py createsuperuser
4. Now start the server with "python3 manage.py runserver"
5. In your browser navigate to "localhost:8000/admin" and login with your created admin credentials of step 3. Now create at least one genre, one location, one "versus" and one time amount
6. After these steps you can navigate to the mainpage under localhost:8000 and create their your games, edit your locations, invite people (reverse proxie or portforwarding needed) and add extensions.
7. When you are done with the configuring have fun and find the perfect game for your next gamenight.
