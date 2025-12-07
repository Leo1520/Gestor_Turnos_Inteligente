const API_URL = 'http://localhost:5000/api';

let currentPage = {
    turnos: 1,
    pacientes: 1
};
const ITEMS_PER_PAGE = 10;

let allData = {
    turnos: [],
    pacientes: [],
    medicos: [],
    especialidades: []
};

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    loadEspecialidades();
    loadPacientes();
    loadMedicos();
    loadTurnos();
    setDefaultDates();
}

function setupEventListeners() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchSection(e.target.dataset.section);
        });
    });

    document.querySelectorAll('.modal-close, .btn-secondary').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modalId = btn.dataset.modal;
            if (modalId) closeModal(modalId);
        });
    });

    document.getElementById('btn-nuevo-turno').addEventListener('click', () => openModal('modal-turno'));
    document.getElementById('btn-nuevo-paciente').addEventListener('click', () => openModal('modal-paciente'));
    document.getElementById('btn-nuevo-medico').addEventListener('click', () => openModal('modal-medico'));

    document.getElementById('form-turno').addEventListener('submit', handleTurnoSubmit);
    document.getElementById('form-paciente').addEventListener('submit', handlePacienteSubmit);
    document.getElementById('form-medico').addEventListener('submit', handleMedicoSubmit);

    document.getElementById('turno-especialidad').addEventListener('change', handleEspecialidadChange);
    document.getElementById('turno-medico').addEventListener('change', handleMedicoChange);
    document.getElementById('turno-fecha').addEventListener('change', handleFechaChange);

    document.getElementById('search-turnos').addEventListener('input', (e) => searchTable('turnos', e.target.value));
    document.getElementById('search-pacientes').addEventListener('input', (e) => searchTable('pacientes', e.target.value));

    document.getElementById('btn-filtrar-turnos').addEventListener('click', loadTurnos);
    document.getElementById('btn-generar-reporte').addEventListener('click', generarReporte);
}

function switchSection(section) {
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    document.getElementById(`${section}-section`).classList.add('active');
    document.querySelector(`[data-section="${section}"]`).classList.add('active');

    if (section === 'turnos') loadTurnos();
    if (section === 'pacientes') loadPacientes();
    if (section === 'medicos') loadMedicos();
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    const formId = modalId.replace('modal', 'form');
    document.getElementById(formId).reset();
}

function setDefaultDates() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('filter-fecha-desde').value = today;
    document.getElementById('filter-fecha-hasta').value = today;
    document.getElementById('reporte-fecha').value = today;
    document.getElementById('turno-fecha').min = today;
}

async function loadEspecialidades() {
    try {
        const response = await fetch(`${API_URL}/especialidades`);
        const result = await response.json();
        allData.especialidades = result.data;

        const selects = ['turno-especialidad', 'medico-especialidad'];
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Seleccione...</option>';
            result.data.forEach(esp => {
                select.innerHTML += `<option value="${esp.id}">${esp.nombre}</option>`;
            });
        });
    } catch (error) {
        console.error('Error loading especialidades:', error);
        showError('Error al cargar especialidades');
    }
}
            select.innerHTML = '<option value="">Seleccione especialidad</option>';
            result.data.forEach(esp => {
                select.innerHTML += `<option value="${esp.id}">${esp.nombre}</option>`;
            });
        });
    } catch (error) {
        showNotification('Error al cargar especialidades', 'error');
    }
}

async function loadPacientes() {
    try {
        const response = await fetch(`${API_URL}/pacientes`);
        const result = await response.json();
        allData.pacientes = result.data;

        const select = document.getElementById('turno-paciente');
        select.innerHTML = '<option value="">Seleccione un paciente</option>';
        result.data.forEach(pac => {
            select.innerHTML += `<option value="${pac.id}">${pac.apellido}, ${pac.nombre} (${pac.dni})</option>`;
        });

        renderPacientesTable();
    } catch (error) {
        showNotification('Error al cargar pacientes', 'error');
    }
}

async function loadMedicos() {
    try {
        const response = await fetch(`${API_URL}/medicos?activos=false`);
        const result = await response.json();
        allData.medicos = result.data;

        const select = document.getElementById('filter-medico');
        select.innerHTML = '<option value="">Todos los médicos</option>';
        result.data.forEach(med => {
            select.innerHTML += `<option value="${med.id}">Dr. ${med.apellido}, ${med.nombre}</option>`;
        });

        renderMedicosTable();
    } catch (error) {
        showNotification('Error al cargar médicos', 'error');
    }
}

async function loadTurnos() {
    try {
        let url = `${API_URL}/turnos?`;
        const fechaDesde = document.getElementById('filter-fecha-desde').value;
        const fechaHasta = document.getElementById('filter-fecha-hasta').value;
        const medico = document.getElementById('filter-medico').value;
        const estado = document.getElementById('filter-estado').value;

        if (fechaDesde) url += `fecha_desde=${fechaDesde}T00:00:00&`;
        if (fechaHasta) url += `fecha_hasta=${fechaHasta}T23:59:59&`;
        if (medico) url += `id_medico=${medico}&`;
        if (estado) url += `estado=${estado}&`;

        const response = await fetch(url);
        const result = await response.json();
        allData.turnos = result.data;
        renderTurnosTable();
    } catch (error) {
        showNotification('Error al cargar turnos', 'error');
    }
}

function renderTurnosTable(data = allData.turnos) {
    const tbody = document.getElementById('turnos-table-body');
    document.getElementById('turnos-count').textContent = data.length;

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No se encontraron turnos</td></tr>';
        return;
    }

    const start = (currentPage.turnos - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const pageData = data.slice(start, end);

    tbody.innerHTML = pageData.map(turno => {
        const fecha = new Date(turno.fecha_hora);
        const fechaStr = fecha.toLocaleDateString('es-AR');
        const horaStr = fecha.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });

        return `
            <tr>
                <td>${fechaStr} ${horaStr}</td>
                <td>${turno.pacientes.apellido}, ${turno.pacientes.nombre}</td>
                <td>${turno.pacientes.dni}</td>
                <td>Dr. ${turno.medicos.apellido}, ${turno.medicos.nombre}</td>
                <td>${turno.medicos.especialidades.nombre}</td>
                <td><span class="badge badge-${turno.estado}">${turno.estado.toUpperCase()}</span></td>
                <td>
                    <div class="action-buttons">
                        ${turno.estado === 'pendiente' ? `
                            <button class="btn btn-success" onclick="cambiarEstado('${turno.id}', 'atendido')">Atender</button>
                            <button class="btn btn-danger" onclick="cancelarTurno('${turno.id}')">Cancelar</button>
                        ` : ''}
                        ${turno.estado === 'pendiente' ? `
                            <button class="btn btn-warning" onclick="cambiarEstado('${turno.id}', 'ausente')">Ausente</button>
                        ` : ''}
                    </div>
                </td>
            </tr>
        `;
    }).join('');

    renderPagination('turnos', data.length);
}

function renderPacientesTable(data = allData.pacientes) {
    const tbody = document.getElementById('pacientes-table-body');
    document.getElementById('pacientes-count').textContent = data.length;

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No se encontraron pacientes</td></tr>';
        return;
    }

    const start = (currentPage.pacientes - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const pageData = data.slice(start, end);

    tbody.innerHTML = pageData.map(pac => `
        <tr>
            <td>${pac.dni}</td>
            <td>${pac.apellido}, ${pac.nombre}</td>
            <td>${new Date(pac.fecha_nacimiento).toLocaleDateString('es-AR')}</td>
            <td>${pac.telefono}</td>
            <td>${pac.email || '-'}</td>
            <td>${pac.obra_social}</td>
            <td>
                <button class="btn btn-secondary" onclick="verHistorial('${pac.id}')">Historial</button>
            </td>
        </tr>
    `).join('');

    renderPagination('pacientes', data.length);
}

function renderMedicosTable() {
    const tbody = document.getElementById('medicos-table-body');

    if (allData.medicos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No se encontraron médicos</td></tr>';
        return;
    }

    tbody.innerHTML = allData.medicos.map(med => `
        <tr>
            <td>${med.matricula}</td>
            <td>${med.apellido}, ${med.nombre}</td>
            <td>${med.especialidades.nombre}</td>
            <td>${med.telefono}</td>
            <td>${med.email || '-'}</td>
            <td><span class="badge badge-${med.activo ? 'activo' : 'inactivo'}">${med.activo ? 'ACTIVO' : 'INACTIVO'}</span></td>
            <td>
                <button class="btn btn-${med.activo ? 'danger' : 'success'}" onclick="toggleMedicoEstado('${med.id}', ${!med.activo})">
                    ${med.activo ? 'Desactivar' : 'Activar'}
                </button>
            </td>
        </tr>
    `).join('');
}

function renderPagination(type, totalItems) {
    const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
    const container = document.getElementById(`${type}-pagination`);

    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = `<button onclick="changePage('${type}', ${currentPage[type] - 1})" ${currentPage[type] === 1 ? 'disabled' : ''}>Anterior</button>`;

    for (let i = 1; i <= totalPages; i++) {
        html += `<button class="${i === currentPage[type] ? 'active' : ''}" onclick="changePage('${type}', ${i})">${i}</button>`;
    }

    html += `<button onclick="changePage('${type}', ${currentPage[type] + 1})" ${currentPage[type] === totalPages ? 'disabled' : ''}>Siguiente</button>`;

    container.innerHTML = html;
}

function changePage(type, page) {
    currentPage[type] = page;
    if (type === 'turnos') renderTurnosTable();
    if (type === 'pacientes') renderPacientesTable();
}

function searchTable(type, query) {
    const lowerQuery = query.toLowerCase();

    if (type === 'turnos') {
        const filtered = allData.turnos.filter(t =>
            t.pacientes.nombre.toLowerCase().includes(lowerQuery) ||
            t.pacientes.apellido.toLowerCase().includes(lowerQuery) ||
            t.pacientes.dni.includes(lowerQuery)
        );
        currentPage.turnos = 1;
        renderTurnosTable(filtered);
    }

    if (type === 'pacientes') {
        const filtered = allData.pacientes.filter(p =>
            p.nombre.toLowerCase().includes(lowerQuery) ||
            p.apellido.toLowerCase().includes(lowerQuery) ||
            p.dni.includes(lowerQuery)
        );
        currentPage.pacientes = 1;
        renderPacientesTable(filtered);
    }
}

async function handleEspecialidadChange(e) {
    const especialidadId = e.target.value;
    const medicoSelect = document.getElementById('turno-medico');

    if (!especialidadId) {
        medicoSelect.disabled = true;
        medicoSelect.innerHTML = '<option value="">Primero seleccione especialidad</option>';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/medicos/especialidad/${especialidadId}`);
        const result = await response.json();

        medicoSelect.disabled = false;
        medicoSelect.innerHTML = '<option value="">Seleccione un médico</option>';
        result.data.forEach(med => {
            medicoSelect.innerHTML += `<option value="${med.id}">Dr. ${med.apellido}, ${med.nombre}</option>`;
        });
    } catch (error) {
        showNotification('Error al cargar médicos', 'error');
    }
}

async function handleMedicoChange() {
    await updateDisponibilidad();
}

async function handleFechaChange() {
    await updateDisponibilidad();
}

async function updateDisponibilidad() {
    const medicoId = document.getElementById('turno-medico').value;
    const fecha = document.getElementById('turno-fecha').value;
    const horaSelect = document.getElementById('turno-hora');

    if (!medicoId || !fecha) {
        horaSelect.disabled = true;
        horaSelect.innerHTML = '<option value="">Seleccione fecha y médico</option>';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/turnos/disponibilidad?id_medico=${medicoId}&fecha=${fecha}`);
        const result = await response.json();

        horaSelect.disabled = false;
        horaSelect.innerHTML = '<option value="">Seleccione una hora</option>';

        if (result.data.length === 0) {
            horaSelect.innerHTML = '<option value="">No hay horarios disponibles</option>';
            return;
        }

        result.data.forEach(hora => {
            horaSelect.innerHTML += `<option value="${hora}">${hora}</option>`;
        });
    } catch (error) {
        showNotification('Error al consultar disponibilidad', 'error');
    }
}

async function handleTurnoSubmit(e) {
    e.preventDefault();

    const data = {
        id_paciente: document.getElementById('turno-paciente').value,
        id_medico: document.getElementById('turno-medico').value,
        fecha_hora: `${document.getElementById('turno-fecha').value}T${document.getElementById('turno-hora').value}:00`,
        duracion_minutos: parseInt(document.getElementById('turno-duracion').value),
        motivo_consulta: document.getElementById('turno-motivo').value
    };

    try {
        const response = await fetch(`${API_URL}/turnos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showNotification('Turno creado exitosamente', 'success');
            closeModal('modal-turno');
            loadTurnos();
        } else {
            showNotification(result.error || 'Error al crear turno', 'error');
        }
    } catch (error) {
        showNotification('Error al crear turno', 'error');
    }
}

async function handlePacienteSubmit(e) {
    e.preventDefault();

    const data = {
        dni: document.getElementById('paciente-dni').value,
        nombre: document.getElementById('paciente-nombre').value,
        apellido: document.getElementById('paciente-apellido').value,
        fecha_nacimiento: document.getElementById('paciente-fecha-nacimiento').value,
        telefono: document.getElementById('paciente-telefono').value,
        email: document.getElementById('paciente-email').value,
        direccion: document.getElementById('paciente-direccion').value,
        obra_social: document.getElementById('paciente-obra-social').value
    };

    try {
        const response = await fetch(`${API_URL}/pacientes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showNotification('Paciente registrado exitosamente', 'success');
            closeModal('modal-paciente');
            loadPacientes();
        } else {
            showNotification(result.error || 'Error al registrar paciente', 'error');
        }
    } catch (error) {
        showNotification('Error al registrar paciente', 'error');
    }
}

async function handleMedicoSubmit(e) {
    e.preventDefault();

    const data = {
        matricula: document.getElementById('medico-matricula').value,
        nombre: document.getElementById('medico-nombre').value,
        apellido: document.getElementById('medico-apellido').value,
        id_especialidad: document.getElementById('medico-especialidad').value,
        telefono: document.getElementById('medico-telefono').value,
        email: document.getElementById('medico-email').value
    };

    try {
        const response = await fetch(`${API_URL}/medicos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showNotification('Médico registrado exitosamente', 'success');
            closeModal('modal-medico');
            loadMedicos();
        } else {
            showNotification(result.error || 'Error al registrar médico', 'error');
        }
    } catch (error) {
        showNotification('Error al registrar médico', 'error');
    }
}

async function cambiarEstado(id, nuevoEstado) {
    try {
        const response = await fetch(`${API_URL}/turnos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ estado: nuevoEstado })
        });

        if (response.ok) {
            showNotification(`Turno marcado como ${nuevoEstado}`, 'success');
            loadTurnos();
        } else {
            showNotification('Error al actualizar turno', 'error');
        }
    } catch (error) {
        showNotification('Error al actualizar turno', 'error');
    }
}

async function cancelarTurno(id) {
    if (!confirm('¿Está seguro que desea cancelar este turno?')) return;

    try {
        const response = await fetch(`${API_URL}/turnos/${id}/cancelar`, {
            method: 'PUT'
        });

        const result = await response.json();

        if (response.ok) {
            showNotification('Turno cancelado exitosamente', 'success');
            loadTurnos();
        } else {
            showNotification(result.error || 'Error al cancelar turno', 'error');
        }
    } catch (error) {
        showNotification('Error al cancelar turno', 'error');
    }
}

async function toggleMedicoEstado(id, nuevoEstado) {
    try {
        const response = await fetch(`${API_URL}/medicos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ activo: nuevoEstado })
        });

        if (response.ok) {
            showNotification(`Médico ${nuevoEstado ? 'activado' : 'desactivado'}`, 'success');
            loadMedicos();
        } else {
            showNotification('Error al actualizar médico', 'error');
        }
    } catch (error) {
        showNotification('Error al actualizar médico', 'error');
    }
}

async function verHistorial(idPaciente) {
    try {
        const response = await fetch(`${API_URL}/pacientes/${idPaciente}/historial`);
        const result = await response.json();

        if (result.data.length === 0) {
            alert('El paciente no tiene historial de turnos');
            return;
        }

        let historial = 'HISTORIAL DE TURNOS:\n\n';
        result.data.forEach(turno => {
            const fecha = new Date(turno.fecha_hora).toLocaleString('es-AR');
            historial += `Fecha: ${fecha}\nMédico: Dr. ${turno.medicos.apellido}\nEspecialidad: ${turno.medicos.especialidades.nombre}\nEstado: ${turno.estado}\n\n`;
        });

        alert(historial);
    } catch (error) {
        showNotification('Error al cargar historial', 'error');
    }
}

async function generarReporte() {
    const fecha = document.getElementById('reporte-fecha').value;

    if (!fecha) {
        showNotification('Seleccione una fecha', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/reportes/diario?fecha=${fecha}`);
        const result = await response.json();

        document.getElementById('stat-total').textContent = result.data.estadisticas.total;
        document.getElementById('stat-atendidos').textContent = result.data.estadisticas.atendidos;
        document.getElementById('stat-pendientes').textContent = result.data.estadisticas.pendientes;
        document.getElementById('stat-tasa').textContent = `${result.data.estadisticas.tasa_asistencia}%`;

        document.getElementById('stats-container').style.display = 'grid';
        document.getElementById('reporte-table-container').style.display = 'block';

        const tbody = document.getElementById('reporte-table-body');
        if (result.data.turnos.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay turnos para esta fecha</td></tr>';
        } else {
            tbody.innerHTML = result.data.turnos.map(t => `
                <tr>
                    <td>${new Date(t.fecha_hora).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}</td>
                    <td>${t.pacientes.apellido}, ${t.pacientes.nombre}</td>
                    <td>Dr. ${t.medicos.apellido}</td>
                    <td>${t.medicos.especialidades.nombre}</td>
                    <td><span class="badge badge-${t.estado}">${t.estado.toUpperCase()}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        showNotification('Error al generar reporte', 'error');
    }
}

function showNotification(message, type) {
    const color = type === 'success' ? '#10b981' : '#ef4444';
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${color};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: 600;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}
