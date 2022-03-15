interface User {
    firstName: string
    surname: string
    email: string
    isAdmin: boolean
    lastEmailSent: Date
    has_projects: Array<Object>
    suggestions: Array<Object>
}
