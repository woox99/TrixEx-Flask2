


<img src="flask_app/static/assets/readme_imgs/home.png" width="700" alt="Image Description">


## About TrixEx

Store, share, and visualize front-end code. TrixEx allows developers to exchange front-end components. 

This application has been redesigned using the Pythong Django stack. Sign into the newly redesigned <a href="http://3.133.92.255/TrixEx.com" target="_blank">TrixEx2.o</a> with a demo account for full access to the site in a single click.

## Build Stack

![Static Badge](https://img.shields.io/badge/Python%20-%20%239A85BE)    ![Static Badge](https://img.shields.io/badge/Flask-%20%239A85BE)    ![Static Badge](https://img.shields.io/badge/MySQL-%20%239A85BE)    ![Static Badge](https://img.shields.io/badge/pip-%20%239A85BE) ![Static Badge](https://img.shields.io/badge/AWS%20EC2-%20%239A85BE) ![Static Badge](https://img.shields.io/badge/MVC%20Design-%20%239A85BE)


## Overview

* Adhered to the MVC design pattern, for a well-structured separation of concerns through modularization.
* Employed the Flask framework for rapid development, incorporating a range of functionality including Jinja2
templating, JSON response handling, HTTP routing methods, & session management.
* Established 'many-to-many relationships' with MySQL for features like followers, favorites, comments, and
replies, enhancing user engagement and interaction.
* Optimized deployment on AWS (EC2) for rapid spin-up time & cost-effective deployment.



## Features Walkthrough

#### Security

🔒 User Authentication & Authorization
* Password ***hashing***
* Registration ***validation***
* Route protection

---

<br>

<img src="flask_app/static/assets/readme_imgs/create.png" width="700" alt="Image Description">

<br>


To ***create*** a project, paste your HTML, CSS, and JS into the browser and watch your component come to life in real time.
* Set the project to ***private*** and it will only be visible to the creator.
* Set the project to ***public*** for the whole TrixEx community to see. 

---

<br>

<img src="flask_app/static/assets/readme_imgs/follow.png" width="450" alt="Image Description">

<br>


Viewing someone's component will show the code for it. If you like their work you can view their ***profile page*** and it will display their other public projects. 

***Follow*** users to show your support and keep track of components that interest you with the ***favorite*** button.

* One to many relationship with users and projects
* Many to many relationship with users and ***followers***
* Many to many relationship with users and ***favorites***

---

<br>

<img src="flask_app/static/assets/readme_imgs/comment.png" width="450" alt="Image Description">

<br>

Drop a ***comment*** or ***reply*** to get involved with other users in the TrixEx community.

* One to many relationship with users and comments
* Many to many relationship with comments and projects

---

<br>

<img src="flask_app/static/assets/readme_imgs/search.png" width="375" alt="Image Description">

<br>

***Search*** will return users or project results.

---

<br>

<img src="flask_app/static/assets/readme_imgs/trixexmobile.png" width="375" alt="Image Description">

<br>

***Responsive*** design to fit any device.

---

<br>

***Adminstrative*** dashboard for approved users to manage user activity.

* Delete inappropriate content
* Ban rule breakers
* Catalog login activity





