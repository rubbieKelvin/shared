const company_name = window.sharedConfig.company_name;
const application_name = window.sharedConfig.application_name;
const application_url = window.sharedConfig.application_url;
const application_icon_url = window.sharedConfig.application_icon_url;
const callback_url = window.sharedConfig.callback_url;
const login_fields = window.sharedConfig.login_fields;

/**
 *
 * @param {String} field_name
 */
function togglePasswordInput(field_name) {
  /**
   * @type {HTMLInputElement}
   */
  const input_field = document.getElementById(`${field_name}_login_input`);
  const eye_icon = document.getElementById(`${field_name}_eye_icon`);
  const eye_off_icon = document.getElementById(`${field_name}_eye_off_icon`);

  if (input_field.type === "password") {
    input_field.type = "text";
    eye_icon.style.display = "none";
    eye_off_icon.style.display = "initial";
  } else {
    input_field.type = "password";
    eye_icon.style.display = "initial";
    eye_off_icon.style.display = "none";
  }
}
