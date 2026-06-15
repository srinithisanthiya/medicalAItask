const API_BASE = "/api/patients";
const form = document.getElementById("patient-form");
const formTitle = document.getElementById("form-title");
const patientIdInput = document.getElementById("patient-id");
const submitBtn = document.getElementById("submit-btn");
const cancelEditBtn = document.getElementById("cancel-edit-btn");
const refreshBtn = document.getElementById("refresh-btn");
const tableBody = document.getElementById("patients-table-body");
const alertContainer = document.getElementById("alert-container");
const fields = {
  fullName: document.getElementById("full-name"),
  dateOfBirth: document.getElementById("date-of-birth"),
  email: document.getElementById("email"),
  glucose: document.getElementById("glucose"),
  haemoglobin: document.getElementById("haemoglobin"),
  cholesterol: document.getElementById("cholesterol"),
};

function showAlert(message, type = "danger") {
  alertContainer.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>`;
}
function clearAlert() { alertContainer.innerHTML = ""; }
function isValidEmail(email) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); }

function validateForm() {
  let valid = true;
  Object.values(fields).forEach((f) => f.classList.remove("is-invalid"));
  if (fields.fullName.value.trim().length < 2) { fields.fullName.classList.add("is-invalid"); valid = false; }
  const dob = fields.dateOfBirth.value;
  if (!dob || dob > new Date().toISOString().split("T")[0]) { fields.dateOfBirth.classList.add("is-invalid"); valid = false; }
  if (!isValidEmail(fields.email.value.trim())) { fields.email.classList.add("is-invalid"); valid = false; }
  ["glucose", "haemoglobin", "cholesterol"].forEach((key) => {
    if (Number.isNaN(Number(fields[key].value))) { fields[key].classList.add("is-invalid"); valid = false; }
  });
  return valid;
}

function getFormPayload() {
  return {
    full_name: fields.fullName.value.trim(),
    date_of_birth: fields.dateOfBirth.value,
    email: fields.email.value.trim(),
    glucose: Number(fields.glucose.value),
    haemoglobin: Number(fields.haemoglobin.value),
    cholesterol: Number(fields.cholesterol.value),
  };
}

function resetForm() {
  form.reset(); patientIdInput.value = "";
  formTitle.textContent = "Add Patient Record";
  submitBtn.textContent = "Save & Predict";
  cancelEditBtn.classList.add("d-none");
  Object.values(fields).forEach((f) => f.classList.remove("is-invalid"));
}

function setEditMode(patient) {
  patientIdInput.value = patient.id;
  fields.fullName.value = patient.full_name;
  fields.dateOfBirth.value = patient.date_of_birth;
  fields.email.value = patient.email;
  fields.glucose.value = patient.glucose;
  fields.haemoglobin.value = patient.haemoglobin;
  fields.cholesterol.value = patient.cholesterol;
  formTitle.textContent = "Edit Patient Record";
  submitBtn.textContent = "Update & Re-predict";
  cancelEditBtn.classList.remove("d-none");
}

function escapeHtml(v) {
  return String(v).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
}

function renderPatients(patients) {
  if (!patients.length) {
    tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-4">No patient records yet.</td></tr>`;
    return;
  }
  tableBody.innerHTML = patients.map((p) => `
    <tr>
      <td>${escapeHtml(p.full_name)}</td>
      <td>${new Date(p.date_of_birth).toLocaleDateString()}</td>
      <td>${escapeHtml(p.email)}</td>
      <td>${p.glucose}</td><td>${p.haemoglobin}</td><td>${p.cholesterol}</td>
      <td class="remarks-cell">${escapeHtml(p.remarks)}</td>
      <td class="text-end">
        <button class="btn btn-sm btn-outline-primary me-1" data-action="edit" data-id="${p.id}">Edit</button>
        <button class="btn btn-sm btn-outline-danger" data-action="delete" data-id="${p.id}">Delete</button>
      </td>
    </tr>`).join("");
}

async function loadPatients() {
  const r = await fetch(API_BASE);
  if (!r.ok) return showAlert("Failed to load records.");
  renderPatients(await r.json());
}

async function savePatient(e) {
  e.preventDefault(); clearAlert();
  if (!validateForm()) return showAlert("Please correct the highlighted validation errors.");
  const payload = getFormPayload();
  const id = patientIdInput.value;
  const isEdit = Boolean(id);
  submitBtn.disabled = true;
  try {
    const r = await fetch(isEdit ? `${API_BASE}/${id}` : API_BASE, {
      method: isEdit ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.detail || "Request failed.");
    showAlert(isEdit ? "Record updated with new AI remarks." : "Record created with AI remarks.", "success");
    resetForm(); await loadPatients();
  } catch (err) { showAlert(err.message); }
  finally { submitBtn.disabled = false; submitBtn.textContent = isEdit ? "Update & Re-predict" : "Save & Predict"; }
}

async function deletePatient(id) {
  if (!confirm("Delete this record?")) return;
  const r = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
  if (!r.ok) return showAlert("Delete failed.");
  showAlert("Record deleted.", "success"); await loadPatients();
}

async function editPatient(id) {
  const r = await fetch(`${API_BASE}/${id}`);
  if (!r.ok) return showAlert("Failed to load record.");
  setEditMode(await r.json());
}

tableBody.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-action]");
  if (!btn) return;
  btn.dataset.action === "edit" ? editPatient(btn.dataset.id) : deletePatient(btn.dataset.id);
});
form.addEventListener("submit", savePatient);
cancelEditBtn.addEventListener("click", resetForm);
refreshBtn.addEventListener("click", loadPatients);
loadPatients();
