
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

// export function storeUniqueValues(arr, prop) {
//   const values_filtered = []

//   for (let i = 0; i < arr.length; i++) {
//     // use bracket notation when we want to use the name of the variable to access the object property
//     if (!values_filtered.includes(arr[i][prop])) values_filtered.push(arr[i][prop])
//   }

//   // sort alphabetically instructor names
//   values_filtered.sort()

//   return values_filtered
// }

export function storeUniqueValues(arr, prop) {
  const uniqueValuesArr = []

  for (let i = 0; i < arr.length; i++) {

      if (uniqueValuesArr.length === 0) uniqueValuesArr.push(arr[i])
      // check in the new array if it already have the value from schedules arr
      const checkForDuplicates = uniqueValuesArr.some((v) => v[prop] === arr[i][prop])
      // if does not have push it to the new array
      if (!checkForDuplicates) uniqueValuesArr.push(arr[i])
  }

  uniqueValuesArr.sort()

  return uniqueValuesArr

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
