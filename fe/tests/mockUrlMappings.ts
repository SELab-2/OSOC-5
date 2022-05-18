let student = {
  "id": 1,
  "url": "https://sel2-5.ugent.be/api/students/1/",
  "suggestions": [
    {
      "suggestion": "0",
      "reason": "",
      "coach": {
        "url": "https://sel2-5.ugent.be/api/coaches/2/",
        "id": 2,
        "first_name": "F",
        "last_name": "V"
      }
    },
    {
      "suggestion": "0",
      "reason": "",
      "coach": {
        "url": "https://sel2-5.ugent.be/api/coaches/3/",
        "id": 3,
        "first_name": "L",
        "last_name": "S"
      }
    }
  ],
  "final_decision": null,
  "employment_agreement": "student",
  "hinder_work": "",
  "first_name": "Jan",
  "last_name": "Pieter",
  "call_name": "",
  "gender": "1",
  "pronouns": "",
  "email": "jan.pieter@example.com",
  "phone_number": "",
  "language": "Dutch",
  "english_rating": 5,
  "motivation": "Making money",
  "cv": "http://example.com",
  "portfolio": "http://example.com",
  "fun_fact": "I skateboard",
  "school_name": "UGent",
  "degree": "MaNaMa",
  "degree_duration": 3,
  "degree_current_year": 3,
  "studies": "Computer Science",
  "alum": false,
  "student_coach": false,
  "status": "0",
  "best_skill": "Back-end Dev",
  "skills": [
    "skills/2"
  ]
}
let coach1 = {
  id: 1, 
  role: "nope", 
  url: "test", 
  firstName: "test", 
  lastName: "test", 
  email: "test", 
  isAdmin: false, 
  isActive: true
}
let coach2 = {
  url: "https://sel2-5.ugent.be/api/coaches/2/",
  id: 2,
  first_name: "F",
  last_name: "V",
  role: "nope",
}
export const UrlMockMappingPost = {
    'auth/password/change/': {data: {succes: true}},
    'auth/login/': {data:{user:{pk:1}, refresh_token: "funky", access_token: "fresh"}},
    'auth/register/': {data: {user: "User was created!"}},
    'students/1/make_suggestion/': {data: {succes: true}},
    'students/${studentId}/make_final_decision/': {data: {succes: true}},
  }
export const UrlMockMappingGet = {
    'coaches/?page_size=500': {data:{results: [coach1]}},
    'coaches/?page=1': {data: {results: [coach1, coach2], next: null}},
    'coaches/1': {data:coach1},
    'coaches/2': {data:coach2},
    'coaches/': {data:{results: [coach1], count: 1}},
    'students/1/': {data: student
    },
    'students/?page=1': {data: {results: [student]}},
    "skills/2": {data: {name: "uitstelgedrag", id: 1, color: "green", url: "skills/2"}},
    'students/count/': {data: {counts: {yes: 2, no: 0, maybe: 1, undecided: 0, none: 0}}}
  }

export const UrlMockMappingPut = {
    'coaches/1/update_status/': {data: {succes: true}}
  }

export const UrlMockMappingDelete = {
    'students/1/remove_suggestion/': {data: {succes: true}},
    'coaches/1/': {data: {succes: true}},
    'student/1': {data: {succes: true}},
    'students/1/remove_final_decision/': {data: {succes: true}},
  }