// capitalize the first letter
export function capitalize(word) {
  if (!word) return ''
  return word.charAt(0).toUpperCase() + word.slice(1)
}

export function isValidName(name) {
  return /^[A-Za-zÀ-ÖØ-öø-ÿ\s']+$/.test(name)
}

export function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
