import axios from 'axios'

function getCookie(name: string) {
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
  baseURL:
    process.env.NODE_ENV == 'development'
      ? 'http://127.0.0.1:8000/'
      : 'https://sel2-5.ugent.be/',
  headers: {
    'X-CSRFToken': `${getCookie('csrftoken')}`,
  },
})

export const setCsrfToken = () =>
  (instance.defaults.headers.common['X-CSRFToken'] =
    getCookie('csrftoken') || '')

export const hasCsrfToken = () => getCookie('csrftoken') !== null
