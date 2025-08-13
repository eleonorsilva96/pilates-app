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