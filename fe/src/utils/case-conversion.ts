const toCamel = (s: string) => {
    return s.replace(/([_][a-z])/gi, ($1: string) => {
        return $1.toUpperCase().replace('_', '')
    })
}

const toSnake = (s: string) => {
    return s.replace(/(.)([A-Z])/g, (_: any, $2: any, $3: string) => {
        return `${$2}_${$3.toLowerCase()}`
    })
}

const isArray = function (a: any) {
    return Array.isArray(a)
}

const isObject = function (o: any) {
    return o === Object(o) && !isArray(o) && typeof o !== 'function'
}

const keysToCamel = function (o: Object): Object {
    if (isObject(o)) {
        const n = {}

        Object.keys(o).forEach((k: string) => {
            n[toCamel(k)] = keysToCamel(o[k])
        })

        return n
    }

    return o
}

const keysToSnake = function (o: Object): Object {
    if (isObject(o)) {
        const n = {}

        Object.keys(o).forEach((k: string) => {
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
