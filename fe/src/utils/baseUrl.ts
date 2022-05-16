export const wsBaseUrl =
  process.env.NODE_ENV == 'development'
    ? 'ws://localhost:8000/ws/socket_server/'
    : 'wss://sel2-5.ugent.be/ws/socket_server/'

export const baseUrl =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/api/'
    : 'https://sel2-5.ugent.be/api/'
