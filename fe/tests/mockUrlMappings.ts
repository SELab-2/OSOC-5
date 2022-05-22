let student = {
  "id": 1,
  "url": "students/1/",
  "suggestions": [
    {
      "suggestion": "0",
      "reason": "",
      "coach": {
        "url": "coaches/2",
        "id": 2,
        "first_name": "F",
        "last_name": "V"
      }
    },
    {
      "suggestion": "0",
      "reason": "",
      "coach": {
        "url": "coaches/3",
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
  url: 'coaches/1', 
  firstName: "test", 
  lastName: "test", 
  email: "test", 
  isAdmin: false, 
  isActive: true
}
let coach2 = {
  url: 'coaches/1',
  id: 2,
  first_name: "F",
  last_name: "V",
  role: "nope",
}
let skill1 = {
  name: "uitstelgedrag",
  id: 1, 
  color: "green", 
  url: "skills/2"
}
let skill2 = {
  name: "Zuid-Afrikaanse Salamander kweker",
  id: 2, 
  color: "green", 
  url: "skills/3"
}
let mail1 = {
  id: 1,
  info: "test",
  type: 1,
  receiver: "NOPE",
  sender: 'coaches/1',
  time: new Date("2019-01-16"),
  url: "emails/1"
}
let projectSuggestion = {
  student: 'students/1/',
  coach: coach1,
  skill: "skills/2",
  reason: "woop woop",
  coachId: 1,
  coachName: "test",
}

let project = {
  name: "YUPPERS",
  partnerName: "regen",
  extraInfo: "liever niet",
  requiredSkills: [{amount: 2, comment: "test", skill: 'proj_skills/1'}],
  coaches: [coach1],
  suggestedStudents: [projectSuggestion],
  id: 1
}

let project_extra = {
  name: "YUPPERS VERVOLG",
  partnerName: "regen",
  extraInfo: "liever niet",
  requiredSkills: [{amount: 2, comment: "test", skill: 'proj_skills/1'}],
  coaches: [coach2],
  suggestedStudents: [projectSuggestion],
  id: 2
}


export const UrlMockMappingPost = {
    'auth/password/change/': {data: {succes: true}},
    'auth/login/': {data:{user:{pk:1}, refresh_token: "funky", access_token: "fresh"}},
    'auth/register/': {data: {user: "User was created!"}},
    'students/1/make_suggestion/': {data: {succes: true}},
    'students/${studentId}/make_final_decision/': {data: {succes: true}},
    'skills/': {data: {skill: "Skill was created!"}},
    'students/bulk_status/': {data: {user: "Users were updated!"}},
    'emails/': {data: {email: "Emails were updated!"}},
    'projects/1/remove_student/': {data: {student: "removed suggestion!"}},
    "projects/": {data: {succes: true}},
  }

export const UrlMockMappingGet = {
    'coaches/?page_size=500': {data:{results: [coach1]}},
    'coaches/?page=1': {data: {results: [coach1, coach2], next: null}},
    'coaches/1': {data:coach1},
    'coaches/2': {data:coach2},
    'coaches/': {data:{results: [coach1], count: 1}},
    'students/1/': {data: student},
    'students/?page=1': {data: {results: [student]}},
    'students/': {data: {results: [student], count: 1}},
    "skills/2": {data: skill1},
    "skills/3": {data: skill2},
    'students/count/': {data: {counts: {yes: 2, no: 0, maybe: 1, undecided: 0, none: 0}}},
    'skills/?page_size=500': {data: {results: [skill1, skill2]}},
    'skills/?page=1': {data: {results: [skill1, skill2]}},
    'emails/': {data: {results: [mail1]}},
    'emails/1': {data: mail1},
    'projects_sug/1': {data: projectSuggestion},
    'projects/': {data: {results: [project]}},
    'projects/1': {data: project},
    'projects/2': {data: project_extra},
    'projects/1/': {data: project},
    'projects/2/': {data: project_extra},
    'projects/?page=1': {data: {results: [project], next: null}},
    'projects/get_conflicting_projects': {data: {results: [{student: 'students/1/', projects: ['projects/1/', 'projects/2/']}]}},
    'proj_skills/1': {data: {amount:2, comment: "test", skill: "skills/2"}},
    'coaches/export_csv': {data: {succes: true}},
    'emails/export_csv': {data: {succes: true}},
    'projects/export_csv': {data: {succes: true}},
    'skills/export_csv': {data: {succes: true}},
    'students/export_csv': {data: {succes: true}},
    'students/export_csv_suggestion': {data: {succes: true}},
  }

export const UrlMockMappingPut = {
    'coaches/1/update_status/': {data: {succes: true}}
  }

export const UrlMockMappingDelete = {
    'students/1/remove_suggestion/': {data: {succes: true}},
    'coaches/1/': {data: {succes: true}},
    'student/1': {data: {succes: true}},
    'students/1/remove_final_decision/': {data: {succes: true}},
    'skills/1/': {data: {succes: true}},
  }

export const UrlMockMappingPatch = {
    "skills/1/": {data: {succes: true}},
    'students/1/': {data: {succes: true}},
    'projects/1/': {data: {succes: true}},
  }