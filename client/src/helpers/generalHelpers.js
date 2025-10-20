
// TODO: add alert functions to the store
export function showAlert(visible, type, message) {
  visible.value = true

  setTimeout(() => {
    visible.value = false
    type.value = []
    message.value = []
  }, 7000)
}

export function showSuccessAlert(msg, isVisible, type, message) {
  type.value.push('success')
  message.value.push(msg)
  showAlert(isVisible, type, message)
}

export function showErrorAlert(err, isVisible, type, message) {
  err.response.data.errors.forEach((msg) => {
    type.value.push('error')
    message.value.push(msg)
    showAlert(isVisible, type, message)
  })
}

export function convertDayWeekShortName(day) {
  const days_of_week_short_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  return days_of_week_short_name[day]
}

export function convertDayWeek(day) {
  const days_of_week = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
  ]

  return days_of_week[day]
}

// store only unique days of week and instructors for each class
export function storeUniqueValues(arr) {
  const days_week_filtered = []
  const instructors_filtered = []

  for (let i = 0; i < arr.length; i++) {
    if (!days_week_filtered.includes(arr[i].day_of_week)) {
      days_week_filtered.push(arr[i].day_of_week)
    }
    if (!instructors_filtered.includes(arr[i].name)) {
      instructors_filtered.push(arr[i].name)
    }
  }

  // sort alphabetically instructor names
  instructors_filtered.sort()

  return [days_week_filtered, instructors_filtered]
}

// add comma until it reaches the last element
export const addComma = (index, item, items) => index != items.length - 1 ? item + ', ' : item

// compute duration
export const calculateDuration = (start_time, end_time) => `(${end_time - start_time})`
   
// convert time in minutes and sum it 
export const convertMinutes = (time) => {
  // split the time string into a new array and convert each part to a number
  const [hour, minutes] = time.split(":").map(Number)

  return hour * 60 + minutes
} 
