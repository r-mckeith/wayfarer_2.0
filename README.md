# [Wayfarer](https://the-wayfarer.herokuapp.com/)

## PROJECT OVERVIEW 
Wayfarer is an exciting travel blog that allows users to experience the world without ever having to leave their home. 

### PREVIEW 

![home page large](https://user-images.githubusercontent.com/77288642/112135037-936bdf00-8b8a-11eb-9735-c0080cdf3f6c.png)

![city show large](https://user-images.githubusercontent.com/74464186/111948572-9ab4bf00-8a9c-11eb-9894-33d3f4c7507e.png)

![comments large](https://user-images.githubusercontent.com/74464186/111949343-c4bab100-8a9d-11eb-8ce2-093d36a7edfd.png)

### Mobile responsiveness: 

![mobile responsiveness 2 views](https://user-images.githubusercontent.com/77288642/112134758-4556db80-8b8a-11eb-992d-16d7ff8ac2d9.png)


# Wayfarer
([click here for the link to our project hosted on Heroku!](https://the-wayfarer.herokuapp.com/))

### What can users do?    
New visitors can instantly view cities and read reviews written by others.
They are encouraged to sign up so that they can to write their own reviews, 
comment on other reviews, even reply to comments!  Logged in users can see
a history of their posts on their profile page, and they can also see others'
profiles!

#### Languages and Framework
* Python
* Django
* SQL
* Materialize
* HTML/CSS
* Javascript


## USER STORIES:
(For this project user stories and basic wire frames were provided.)

#### Sprint 1: Basic Auth & Profiles
###### A user should be able to:
- Navigate to "/" and see a basic splash page with:
  - The name of the website.
  - Links to "Log In" and "Sign Up".
- Sign up for an account.
- Log in to their account if they already have one.
- Be redirected to their public profile page after logging in.
- On their public profile page, see their name, the current city they have set in their profile, and - their join date.
- See the site-wide header on every page with:
- A link to "Log Out" if they're logged in.
- Links to "Log In" and "Sign Up" if they're logged out.
- Update their profile by making changes to their name and/or current city.
- See the titles of all the posts they've contributed (start with pre-seeded data).
- Click on the title of one of their posts and be redirected to a "show" page for that post.
- View post "show" pages with title, author, and content.

#### Sprint 2: CRUD
###### A user should be able to:
- View the "San Francisco" page (at "/cities/1") including:
  - The site-wide header.
  - The name of the city.
  - An iconic photo of the city.
- View a list of posts on the San Francisco page:
  - Sorted by newest first.
  - With the post titles linked to the individual post "show" pages.
- Use an "Add New Post" button on the San Francisco city page to pull up the new post form.
- Create a new post for San Francisco.
- Click "Edit" on ANY individual post, and be redirected to the edit form.
- Click "delete" on ANY individual post, then:
  - See a pop-up that says: "Are you sure you want to delete #{title}?"
  - If the user confirms, delete the post.

#### Sprint 3: Validations & Authorization
###### A user should be able to:
- View city pages for "London" and "Gibraltar".
- Verify that a new post they create is successfully published on the correct city page.
###### A user CANNOT save invalid data to the database, according to the following rules:
- A user CANNOT sign up with an email (or username) that is already in use.
- A post's title must be between 1 and 200 characters.
- A post's content must not be empty.
###### A user is authorized to perform certain actions on the site, according to the following rules:
- A user MUST be logged in to create/update/destroy resources.
- A user may only edit their own profile and edit/delete their own posts.

## MODELS:

#### User Model

| Column Name | Data Type | Notes |
| --------------- | ------------- | ------------------------------ |
| id | Integer | Serial Primary Key, Auto-generated |
| username | CharField | Must be provided |
| password | CharField | Stored as a hash |


#### City Model

| Column Name | Data Type | Notes |
| --------------- | ------------- | ------------------------------ |
| id | IntegerField | Serial Primary Key, Auto-generated |
| name | CharField | Must be provided |
| photo_url | CharField | Must be provided |
| slug | SlugField | Auto-generated |


#### Post Model

| Column Name | Data Type | Notes |
| --------------- | ------------- | ------------------------------ |
| id | IntegerField | Serial Primary Key, Auto-generated |
| title | CharField | Must be provided |
| body | TextField | Must be provided |
| created_at | DateTimeField | Auto-generated |
| city | IntegerField | ForeignKey, Pulled from City DB |
| user | IntegerField | ForeignKey, Pulled from User DB |


#### Comment Model 

Column Name | Data Type | Notes |
| ---------------- | ------------- | -------------- |
| id | Integer | Serial Primary Key, Auto-generated |
| post | IntegerField | Foreign Key, Pulled from Post DB |
| user | IntegerField | Foreign Key, Pulled from User DB |
| created_at | DateTimeField | Auto-generated |
| content | TextField | Must be provided |
| reply | Integer | Foreign Key, Self-referencing |

#### Profile Model (Extends User Model) 

Column Name | Data Type | Notes |
| ---------------- | ------------- | -------------- |
| id | Integer | Serial Primary Key, Auto-generated |
| user | OneToOneField | Foreign Key, Pulled from User DB |
| current_city | CharField | Must be provided |
| first_name | CharField | Must be provided |
| last_name | CharField | Must be provided |
| photo_url | CharField | Must be provided |


### INSTALLATION INSTRUCTIONS

##### 1. FORK AND CLONE RESPOSITORY TO YOUR GITHUB AND LOCAL REPOSITORY

##### 2. OPEN REPOSITORY AND CREATE A VIRTUAL ENVIRONMENT
RUN THE FOLLOWING CODE:

```
source .env/bin/activate
```

##### 3. INSTALL DEPENDENCIES
RUN THE FOLLOWING CODE:

```
pip3 install -r requirements.txt
```

##### 3. CREATE NEW DATABASE NAMED: wayfarer
RUN THE FOLLOWING CODE:

```
createdb: wayfarer
```

##### 4. RUN THE MIGRATIONS
RUN THE FOLLOWING CODE:

```
python3 manage.py db:migrate
```

### Challenge/Triumph: Threaded Comments
Making a comment to a post is easy enough.  But how about a reply to comment?
A reply to that reply?  A rely to that reply of that reply?  Threaded comments
are tricky (and very cool). Although a user can make a post, comment to a post, 
and reply to a comment, a user MAY NOT reply to a reply. That functionality is 
a work in progress. Here is a look at the comment model (Notice how 'reply' 
references 'self'):
```
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  content = models.TextField()
  reply = models.ForeignKey('self', on_delete = models.CASCADE, null=True, blank=True, related_name='replies')
  is_parent = models.BooleanField(null=True)
```

### Challenge/Triumph: Making Modal Reappear After Leaving a Comment
Imagine you make a comment in a modal, but after you submit the comment, the modal
disappears!  Annoying!  How do I make the modal reappear? First, I looked at the 
comment_new view, where I stored the post modal id in request.session.
`request.session['yourKeyHere'] = 'yourValueHere (does not have to be string)'`
When my template loads, I use javascript to create a modal trigger that clicks itself. 
(I feed in the id I stored in request.session)
```
if ('{{request.session.modeltoopen}}' !== '') {
    const modalTrigger = document.createElement('a')
    modalTrigger.setAttribute('class', 'modal-trigger')
    modalTrigger.setAttribute('href', '#post-modal{{request.session.modeltoopen}}')
    document.body.appendChild(modalTrigger)
    modalTrigger.click()
    modalTrigger.remove()
}
```

### Thoughts
##### A city page with no posts?
When you reach the landing page, the images of those cities are not ordered
by number of posts! This means that there is a good chance you will click a 
city with no posts, and leave disheartened. Until this is fixed, I advise that
you use the search/drop-down bar on top, which actually orders the cities based 
on number of posts!
##### A city review site with hardly any cities?
Another main worry for the site is that the cities are hard-coded, which
really limits the city choices that users have to interact with. A 
great idea for a future update would be to implement an API that grabs
city names from anywhere in the world.  Combine that with good search
functionality, and wala!  
##### Imperfections?
Of course, there are a ton of smaller improvements that could be made throughout
the site, but deadlines must be set and met! Thanks for checking out the details 
of this project! Have a good one!

### Contributor Links
##### Ryan McKeith
- [Github](https://github.com/r-mckeith)
- [Linkedin](https://www.linkedin.com/in/rmckeith/)
##### Richard Ng
- [Github](https://github.com/richardkentng)
- [Linkedin](https://www.linkedin.com/in/richard-kent-ng/)