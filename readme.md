## credit 

microphone pic https://pixabay.com/photos/recording-studio-indoors-mic-1869560/

# Beats
Website is a dynamic web application that allows users to purchase high-quality beats from talented producers. The platform provides a seamless user experience, enabling visitors to explore producer profiles, listen to beats, and purchase them securely using Stripe. Users can also view producer information such as years of experience, primary instruments, and software used. The website is designed to cater to artists, content creators, and businesses looking for unique music production solutions by purchasing royalty free beats.

# Rationale 
The "Beats" website is designed to create a vibrant and interactive community platform for music enthusiasts. It provides a space for users to buy music 

## Key Features and Their Rationales

### User Authentication and Access Control
#### Registration & Login: 
Users can register and log in to access member-only features like purchasing beats, viewing profiles, and saving orders.

#### Profile Management: 
Users can edit their personal information and manage purchases through their profiles.

### Producer Profiles
Producer Information: Displays producer bio, skills, and equipment, such as software and hardware used.

Producer Cards: Each producer has a dedicated card on the "Our Producers" section, showcasing:Name, Years of production experience, Main instrument, Software expertise

### Beat Marketplace 
#### Browse Beats:
Users can browse beats and listen to previews.

#### Search & Filter: 
Users can search for beats by Price, title or producer.

### E-commerce (Powered by Stripe)
#### Secure Payments: 
Integration with Stripe ensures secure payments for beat purchases.

#### Order History:
 Users can view their purchase history from their profiles.

#### Instant Beat Download:
 After successful payment, users can download the purchased beats directly.

### Custom Beat Requests
Users can request customized beats from producers by filling out a contact form.
Producers can receive and respond to user requests via email.


# Beat Model

The Beat model represents individual music beats that can be listed, purchased, or streamed. It includes details like the beat's title, producer, price, and associated media files.

## Features

#### UUID for Unique Identification:
 Each beat is assigned a globally unique identifier (UUID) to ensure uniqueness and make URLs less predictable.

#### File Uploads:
 Supports uploading of both a cover image and an audio file. These files are stored in the static/covers/ and static/audio/ directories, respectively.

#### String Representation:
 The str method returns the title of the beat, making it easier to identify beats in the Django admin and other interfaces

 ## The Producer model 
 represents music producers who create beats. It tracks details about their experience, primary instruments, and preferred software.

 ### Years of Experience: 
 Tracks how long the producer has been creating music using a PositiveIntegerField.

### Software & Instrument Info:
 Provides insight into the producer's tools of the trade.

# User Stories
The purpose of Gig reviews is to let users display their thoughts on the musicians they have seen recently and to see any other reviews about gigs they maybe interesed in from other users

### User Goals
* To buy royalty free music
* To have a platform to purchase music for a fixed price with no royalty confusion
* To purchase music, using online payments
* To have the option to listen to the music before they purchase
* 

### Site Owner goals 

* To make a website where the site owner can upload own music for free and sell to the public
* Make a fully functioning online shop, where users can preview and purchase instrumentals
* Ensure that only logged-in users can buy instrumentals.
* Make a database where when users have stored their information it can be seen from the admin panel for the admin 
* To give the option for users to remove themselves off the database
* To see the amount of orders and order details on the admin panel 
* To keep track of payments using stripe 


# UX Design

For the colour scheme I have gone with a dark colour with white text, I think it looks more professional

# Data Schema Overview


 # WireFrames Desktop

 For the wireframes I didn't have a wireframe designer so I designed the app on Adobe Photoshop.
1. Wireframe for profile
![image](assets/docs/imagedocs/wireframe-profile.png)

2. Wireframe for mainpage
![image](assets/docs/imagedocs/wireframe-main-page.png)

# Features 

1. An admin dashboard for the admin to see the database
   ![image](assets/docs/imagedocs/admin-dash.png)
2. Blog form to submit a blog 
   ![image](assets/docs/imagedocs/feature-blog.png)
3. A nav bar so users can easily navigate the website
   ![image](assets/docs/imagedocs/feature-nav-bar.png)
4. Sign up form
   ![image](assets/docs/imagedocs/feature-sign-up.png)
5. login form
   ![image](assets/docs/imagedocs/login-feature.png)
## Future features
 For the future features I would like to add a shop page to the website where the user can click on the image and buy the image from the website and for it to be printed onto a canvas.

# Technologies Used 
* Google Fonts
* Adobe PhotoShop
* HTML
* AWS S3
* Django
* Python
* JS 
* CSS
* VSCode
* Code Anywhere 
* Github.com
* Git
* Font Awesome
* Am I Reponsive
* Jquery
* Jinja
* SQLite
* 

# Manual testing 

## Manual Testing Table for Sign-Up Page

| Action                         | Predicted Outcome                               | Outcome |
|:-------------------------------|:-----------------------------------------------:|--------:|
| Enter valid email              | Form accepts email and allows further input     | works   |
| Enter invalid email            | Displays error or prevents form submission      | works   |
| Enter valid first name         | Form accepts the first name and allows further input | works |
| Leave first name field empty   | Displays error or prevents form submission      | works   |
| Enter matching passwords       | Form accepts passwords and allows form submission | works |
| Enter non-matching passwords   | Displays error indicating passwords do not match | works   |
| Click submit with valid inputs | Form submits successfully, redirects to next page or shows success message | works |
| Click submit with invalid inputs | Form does not submit, displays appropriate error messages | works |
| Check CSRF token inclusion     | Form includes a valid CSRF token                | works   |

## Manual Testing Table for Login Page

| Action                         | Predicted Outcome                               | Outcome |
|:-------------------------------|:-----------------------------------------------:|--------:|
| Enter valid email              | Form accepts email and allows further input     | works   |
| Enter invalid email            | Displays error or prevents form submission      | works   |
| Enter valid password           | Form accepts the password and allows form submission | works |
| Leave password field empty     | Displays error or prevents form submission      | works   |
| Click login with valid inputs  | Form submits successfully, redirects to dashboard or home page | works |
| Click login with invalid inputs| Form does not submit, displays appropriate error messages | works |
| Check CSRF token inclusion     | Form includes a valid CSRF token                | works   |

## Manual Testing Table for Profile Page

| Action                                      |                  Predicted Outcome                         |  Outcome  |
|:--------------------------------------------|:----------------------------------------------------------:|----------:|
| View Profile Page                           | User's first name and email are displayed correctly         | works     |
| Log in as Admin and view Profile Page       | "Go to Admin Panel" link is visible and functional          | works     |
| Log in as Non-Admin and view Profile Page   | "Go to Admin Panel" link is not visible                     | works     |
| Submit "Delete Profile" form                | Profile is deleted after confirmation prompt                | works     |
| Submit "Delete Profile" form without CSRF   | Form submission fails, CSRF token error is shown            | works     |
| Add a gig review with valid inputs          | Review is successfully added and displayed                  | works     |
| Add a gig review with empty fields          | Form displays error messages, does not submit               | works     |
| Add a gig to wishlist                       | Gig is added to the wishlist and appears in the list        | works     |
| Delete a gig from wishlist                  | Gig is removed from the wishlist                            | works     |
| Edit a gig in wishlist                      | Gig's details are updated and changes are reflected         | works     |
| Submit a wishlist form without CSRF         | Form submission fails, CSRF token error is shown            | works     |
| Attempt to delete a profile without confirmation | Profile is not deleted, stays intact                      | works     |

## Manual Testing Table for Home Page

| Action                                      |                  Predicted Outcome                         |  Outcome  |
|:--------------------------------------------|:----------------------------------------------------------:|----------:|
| View Home Page                              | Page displays a title, intro section, and content based on user status | works     |
| Visit page as unauthenticated user          | Login prompt with sign-up and sign-in options are displayed | works     |
| Visit page as authenticated user            | Login prompt is not visible; user sees gig beats and options to buy beats | works     |
| beat cards are editble for authenticated admin                    | Beats are listed with title, content, author, and are editable | works     |
| Attempt to edit a beat as admin       | Edit option is visible and functional for the admin   | works     |
| Attempt to delete a beat as admin    | Delete option is visible and functional for the post owner  | works     |
| Attempt to edit/delete a beat as non-owner  | Edit and Delete options are not visible for non-owners      | works     |
| Attempt to edit/delete a beat as admin      | Edit and Delete options are visible and functional for admin | works     |
| Submit any form without CSRF token          | Form submission fails, CSRF token error is shown            | works     |
| click play button underneath song                | plays the beat corosponding to the song                | works     |
| View post without comments                  | "No comments yet" message is displayed                      | works     |
| View page with no blog posts                | "No reviews available" message is displayed                 | works     |



## W3C Validation 
Managed to fix these few errors by finding the lines of code referenced on the page and removing the stray tags and correctly formating the code. Here are the results. 


![image](assets/docs/imagedocs/edit-blog-post.png)

![image](assets/docs/imagedocs/edit-note.png)

![image](assets/docs/imagedocs/login.png)

![image](assets/docs/imagedocs/sign-up-valid.png)



### Lighthouse Report 
![image](assets/docs/imagedocs/lighthouse.png)
Lighthouse report.

# Challenges and Bugs

1. CRSF Token wasn't in the right line of code
![image](assets/docs/imagedocs/bug-docs/crsf-token.png)

2. Url endpoints ended up conflicting and throwing the app off until i changed the route
![image](assets/docs/imagedocs/bug-docs/end-point.png)
![image](assets/docs/imagedocs/bug-docs/end-points.png)

3. import bugs, resolved when I used captials correctly
![image](assets/docs/imagedocs/bug-docs/import-error.png)

4. added user id later in the database and it wasnt being reconigzed until I migrated the database
![image](assets/docs/imagedocs/bug-docs/no-user-id.png)

5. SQL wasn't installed properly 
![image](assets/docs/imagedocs/bug-docs/hadnt-installed-sql.png)

6. note wasn't imported at the top of the page.
![image](assets/docs/imagedocs/bug-docs/note-not-defined.png)
![alt text](assets/docs/imagedocs/bug-docs/note-not-defined-solution.png)

I had made a previous account called "Twinwinter" on my email address robertwinterburn@hotmail.co.uk and I had made a new account to make my name a bit more professional and readable (RWinterburn) but when I started making commits they came from "Twinwinter" on one and "RWinterburn" from another I don't know wether it was to do with me from switching from gitpod.io and codeanywhere to VScode need to figure this problem out for future developments as I haven't figured it out yet. So you will see commits from both of my Github accounts, dont think this has happened again. Resolved by git.

I did run into a problem I had to sign up for gitpod.io with my student account after I already had started my website so there will be a commit name saying "RWinterburn2" it is linked to my student email.

I tried signing up for Heroku so I had to find alternatives and it slowed my project to a halt for a few days finding a solution asked for an extended deadline on the project but I only managed to get a request form in at the last minute(Managed to fix heroku by starting new account unfortunately im getting charged at the minute though for add ons)



# Am I responsive 

![alt text](assets/docs/imagedocs/am-i-responsive.png) 
Am I Responsive test

# Deployment and Development 

### Heroku deployment 


* Login: Open your terminal and log in to Heroku: heroku login
* Create an App: heroku create gig-reviews 
* Deploy: git push heroku main 
* View: heroku open


### Deployment 

To deploy the website the user must 
* Log in to Github.com.
* Go to "settings".
* Click "pages" under "codes and automation".
* Select "deploy from a branch" and select the "main" branch.
* Then select "/(root)" 
* Click "save" to save the Github page source.
* Go to "code".
* Click on the yellow circle on the page repository.
* You will see the backend working on building the website when this is complete go to "settings"
* Click "pages" 
* You should see the website link https://rwinterburn.github.io/project-3
* Click on the link and you will see the website.


### Deployment on Cloud Flare
Currently isn't working asked for an extension on deadline to resolve

### Development 
For future development go to https://github.com/RWinterburn/project-3
* Click the green "code" button.
* Copy the URL
* Go to your cloud based coding site. e.g. Code Anywhere or Gitpod.io
* click on "new workspace". 
* Paste in the repository URL
* Click create and it will create the code space for you.

#### VSCode Development
For future development go to https://github.com/RWinterburn/project-3
* Click the green "code" button.
* Copy the URL
* Open "command palette in VSCode (CTRL + SHIFT + P)
* Click the option "Git Clone"
* Click "clone from Github"
* Paste in the Repository URL 
* Hit "Enter"
* A window will pop up on your computer asking you to choose you repository destination, choose an appropriate folder. 
* Select the repository destination and the workspace will click open. 
* You may get the option saying "Do you trust this author? click Yes"

# Tutorials Used & external code implimented
Code has been partially used from these websites, most of the time when I first implimented it it wouldn't work as intended until I changed the parameters.
* W3Schools
* Stackoverflow
* YouTube: https://www.youtube.com/watch?v=dam0GPOAvVI
* Chat GPT



