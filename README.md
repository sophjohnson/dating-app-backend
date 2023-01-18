# RecommeND Dating App - Backend

## Database Setup

### Requirements:
1. Oracle

### Build Database

Create Oracle user:

Build database:
> $ ./database/build.sh

## API Setup

### Requirements:
1. Python >= 3.6
2. Pip3

### Start API

Initialize virtual environment:
> $ source ./api/.venv/bin/activate

Install requirements (inside virtual environment):
> (.venv) $ pip3 install -r ./api/requirements.txt

Run app:
> (.venv) $ gunicorn -b 0.0.0.0:8800 api.api.app --reload

## API Documentation
| Request | Endpoint | Input Example | Output Example | Description |
| --- | --- | --- | --- | --- |
| GET | /states/ | | [{"code": "AL", "name": "Alabama"}, {"code": "AK", "name": "Alaska"}, {"code": "AZ", "name": "Arizona"},...] | Get all states |
| GET | /dorms/ | | [{"dorm": "Alumni Hall", "quad": "South Quad", "airConditioning": 0, "logo": null, "mascot": "Alumni Hall"},...] | Get all dorms |
| GET | /majors/ | | ["Accountancy", "Aerospace Engineering",...] | Get all majors |
| GET | /minors/ | | ["AL/SC Honors Program", "Accounting",...] | Get all minors |
| GET | /masses/ | | [{"massID": 1, "location": "Dunne Hall", "day": "Sunday", "time": "4 p.m."},...] | Get all masses |
| POST | /students/ | {<br>&emsp;"netid": "sjohns37",<br>&emsp;"password": "12345"<br>}|  | Register new student |
| POST | /students/:netid | Body: binary image file|  | Upload student profile picture |
| GET | /students/:netid | | {<br>&emsp;"netid": "sjohns37",<br>&emsp;"firstName": "Sophie",<br>&emsp;"lastName": "Johnson",<br>&emsp;"gradYear": "2020",<br>&emsp;"majors": [<br>&emsp;&emsp;"Computer Science"<br>&emsp;],<br>&emsp;"minors": [],<br>&emsp;"city": "Cadillac",<br>&emsp;"state": "MI",<br>&emsp;"dorm": "Badin",<br>&emsp;"genderIdentity": "female",<br>&emsp;"browseGenderIdentity": [<br>&emsp;&emsp;"male"<br>&emsp;],<br>&emsp;"funFacts": [<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"id": 1,<br>&emsp;&emsp;&emsp;"netid": "sjohns37",<br>&emsp;&emsp;&emsp;"caption": "I like ceramics",<br>&emsp;&emsp;&emsp;"image": "sjohns37_1.jpe"<br>&emsp;&emsp;},<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"id": 2,<br>&emsp;&emsp;&emsp;"netid": "sjohns37",<br>&emsp;&emsp;&emsp;"caption": "I like strawberries",<br>&emsp;&emsp;&emsp;"image": "sjohns37_2.jpe"<br>&emsp;&emsp;}<br>&emsp;],<br>&emsp;"question": "What’s up?",<br>&emsp;"image": "sjohns37_0.jpe",<br>&emsp;"danceInvite": 0,<br>&emsp;"temperament": "ambiverted",<br>&emsp;"giveAffection": "touch",<br>&emsp;"trait": "compassionate",<br>&emsp;"idealDate": "lakes",<br>&emsp;"fridayNight": "chat",<br>&emsp;"diningHall": "SDH",<br>&emsp;"studySpot": "duncan",<br>&emsp;"mass": "never",<br>&emsp;"club": "artistic",<br>&emsp;"gameDay": "kegs",<br>&emsp;"hour": "6",<br>&emsp;"zodiacSign": "scorpio",<br>&emsp;"idealTemperament": "ambiverted",<br>&emsp;"receiveAffection": "gifts",<br>&emsp;"idealTrait": "funny"<br>} | Get all profile information and preferences for a student |
| PUT | /students/:netid | {<br>&emsp;"question": “How are you?",<br>&emsp;"trait": "funny",<br>&emsp;"majors": [<br>&emsp;&emsp;"Computer Science",<br>&emsp;&emsp;“Russian”<br>&emsp;]<br>}|  | Update a student’s profile or preferences |
| POST | /schedules/ | Body: binary .ics file|  | Upload student’s academic calendar to parse courses and lunch times |
| POST | /funfacts/:netid | Parameters: caption<br>Body: binary image file|  | Create new fun fact |
| GET | /funfacts/:netid | | [<br>&emsp;{<br>&emsp;&emsp;"id": 1,<br>&emsp;&emsp;"netid": "sjohns37",<br>&emsp;&emsp;"caption": "I like ceramics",<br>&emsp;&emsp;"image": "sjohns37_1.jpe"<br>&emsp;},<br>&emsp;{<br>&emsp;&emsp;"id": 2,<br>&emsp;&emsp;"netid": "sjohns37",<br>&emsp;&emsp;"caption": "I like strawberries",<br>&emsp;&emsp;"image": "sjohns37_2.jpe"<br>&emsp;}<br>] | Get all of a student’s fun facts |
| PUT | /funfacts/:netid/:id | Parameters: caption<br>Body: binary image file|  | Updates caption or photo of fun fact |
| DEL | /funfacts/:netid/:id | | | Deletes a fun fact given netid and id |
| GET | /images/:path | | Body: binary image file | Gets an image based on path |
| POST | /login/ | {<br>&emsp;"netid": "sjohns37",<br>&emsp;"password": "12345"<br>}|  | Validates netid and password combination |
| PUT | /login/ | {<br>&emsp;"netid": "sjohns37",<br>&emsp;"oldPassword": "12345",<br>&emsp;"newPassword": "abcd"<br>}|  | Updates password (is old password provided is correct) |
| POST | /request/ | {<br>&emsp;"sender": "sjohns37",<br>&emsp;"receiver": "alamber2"<br>}|  | Sends request from sender asking receiver to become a recommender |
| GET | /request/ | Parameters: netid | {<br>&emsp;"requestsReceived": [<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"sender": "sjohns37",<br>&emsp;&emsp;&emsp;"firstName": "Sophie",<br>&emsp;&emsp;&emsp;"lastName": "Johnson"<br>&emsp;&emsp;}<br>&emsp;],<br>&emsp;"requestsSent": [<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"receiver": "alamber2",<br>&emsp;&emsp;&emsp;"firstName": "Ana Luisa",<br>&emsp;&emsp;&emsp;"lastName": "Lamberto"<br>&emsp;&emsp;}<br>&emsp;]<br>} | Get all requests sent and received by a student |
| PUT | /request/ | {<br>&emsp;"sender": "sjohns37",<br>&emsp;"receiver": "alamber2",<br>&emsp;"status" : "accept"<br>}|  | Updates status of a request by creating a recommender if accepted then deleting the request |
| GET | /recommenders/:netid | | {<br>&emsp;"recommenders": [<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"netid": "alamber2",<br>&emsp;&emsp;&emsp;"firstName": "Ana",<br>&emsp;&emsp;&emsp;"lastName": "Lamberto"<br>&emsp;&emsp;}<br>&emsp;],<br>&emsp;"recommendees": [<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"netid": "sjohns37",<br>&emsp;&emsp;&emsp;"firstName": "Sophie",<br>&emsp;&emsp;&emsp;"lastName": "Johnson"<br>&emsp;&emsp;},<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"netid": "merdenbe",<br>&emsp;&emsp;&emsp;"firstName": "Mike",<br>&emsp;&emsp;&emsp;"lastName": "Erdenberger"<br>&emsp;&emsp;}<br>&emsp;]<br>} | Get all students who can recommend for the given netid and all students who the given netid can recommend for |
| DEL | /recommenders/ | {<br>&emsp;"recommender": "sjohns37",<br>&emsp;"recommendee": "alamber2"<br>}|  | Deletes recommender relationship |
| POST | /browse/ | {<br>&emsp;"viewedFor": "sjohns37",<br>&emsp;"netid": "merdenbe",<br>&emsp;"viewedBy": "alamber2",<br>&emsp;"status": "recommend"<br>}|  | Updates status of profile viewed by either creating a recommendation or skipping to the next profile |
| GET | /browse/ | Parameters: viewFor, viewBy | <br>{<br>&emsp;"netid": "merdenbe",<br>&emsp;"firstName": "Mike",<br>&emsp;"lastName": "Erdenberger",<br>&emsp;"gradYear": "2020",<br>&emsp;"majors": [<br>&emsp;&emsp;"Computer Science"<br>&emsp;],<br>&emsp;"minors": [],<br>&emsp;"city": "Chester",<br>&emsp;"state": "NJ",<br>&emsp;"dorm": "Stanford",<br>&emsp;"question": "Do you even row?",<br>&emsp;"image": "merdenbe_0.jpe",<br>&emsp;"funFacts": [<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"id": 21,<br>&emsp;&emsp;&emsp;"netid": "merdenbe",<br>&emsp;&emsp;&emsp;"caption": "I like bikes",<br>&emsp;&emsp;&emsp;"image": "merdenbe_21.jpe"<br>&emsp;&emsp;},<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"id": 22,<br>&emsp;&emsp;&emsp;"netid": "merdenbe",<br>&emsp;&emsp;&emsp;"caption": I like plants",<br>&emsp;&emsp;&emsp;"image": "merdenbe_22.jpe"<br>&emsp;&emsp;}<br>&emsp;],<br>&emsp;"danceInvite": 1,<br>&emsp;"compatibilityScore": 70.59<br>} | Get next profile to potentially recommend for your friend with highest compatibility score that has not been viewed already |
| GET | /recommendation/ | Parameters: netid | {<br>&emsp;"netid": "merdenbe",<br>&emsp;"firstName": "Mike",<br>&emsp;"lastName": "Erdenberger",<br>&emsp;"gradYear": "2020",<br>&emsp;"majors": [<br>&emsp;&emsp;"Computer Science"<br>&emsp;],<br>&emsp;"minors": [],<br>&emsp;"city": "Chester",<br>&emsp;"state": "NJ",<br>&emsp;"dorm": "Stanford",<br>&emsp;"question": "Do you even row?",<br>&emsp;"image": "merdenbe_0.jpe",<br>&emsp;"funFacts": [<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"id": 21,<br>&emsp;&emsp;&emsp;"netid": "merdenbe",<br>&emsp;&emsp;&emsp;"caption": "I like bikes",<br>&emsp;&emsp;&emsp;"image": "merdenbe_21.jpe"<br>&emsp;&emsp;},<br>&emsp;&emsp;{<br>&emsp;&emsp;&emsp;"id": 22,<br>&emsp;&emsp;&emsp;"netid": "merdenbe",<br>&emsp;&emsp;&emsp;"caption": I like plants",<br>&emsp;&emsp;&emsp;"image": "merdenbe_22.jpe"<br>&emsp;&emsp;}<br>&emsp;],<br>&emsp;"danceInvite": 1,<br>&emsp;"recommendedBy": "Ana Lamberto",<br>&emsp;"compatibility": 70.59,<br>&emsp;"courses": 0,<br>&emsp;"lunches": 0<br>} | Get profile of next recommendation |
| PUT | /recommendation/ | {<br>&emsp;"viewer": "sjohns37",<br>&emsp;"viewee": "alamber2",<br>&emsp;"status": "interested",<br>&emsp;"message": "hi hot stuff"<br>}|  | Updates status of recommendation by either sending a message or skipping to next recommendation |
| GET | /conversations/:netid | | [<br>&emsp;{<br>&emsp;&emsp;"id": 1,<br>&emsp;&emsp;"netid": "alamber2",<br>&emsp;&emsp;"firstName": "Ana",<br>&emsp;&emsp;"lastName": "Lamberto",<br>&emsp;&emsp;"sender": "sjohns37",<br>&emsp;&emsp;"receiver": "alamber2",<br>&emsp;&emsp;"content": "hi ana",<br>&emsp;&emsp;"timestamp": "04/28/20, 11:31 PM"<br>&emsp;}<br>] | Get all conversations with details for student |
| POST | /messages/ | | {<br>&emsp;"sender": "sjohns37",<br>&emsp;"receiver": "merdenbe",<br>&emsp;"content": "Hi there!"<br>} | Creates new message |
| GET | /messages/:id | | | Gets all messages based on conversation id |
| GET | /compatibility/ | Parameters: viewer, viewee | {<br>&emsp;"compatibility": 50,<br>&emsp;"courses": [<br>&emsp;&emsp;"Advanced Database Projects"<br>&emsp;],<br>&emsp;"lunches": [<br>&emsp;&emsp;"Monday from 11:00 AM - 02:00 PM",<br>&emsp;&emsp;"Tuesday from 11:00 AM - 12:30 PM",<br>&emsp;&emsp;"Thursday from 11:00 AM - 12:30 PM",<br>&emsp;&emsp;"Friday from 11:00 AM - 02:00 PM"<br>&emsp;],<br>&emsp;"messages": [<br>&emsp;&emsp;"Go Bullfrogs, amirite?!",<br>&emsp;&emsp;"I'd walk all the way from Lewis to Pasquerilla Center for you",<br>&emsp;&emsp;"Two scorpio signs are better than one.",<br>&emsp;&emsp;"Okay, real talk... NDH > SDH"<br>&emsp;],<br>&emsp;"mass": false<br>} | Gets compatibility score, shared courses, overlapping lunch breaks, generated messages, and mass attendance for a given pair of students
