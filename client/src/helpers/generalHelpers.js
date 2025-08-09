export function showAlert(visible, type, message) {
  visible.value = true

  setTimeout(() => {
    visible.value = false
    type.value = []
    message.value = []
  }, 7000)
}
