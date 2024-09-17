
const ENV = process.env.NODE_ENV;
const PROD_URL = process.env.REACT_APP_PROD_URL;
const DEV_URL = process.env.REACT_APP_DEV_URL;

let BASE_URL = ''

if (ENV === 'production') {
    BASE_URL = 'https://' + window.location.hostname + PROD_URL + '/devices';
} else {
    BASE_URL = 'https://' + window.location.hostname + DEV_URL + '/devices';
}

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

export const createDevice = async(deviceData) => {
    let url = BASE_URL
    const rawResponse = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(deviceData),
    })
    const response = await rawResponse;
    return response

}

export const deleteAllDevices = async() => {

    let url = BASE_URL
    const rawResponse = await fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const response = await rawResponse;
    return response
}
