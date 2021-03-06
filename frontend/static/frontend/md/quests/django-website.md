<h1 class="header">Django Cloud Hosting</h1>
</br>
*31 October 2014* | [View On Github](https://github.com/sevaivanov/personal-website/blob/master/frontend/static/frontend/md/quests/django-website.md#host-django-website) | [Revision History](https://github.com/sevaivanov/personal-website/commits/master/frontend/static/frontend/md/quests/django-website.md)

# [Gandi](https://www.gandi.net)

## Why choose it? 

1. They have a great history of supporting freedoom and privacy on the internet. They [support](https://www.gandi.net/supports/) many projects, either financially, technically, administratively, or morally. 

2. They do not store your credit card information.

3. Their customer support is very fast.

## [Simple Hosting Instance](https://www.gandi.net/hosting/simple?language=python)

### Advantages

1. All the server side is handled for you.
2. You have more time to develop your project.
3. The costs are fewer comparing to Virtual Private Server.

### Counterparts

1. You can't add packages that are elsewhere than in the Python Package Index (pip) repositories even if they are present in common distributions like *pyexiv2*, in my case. Thus, it is a headache to avoid certain libraries just because they're relying on external C ones.

### How do I get started ?

Well their documentation covers a good part. I struggled in a few sections. This section should help you get going after painful hours of misunderstanding!

1. Buy a domain name

2. Take a [Simple Hosting](https://www.gandi.net/hosting/simple?language=python&db=mysql&grid=A) free testing instance for 5 days.

    Afterwards, you can renew it for a year with 5$/month -> 30$/1st year = 60$ - 30$ with a first use discount.

3. Configure your instance

    To enter your server via ssh, you have to activate it via the web pannel.

        ls web/vhosts/default/

    Here will be hosted your instance project. From this point you can read their [django-simple-hosting](http://wiki.gandi.net/en/simple/instance/python) documentation. It is important that you read it carefully. This part is crucial...

    > You must use Git to commit and push this file to the instance so it can be used.

    It means that you have to create a repository with Git [git-simple-hosting](http://wiki.gandi.net/en/simple/git) that will push the code to a Git repository **associated by name** to your default *vhost* folder seen earlier.

        mkdir -p gandi/roger/default
        cd gandi/roger/default
        git init
        git remote add origin ssh+git://12345@git.alien.gpaas.net/default.git
        echo "hi" > test
        git add test
        git commit -m "test" test
        git push origin master


    One important thing to understand is that right now Gandi does not support Git submodules. It means that you can't create a repository for your simple hosting instance and put your github external repository with the [.git/] folder inside. Otherwise, it will commit an empty folder to your Gandi repository. I know, it means it is a sync party! You will have to sync your external Github repository to your local Gandi one by hand. You can achieve that with *rsync*.

        rsync -az source/ destination/

    Add delete option to remove everything that is in *destination/* but not in the *source/*.

        rsync -az --delete source/ destination/


    For some reason, deploying code didn't work via the admim web pannel. Hence, to deploy your code from your Gandi Git repository to your web server, you must do it by handy hand.

        ssh 12345@git.alien.gpaas.net 'deploy default.git'


    Assuming you /vhost/default looks like

        default
          ├── requirements.txt
          ├── wsgi.py
          ├── static ──> myproject/myapp/static
          ├── myproject
          │   ├── myapp
          │   │   ├──static
          │   │   
          │   ├── manage.py
          │   │   
          │   ├── myproject
          │   │   ├── __init__.py
          │   │   ├── settings.py
          │   │   ├── urls.py

    Your *wsgi.py* file should be

        import os, sys

        django_project = os.path.abspath(os.path.join(os.path.dirname(__file__), 'myproject'))
        sys.path.append(django_project)

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()

    To avoid messing with your project structure and let the Gandi Apache collect your static files, add a symbolic link in your *default/* to your static folder.

            ln -s myproject/myapp/static static

    </br>
    [Domain-as-website](http://wiki.gandi.net/en/domains/management/domain-as-website)

    It is important that you understand how to connect your domain name to your website. There are three ways to do it. I suggest the third one: *Configuring your zone file at Gandi*. It can take up to a few hours before it spreads to the World Wide Web.

    Why should I use the Domain-as-website?

    > The Gandi web forwarding server is serving a robots.txt file that you probably don't want.

    Hence, my website wasn't indexed by google crawlers.

    Go to your Gandi admin pannel under *Simple Hosting > Your Instance > Websites Section* and add your addresses to the vhosts & check the **DNS modification** box.

    Websites Section example:

        Address (vhost) (2/2)
        ---------------------
        webiste.com
        www.website.com

    You have to insert into *myproject/settings.py*

        ALLOWED_HOSTS = ['website.com', 'www.website.com']

    Otherwise you will get an **Internal Server Error**.

    There will be a certain amount of time to allow the propagation of the DNS zone file. It's a great occasion to take a cup of tea!

4. Due to the Varnish cahing system, the instance has difficulties delivering the appropriate webpage even after a reasonable delay when switching user agents or browsers.

    Although you can't completely disable it using Gandi, there is an easy way to do it with Django. First let's see what is happenning:

        > curl -I yourwebsite.com
        ...
        Via: 1.1 varnish
        Age: 30

    *Why should I disable it?*

    You probably don't have a high-traffic website and want your users to view the right version of your website depending on their browser/device without any possible delay. Remember that web browsers have their caching, which means that once the page has been loaded, it probably stays in the user cache during all of his navigation. Hence, if you have a second mobile version or you're detecting dinosaur browsers, you might (under the same external IP) either get through with non-supported browsers or get a delay between a mobile and a desktop version accessibility.

    In order to stop caching, you have to add headers to the response that will stop the caching. The *Django* framework has a *add_never_cache_headers* function [here](https://github.com/django/django/blob/master/django/utils/cache.py), that is called from *never_cache* decorator [here](https://github.com/django/django/blob/master/django/views/decorators/cache.py), that you just need to import:

        from django.views.decorators.cache import never_cache

    And then add **@never_cache** decorator above all of the controllers in your *views.py* where you don't want to cache. Then you should have something like:
        
        > curl -I yourwebsite.com
        ...
        Cache-Control: max-age=0
        Via: 1.1 varnish
        Age: 0

<p class="footer">Everything else is explained very clearly in the Gandi.net documentation.</p>
