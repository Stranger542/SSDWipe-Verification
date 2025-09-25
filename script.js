const verifyBtn = document.getElementById('verifyBtn');
const serialNumberInput = document.getElementById('serialNumberInput');
const initialState = document.getElementById('initialState');
const loadingState = document.getElementById('loadingState');
const notFoundState = document.getElementById('notFoundState');
const successState = document.getElementById('successState');

// The URL of your Python backend server
const BACKEND_URL = 'http://127.0.0.1:5001';

async function verifySerialNumber() {
    const serialNumber = serialNumberInput.value.trim();
    if (!serialNumber) {
        alert("Please enter a serial number.");
        return;
    }

    setState('loading');
    verifyBtn.disabled = true;

    try {
        const response = await fetch(`${BACKEND_URL}/verify/${serialNumber}`);

        if (!response.ok) {
            throw new Error('Certificate not found');
        }

        const result = await response.json();

        if (result.success) {
            const data = result.data;
            document.getElementById('cert-serial').textContent = data.serialNumber;
            document.getElementById('cert-model').textContent = data.model;
            document.getElementById('cert-wipe-method').textContent = data.wipeMethod;
            
            const date = new Date(data.timestamp * 1000);
            document.getElementById('cert-timestamp').textContent = date.toLocaleString();
            
            setState('success');
        } else {
            setState('notFound');
        }
    } catch (error) {
        console.error("Verification failed:", error);
        setState('notFound');
    } finally {
        verifyBtn.disabled = false;
    }
}

function setState(state) {
    initialState.classList.add('hidden');
    loadingState.classList.add('hidden');
    notFoundState.classList.add('hidden');
    successState.classList.add('hidden');

    if (state === 'loading') loadingState.classList.remove('hidden');
    else if (state === 'notFound') notFoundState.classList.remove('hidden');
    else if (state === 'success') successState.classList.remove('hidden');
    else initialState.classList.remove('hidden');
}

verifyBtn.addEventListener('click', verifySerialNumber);
serialNumberInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        verifySerialNumber();
    }
});