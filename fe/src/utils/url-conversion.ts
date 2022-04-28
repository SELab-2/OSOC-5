// Extracts the id form a url and converts it to a number.
// If there's no id part in the url a -1 is returned instead.
export const urlToId = (url: string) =>
  Number.parseInt(url.split('/').at(-2) ?? '-1')
