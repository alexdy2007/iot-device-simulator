
const BASE_URL = 'http://' + window.location.hostname + ':8000/devices'

export const getDevicesMetaData = async() => {
    return fetch(BASE_URL).then( (res) => res.json() );
};

export const getDeviceData = async(device_id, n=20) => {
    let url = `${BASE_URL}/readings/${device_id}?n_historic=${n}`
    return fetch(url).then( (res) => res.json() );
};


export const pauseDevice = async(device_id) => {
    let url = `${BASE_URL}/pause/${device_id}`
    return fetch(url).then( (res) => res.json() );
};

export const startDevice = async(device_id) => {
    let url = `${BASE_URL}/start/${device_id}`
    return fetch(url).then( (res) => res.json() );
};
