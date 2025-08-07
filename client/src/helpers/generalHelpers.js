
export function showAlert(alert) {
    alert.value = true

      setTimeout(() => {
        alert.value = false
      }, 5000)
}
