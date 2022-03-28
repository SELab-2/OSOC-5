const toCamel = (s) => {
  return s.replace(/([_][a-z])/gi, ($1) => {
    return $1.toUpperCase().replace('_', '')
  })
}

const toSnake = (s) => {
  return s.replace(/(.)([A-Z])/g, (_, $2, $3) => {
    return `${$2}_${$3.toLowerCase()}`
  })
}

const isArray = function (a) {
  return Array.isArray(a)
}

const isObject = function (o) {
  return o === Object(o) && !isArray(o) && typeof o !== 'function'
}

const keysToCamel = function (o) {
  if (isObject(o)) {
    const n = {}

    Object.keys(o).forEach((k) => {
      n[toCamel(k)] = keysToCamel(o[k])
    })

    return n
  } else if (isArray(o)) {
    return o.map((obj) => keysToCamel(obj))
  }

  return o
}

const keysToSnake = function (o) {
  if (isObject(o)) {
    const n = {}

    Object.keys(o).forEach((k) => {
      // Ignore private variables as they start with an underscore.
      // These can be recursive references leading to a recursive loop.
      if (!k.startsWith('_')) {
        n[toSnake(k)] = keysToSnake(o[k])
      }
    })

    return n
  }

  return o
}

export {
  toSnake as convertStringToSnakeCase,
  keysToCamel as convertObjectKeysToCamelCase,
  keysToSnake as convertObjectKeysToSnakeCase,
}
