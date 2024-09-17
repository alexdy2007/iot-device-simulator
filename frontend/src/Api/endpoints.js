
const ENV = process.env.NODE_ENV;
const PROD_URL = process.env.REACT_APP_PROD_URL;
const DEV_URL = process.env.REACT_APP_DEV_URL;

let BASE_URL = ''

if (ENV === 'production') {
    BASE_URL = 'https://' + window.location.hostname + PROD_URL + '/endpoints';
} else {
    BASE_URL = 'https://' + window.location.hostname + DEV_URL + '/endpoints';
}

export const createEndpoint = async(endpointData) => {
    let url = BASE_URL
    const rawResponse = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(endpointData),
    })
    const response = await rawResponse;
    return response
};

export const getEndpoints = async() => {
    return fetch(BASE_URL).then( (res) => res.json() );
};