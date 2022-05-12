export const UrlMockMappingPost = {
    'auth/password/change/': {data: {succes: true}},
    'auth/login/': {data:{user:{pk:1}, refresh_token: "funky", access_token: "fresh"}},
    'auth/register/': {data: {user: "User was created!"}},
  }
export const UrlMockMappingGet = {
    'coaches': {data:[{id: 1, role: "nope", url: "test", firstName: "test", lastName: "test", email: "test", isAdmin: false, isActive: true}]},
    'coaches/1': {data:{id: 1, role: "nope", url: "test", firstName: "test", lastName: "test", email: "test", isAdmin: false, isActive: true}}
  }

export const UrlMockMappingPut = {
    'coaches/1/update_status/': {data: {succes: true}}
  }

export const UrlMockMappingDelete = {
    'coaches/1/': {data: {succes: true}}
  }