# Flash.ME

## Welcome to Flash.ME!

### Inspiration
Studying for memorization-heavy exams, such as medical school and law school exams, can be incredibly taxing on students. While Anki is often the go-to study software endorsed by many productivity youtubers and medical school influencers, we found personally that it lacked visuals. Spending too long on a monotone UI can be even more taxing along with the weight of studying tons of information. While Quizlet is another strong choice, it lacks the crucial spaced-repetition algorithm of Anki to boost effective studying. We wanted to create something that combines the best of both worlds.

### What it does
This project aims to implement evidenced-based study strategies such as active recall and spaced repetition in a flashcard website while providing users with a fresh and intuitive UI. Users are able to sign in using OAuth and create flashcard sets. While studying, the program is actively analyzing the quality of their response with each flashcard, for example, how quick a user responds or how accurate it is. For example, low accuracy answers means the flashcard will appear again in a sooner study session.

Active Recall
: Testing yourself on information to improve it's strength in your long term memory

Spaced Repetition
: Spreading your study sessions over a period of time to combat the "forgetting curve"

### How we built it

We used Python and imported a spaced repetition algorithm module called SuperMemo2 on the back-end. SuperMemo2 provided us various values to determine the "spacing" and "repetition" in our study sessions. The values "quality" and "easiness" help determine the strength of a user's knowledge of a certain flashcard based on answer similarity and response time. The values "repetition" and "interval" help determine the next time a user will come across the flashcard in their study sessions in order to calculate a "review_date".

On the front-end, we used vue.js to build a responsive single-page website while using a combination of Sketch and Figma to design the user interace. User information, flashcard sets, and the flashcards were stored on a MongoDB database that can send or retrieve data at any time. We host our website on netlify.



### What we learned
* First time working with database storage and server hosting
* First time developing as a team, understanding each others' coding styles
* Front-end and back-end workflow
* Familiarized ourselves with new frameworks
* OAuth implementation


### Challenges we faced
* Been over a year since any of us have used Python
* Hosting collaboration sessions over different operating systems
* Trouble setting up the Python environment(we weren't able to get the right Python version to run)
* Implementing the algorithm for spaced repetition (determining quality and how easiness was calculated as well as the next study date)
* Linking our code to the database
* Git/GitHub commitment issues :sob:
* Authorization error when trying to log on to OAuth from different IPs
* Unfamiliarity with frameworks
* Passing from front-end to back-end and vice versa
* connecting database to frontend 

### Accomplishments we're proud of
* The design turned out amazing. We're really happy with how it looks!
* Lots of growth as software engineers in a short amount of time
* Bringing a product to the market thats applicable and useful

### What's next for Flash.ME
* Text to speech function
* Image support
* Ability to undo and override misclicks
* Improve precision by accounting for time of day
* Make project name more G rated

### Built with:
* Back-end: Python
* Front-end: JavaScript (vue.js?)
* MongoDB
* Postman
* Figma
* Heroku
* ngrok

#### The team:
* Pranav Grover
* Tan Huynh
* Christopher Linscott
* Bowen Tang
* Edmund Zhi
