# Steps for above project
1. Clone this repo<br>
2. Create virtual env<br>
<pre>
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
pip3 install -r requirements.txt
</pre>
3. Create an app password in gmail, add gmail address and password in settings.
4. To start celery<br>
<pre>
1. create and start redis docker container
2. use celery command:
$ celery -A school_project.celery worker -l info 
</pre>
