An app to create, manage survey and allow users to respond to suveys.

How to run...

1. Make sure you have Python 3.7 or higher version installed.
2. Create a virtual environment to store project dependencies by running this command in terminal
	
	First move to the directory where you want to create virtual environment and store the project. Then run this command on terminal...

	python -m venv virtual_environment_name

3. After installing the virtual environment check if the the directory is created in the folder where executed the command.
4. After confirming the directory use this command to move inside the directory to activate the virtual environment...
	
	cd virtual_env_directory_name

	& then run this command to activate the environment...

	scripts/activate (After running this command you will see the name of virtual environment appearing at start of your terminal line indicating that the env was activated)

	Now we are ready for the final step.

5. Place your project directory inside the virtual enivormant directory. (You can paste the directory anywhere but placing it inside env directory makes it easy to activate the env and acces our project directly)

6. After placing the project directory inside the env directory run this command to move inside project directory...
	
	cd survey

7. Once you are inside the project directory run this command to install the project dependencies...

	pip install -r requirements.txt

	this command will open the requirements.txt file inside the project directory and will install all of the required libraries 1 by 1.

8. After running the above mentioned command check if django is installed perfecty by running this command...
	
	django --version	(if django is not installed. Then run this command "pip install django")

9. After confirming Django version you are ready to use the application. Since I have already set up everything else you are ready to use the application directly

10. Run this command to activate localhost server...

	python manage.py runserver

	After running this command Django development server will start and you can access the application at these urls: http:/localhost:8000 or http://127.0.0.1:8000/


But if you want to use anyother database instead of SQLite 3 do the following...

1. Inside the project directory there will be another directory with same name "survey". Open that directory and then open setting.py file. This is the file that will have all the settings for your application, from database configuration, smtp server settings, application module registration to all the other settings required for running this application.

2. Inside the settings applciation you need to see these things. 

	SECRET_KEY (This is the main thing that keeps your Django/Python project secure never share it with other or change it)

	DEBUG (This variable tells the framework if the application is in development or deployment mode, DEBUG = True means it is currently in development mode and will show errors for debuging but if you replace True witf False then Dajngo will not display erors in debug mode but will display the basic error pages like Error 404 and other page.)

	You can change the database settings on line 87 to 107. The part in if condition is for development mode and if you want to change type of database you can fill in the required info in the fields, like databse engine, database name, user name, password and other things.

	Also you need to add your own smtp server so that application can send emails to user inviting them to fill survey. The set up for smtp is at line 167 to line 185. This is just like database setup section the if part is for development mode and else is for deployment mode. You can add your own information for your smtp server. Here accordingly.

If you decide to change that database please follow these setups...

1. Add database settings in setting.py file.
2. Stop the running server if it is running other wise make sure you have virtual environment activated and run these commands 1 by 1

	python manage.py makemigrations  (To check if any table is updated or not)

	Python manage.py migrate (To upload all the changes to database)

	python manage.py createsuperuser (To create super user admin creds, so you can login to Django admin panel)


Links for all the pages...

1. localhost:8000 (Main page and survey creation page)

2. localhost:8000/survey/slug_value (Page to edit created survey and upload csv file for inviting user to fill survey. This page will load by default when you will create any survey)

3. localhost:8000/survey-list (Page to view created survey list)

4. localhost:8000/survey/slug_value/username (Page which will load when user will click on take survey button in their emails)

5. localhost:8000/ingest-data (Page to upload reponse for survey created outside of the platform)

Keep in mind that the links that require parameters like slug_value and username requrie to varify some information from database so trying to open the pages with random value will not load the page but will show error 404.

Some other instructions...
1. Instruction on how to access Django Admin Panel...

	Go to this link to open the Django Admin Panel  "localhost:8000/admin", but you need to have superuser, admin or staff account to acces the admin panel. You can create super user account by using this command in your command line...
	
	python manage.py createsuperuser

	After running this command add these information when asked, "1. Username, 2. Email (Optional), 3. Password, 4. Confirm Password"

	Then you can use these credentials to acces django admin panel.

	Inside admin panel you can access all the database tables and their data you have created in your apps.

2. How to access survey answer page...

	By default you can access survey answer page by clicking the "Start Survey" button in the email user will get for the survey invitation. But if you want to check the answer page, then follow this url format to access it by following this url format.

	localhost:8000/upload/survey_slug/username

	here you can add any string value for the username parameter but you can not enter random value in slug_value parameters place. You need to the exact slug value that is saved in database when you create a new survey. You can get that slug value by going to Django Admin panel and check "Survey Details" Table.

I hope you don't face any issues after reading this. But in case you can reach out to me for further assistance. Thank you.

