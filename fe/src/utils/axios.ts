import axios from 'axios'

function getCookie(name: String) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export const instance = axios.create({
  withCredentials: true,
  //'https://sel2-5.ugent.be/api/' 'http://localhost:8000/api/'
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'X-CSRFToken': `${getCookie('csrftoken')}`
  }
})

export const setCsrfToken = () =>
    (instance.defaults.headers.common['X-CSRFToken'] =
        getCookie('csrftoken') || '')

export const hasCsrfToken = () => getCookie('csrftoken') !== null